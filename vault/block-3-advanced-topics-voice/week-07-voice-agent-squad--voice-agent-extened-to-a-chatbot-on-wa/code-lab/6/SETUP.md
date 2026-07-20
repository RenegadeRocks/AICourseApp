# SETUP — wiring the two surfaces

Do the brain first (it's the only part that runs offline), then one voice
platform, then WhatsApp. Budget ~60–90 minutes including account sign-ups.

## 0. Brain (offline, 5 min)

```bash
cd code-lab/6
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn brain.app:app --reload --port 8000
curl localhost:8000/health          # {"ok": true, "writes_enabled": false}
ngrok http 8000                      # note the https URL -> <NGROK>
```

Smoke-test the shared core with no platforms at all:

```bash
curl -s localhost:8000/tools -H 'content-type: application/json' \
  -d '{"transcript":"I need to reschedule my appointment","from":"+919000000001","call_id":"t1"}'
# -> a booking reply referencing "Tue 14th, 3:00pm"
```

That proves the router + gateway + CRM work before any vendor is involved.

## 1. Voice squad — Vapi (recommended for the squad primitive)

1. Sign up at dashboard.vapi.ai, copy an API key into `VAPI_API_KEY`.
2. Edit `configs/squad.vapi.json`: replace every `<NGROK>` with your tunnel URL.
3. Create the squad:
   ```bash
   curl -s https://api.vapi.ai/squad \
     -H "Authorization: Bearer $VAPI_API_KEY" \
     -H "content-type: application/json" \
     -d @configs/squad.vapi.json
   ```
4. Attach a phone number (Vapi provides a test number on trial) to the squad's
   triage member in the dashboard, or via the API.
5. Call the number. The `/tools` webhook fires when a specialist calls its tool;
   watch `events.jsonl` fill.

Platform payload note: Vapi posts a `message` object on tool calls; the brain's
`/tools` reads `message.text` / `customer.number` / `call.id`. If your Vapi
version nests differently, adjust the three `.get(...)` lines in `voice_tools`.

## 1-alt. Voice squad — Retell

1. Sign up at dashboard.retellai.com, copy `RETELL_API_KEY`.
2. Create a Retell LLM + agent from `configs/squad.retell.json` (Retell's create
   endpoints; the file mirrors the logical design). Point custom tools at
   `https://<NGROK>/tools`.
3. Retell posts `call_id` + `transcript` + `from`; the brain already reads those
   fallbacks.

## 2. WhatsApp Cloud API (test number sandbox)

1. developers.facebook.com -> create app -> add **WhatsApp** product.
2. Under **API Setup**: copy the temporary access token -> `WA_ACCESS_TOKEN`,
   and the test number's `phone_number_id` -> `WA_PHONE_NUMBER_ID`. Add your own
   phone as a recipient (sandbox only sends to verified testers).
3. **Configure webhook**: callback URL `https://<NGROK>/wa/webhook`, verify token
   = whatever you set in `WA_VERIFY_TOKEN`. Subscribe to the **messages** field.
   Meta will GET the URL to verify — the brain answers the handshake.
4. From your phone, message the test number:
   - a **text**: "what's my balance" -> expect an interactive reply,
   - a **voice note**: speak "reschedule my appointment" -> the adapter fetches
     the audio (or uses Meta's transcription) and replies,
   - wait 24h+ and message again to feel the window mechanic (or just read the
     `window_open` logic — Friday, Layer 1).

Token note: the sandbox token expires in 24h. For a longer-lived test, create a
System User token with `whatsapp_business_messaging`. Never commit either.

## 3. Run the graded exercises + eval

Voice, three calls: (1) "what's my appointment" [+919000000001], (2) a
multi-step booking, (3) **interrupt during the triage->specialist handoff** with
"actually it's about my bill" — this is the seam that breaks (Wednesday). Then:

```bash
python eval.py events.jsonl
```

Paste the platform dashboard's first-audio p50/p95 for the three calls into your
build writeup, and hand-grade the barge-in recovery (did the billing specialist
pick up without re-asking your name?).

## Turning on writes (deliberate, optional)

`reschedule_appointment` is a WRITE tool. It stays dead until you:
1. set `ALLOW_WRITES=true` in `.env`,
2. implement a confirmation-read in the booking specialist prompt ("I'm moving
   you to Thursday 10am — confirm?") and pass `confirmed=true` to the gateway
   only after explicit assent,
3. keep the hard caps in `tools/gateway.py`.

This ordering is Thursday's Layer 5 made executable. Do not shortcut it.
