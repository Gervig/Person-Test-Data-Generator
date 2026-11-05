import { test, expect } from "@playwright/test";

test("generate a random persons CPR, name and birthdate", async ({ page }) => {
  await page.goto("http://localhost:5173/");

  await page.getByRole('combobox').selectOption('cprNameAndBirthDate');
  await page.getByRole('button', { name: 'Generate' }).click();

    // Get the generated JSON
  const output = page.locator("pre");
  const jsonText = await output.textContent();

  // Convert JSON string into a JavaScript object
  const person = JSON.parse(jsonText);

  // Validate generated person
  expect(person.first_name).toBeTruthy();
  expect(person.last_name).toBeTruthy();

  expect(["male", "female"]).toContain(person.gender);

  //validate generated cpr number
  expect(person.cpr).toMatch(/^\d{10}$/);

  //validate generated birthdate
  expect(person.date_of_birth).toMatch(/^\d{4}-\d{2}-\d{2}$/);
});