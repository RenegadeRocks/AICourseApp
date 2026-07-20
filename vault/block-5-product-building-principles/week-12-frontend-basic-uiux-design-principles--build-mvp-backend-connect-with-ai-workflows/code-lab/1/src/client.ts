/**
 * Minimal AI-native frontend — the streaming request-to-render loop.
 *
 * Demonstrates Tuesday's UX patterns and Friday's streaming loop with no
 * framework: optimistic render of the user's message, token streaming into an
 * assistant placeholder, and graceful failure that PRESERVES the user's input.
 * The Next.js + AI SDK equivalent (useChat) is in the README.
 */

interface Els {
  form: HTMLFormElement;
  input: HTMLTextAreaElement;
  button: HTMLButtonElement;
  thread: HTMLElement;
  empty: HTMLElement;
}

function els(): Els {
  const get = <T extends HTMLElement>(id: string): T => {
    const el = document.getElementById(id);
    if (el === null) throw new Error(`missing #${id}`);
    return el as T;
  };
  return {
    form: get<HTMLFormElement>("form"),
    input: get<HTMLTextAreaElement>("prompt"),
    button: get<HTMLButtonElement>("send"),
    thread: get<HTMLElement>("thread"),
    empty: get<HTMLElement>("empty"),
  };
}

function bubble(role: "user" | "assistant", text: string): HTMLElement {
  const el = document.createElement("div");
  el.className = `bubble ${role}`;
  el.textContent = text;
  return el;
}

async function stream(prompt: string, target: HTMLElement, onError: (m: string) => void): Promise<void> {
  const res = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (!res.ok || res.body === null) {
    onError("The server did not respond. Your prompt is preserved — retry.");
    return;
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  target.textContent = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";
    for (const frame of frames) {
      const lines = frame.split("\n");
      const event = lines.find((l) => l.startsWith("event: "))?.slice(7) ?? "message";
      const dataLine = lines.find((l) => l.startsWith("data: "));
      if (dataLine === undefined) continue;
      const payload = JSON.parse(dataLine.slice(6)) as { text?: string; message?: string };
      if (event === "token") {
        target.textContent += payload.text ?? "";
      } else if (event === "error") {
        onError(payload.message ?? "Generation failed. Your prompt is preserved — retry.");
        return;
      }
      // event === "done" falls through: the stream is complete.
    }
  }
}

function main(): void {
  const el = els();

  el.form.addEventListener("submit", (e) => {
    e.preventDefault();
    const prompt = el.input.value.trim();
    if (prompt.length === 0) return;

    el.empty.hidden = true;
    // Optimistic render of the ACTION (not the content): the user's message
    // appears instantly; the assistant bubble is a streaming placeholder.
    el.thread.appendChild(bubble("user", prompt));
    const assistant = bubble("assistant", "…");
    el.thread.appendChild(assistant);
    el.thread.scrollTop = el.thread.scrollHeight;

    el.button.disabled = true;
    const submitted = prompt;
    el.input.value = "";

    const onError = (message: string): void => {
      assistant.classList.add("error");
      assistant.textContent = message;
      const retry = document.createElement("button");
      retry.type = "button";
      retry.className = "retry";
      retry.textContent = "Retry";
      retry.addEventListener("click", () => {
        el.input.value = submitted; // input preserved on failure
        el.button.disabled = false;
        el.input.focus();
      });
      assistant.appendChild(retry);
      el.button.disabled = false;
    };

    void stream(submitted, assistant, onError).finally(() => {
      el.button.disabled = false;
      el.thread.scrollTop = el.thread.scrollHeight;
    });
  });
}

main();
