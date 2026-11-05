import { test, expect } from "@playwright/test";

test("generate a random phone number", async ({ page }) => {
  await page.goto("http://localhost:5173/");

  await page.getByRole('combobox').selectOption('mobile');
  await page.getByRole('button', { name: 'Generate' }).click();

    // Get the generated JSON
  const output = page.locator("pre");
  const jsonText = await output.textContent();

  // Convert JSON string into a JavaScript object
  const MOBILE = JSON.parse(jsonText);
  
  //get generated phone number
  expect(MOBILE.mobile_phone_number).toMatch(/^\d{8}$/);
});