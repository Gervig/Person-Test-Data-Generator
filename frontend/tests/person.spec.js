import { test, expect } from "@playwright/test";

test("generate a random person", async ({ page }) => {
  await page.goto("http://localhost:5173/");

  await page.getByRole("button", { name: "Generate" }).click();

  // Get the generated JSON
  const output = page.locator("pre");
  const jsonText = await output.textContent();

  // Convert JSON string into a JavaScript object
  const person = JSON.parse(jsonText);

  // Validate generated person
  expect(person.first_name).toBeTruthy();
  expect(person.last_name).toBeTruthy();

  expect(["male", "female"]).toContain(person.gender);

  expect(person.date_of_birth).toMatch(/^\d{4}-\d{2}-\d{2}$/);

  expect(person.cpr).toMatch(/^\d{10}$/);

  expect(person.mobile_phone_number).toMatch(/^\d{8}$/);

  // Validate address
  expect(person.address.street).toBeTruthy();
  expect(person.address.number).toBeTruthy();
  expect(person.address.postal_code.postal_code).toMatch(/^\d{4}$/);
  expect(person.address.postal_code.town_name).toBeTruthy();
});