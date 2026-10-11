import { test, expect } from "@playwright/test";

test.describe("QA Automation Dashboard", () => {
  test("displays the dashboard and API connection", async ({ page }) => {
    await page.goto("/");

    await expect(
      page.getByRole("heading", { name: "Products", exact: true })
    ).toBeVisible();

    await expect(page.getByText("API connected")).toBeVisible();

    await expect(
      page.getByRole("heading", { name: "Product catalog" })
    ).toBeVisible();
  });

  test("loads products from the API", async ({ page }) => {
    await page.goto("/");

    await expect(
      page.getByRole("cell", { name: "Mechanical Keyboard" })
    ).toBeVisible();

    await expect(
      page.getByRole("cell", { name: "Gaming Mouse" })
    ).toBeVisible();

    await expect(
      page.getByRole("cell", { name: "USB-C Hub" })
    ).toBeVisible();
  });

  test("filters products using the search field", async ({ page }) => {
    await page.goto("/");

    const searchInput = page.getByRole("textbox", {
      name: "Search products",
    });

    await searchInput.fill("Gaming Mouse");

    await expect(
      page.getByRole("cell", { name: "Gaming Mouse" })
    ).toBeVisible();

    await expect(
      page.getByRole("cell", { name: "Mechanical Keyboard" })
    ).toHaveCount(0);

    await expect(
      page.getByRole("cell", { name: "USB-C Hub" })
    ).toHaveCount(0);
  });

  test("adds a new product successfully", async ({ page }) => {
    await page.goto("/");

    const uniqueName = `Playwright Product ${Date.now()}`;

    await page.getByLabel("Product name").fill(uniqueName);
    await page.getByLabel("Price (RON)").fill("199.99");
    await page.getByLabel("Stock quantity").fill("12");

    await page.getByRole("button", { name: "Add product" }).click();

    await expect(page.getByRole("status")).toContainText(
      `"${uniqueName}" was added to your catalog.`
    );

    await expect(
      page.getByRole("cell", { name: uniqueName })
    ).toBeVisible();
  });

  test("requires a product name", async ({ page }) => {
    await page.goto("/");

    await page.getByLabel("Price (RON)").fill("49.99");
    await page.getByLabel("Stock quantity").fill("5");

    await page.getByRole("button", { name: "Add product" }).click();

    await expect(page.getByLabel("Product name")).toHaveJSProperty(
      "validity.valid",
      false
    );
  });

  test("displays the out-of-stock status", async ({ page }) => {
    await page.goto("/");

    const productRow = page.getByRole("row").filter({
      has: page.getByRole("cell", { name: "USB-C Hub" }),
    });

    await expect(productRow.getByText("Out of stock")).toBeVisible();
  });
});