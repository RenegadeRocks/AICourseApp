import path from "node:path";

export const REPO_ROOT = path.resolve(process.cwd(), "..");
export const PROJECT_ROOT = REPO_ROOT;
export const VAULT_ROOT = path.join(REPO_ROOT, "vault");
export const CURRICULUM_JSON = path.join(REPO_ROOT, "curriculum.json");
export const PROGRESS_DB = path.join(process.cwd(), "progress.db");
