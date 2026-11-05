import { test, expect } from "@playwright/test";

test("generate a random adress", async ({ page }) => {
  await page.goto("http://localhost:5173/");

  await page.getByRole('combobox').selectOption('address');
  await page.getByRole('button', { name: 'Generate' }).click();

    // Get the generated JSON
  const output = page.locator("pre");
  const jsonText = await output.textContent();

  // Convert JSON string into a JavaScript object
  const person = JSON.parse(jsonText);
  
  // Validate address
  expect(person.address.street).toBeTruthy();
  expect(person.address.number).toBeTruthy();
  expect(person.address.postal_code.postal_code).toMatch(/^\d{4}$/);
  expect(person.address.postal_code.town_name).toBeTruthy();
});