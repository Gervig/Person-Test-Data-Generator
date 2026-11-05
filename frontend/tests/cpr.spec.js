import { test, expect } from "@playwright/test";

test("generate a random CPR number", async ({ page }) => {
  await page.goto("http://localhost:5173/");

  await page.getByRole('combobox').selectOption('cpr');
  await page.getByRole('button', { name: 'Generate' }).click()

    // Get the generated JSON
  const output = page.locator("pre");
  const jsonText = await output.textContent();

  // Convert JSON string into a JavaScript object
  const CPR = JSON.parse(jsonText);

  //validate generated cpr number
  expect(CPR.cpr).toMatch(/^\d{10}$/);
});