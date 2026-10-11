import os from "node:os";
import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const pythonExecutable =
  process.platform === "win32"
    ? ".venv\\Scripts\\python.exe"
    : "python";

// Each run gets a fresh SQLite file, so UI tests never touch qa_automation.db.
const testDatabasePath = path.join(
  os.tmpdir(),
  `qa-automation-playwright-${Date.now()}.db`
);

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,

  reporter: [
    ["list"],
    ["html", { outputFolder: "playwright-report", open: "never" }],
  ],

  use: {
    baseURL: "http://localhost:5173",
    trace: "retain-on-failure",
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  webServer: [
    {
      command: "npm run dev -- --host 127.0.0.1",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
    {
      command: `${pythonExecutable} -m uvicorn main:app --host 127.0.0.1 --port 8000`,
      cwd: "..",
      env: { QA_DATABASE_PATH: testDatabasePath },
      url: "http://127.0.0.1:8000/health",
      // Never reuse a running dev backend: it would write to the real database.
      reuseExistingServer: false,
      timeout: 30_000,
    },
  ],
});