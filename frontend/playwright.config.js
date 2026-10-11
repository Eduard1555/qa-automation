import { defineConfig, devices } from "@playwright/test";

const pythonExecutable =
  process.platform === "win32"
    ? ".venv\\Scripts\\python.exe"
    : "python";

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
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
  ],
});