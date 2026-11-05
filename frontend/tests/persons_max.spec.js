import { test, expect } from "@playwright/test";

test("generate 100 persons", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");

    await page.getByRole("spinbutton").fill("100");

    await page.getByRole("button", { name: "Generate" }).click();

// Get the generated JSON
    const output = page.locator("pre");
    const jsonText = await output.textContent();

    // Convert JSON string into a JavaScript object
    const persons = JSON.parse(jsonText);

    // Validate that exactly 100 persons exist
    expect(persons).toHaveLength(100);
});