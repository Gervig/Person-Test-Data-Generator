import { test, expect } from "@playwright/test";

// 1. Generate one person and validate all fields
test("generate a random person", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");
    await page.getByRole("button", { name: "Generate" }).click();

    const output = page.locator("pre");
    const jsonText = await output.textContent();

    const result = JSON.parse(jsonText);
    const person = result.persons[0];

    expect(result.persons).toHaveLength(2);

    expect(person.first_name).toBeTruthy();
    expect(person.last_name).toBeTruthy();

    expect(person.first_name).toEqual(expect.any(String));
    expect(person.last_name).toEqual(expect.any(String));

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


// 2. Generate two persons and validate all fields
test("generate two persons and validate all fields", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");
    await page.getByRole("spinbutton").fill("02");

    await page.getByRole("button", { name: "Generate" }).click();

    const output = page.locator("pre");
    const jsonText = await output.textContent();

    const result = JSON.parse(jsonText);
    const persons = result.persons;

    expect(persons).toHaveLength(2);

    for (const person of persons) {
        expect(person.first_name).toBeTruthy();
        expect(person.last_name).toBeTruthy();

        expect(person.first_name).toEqual(expect.any(String));
        expect(person.last_name).toEqual(expect.any(String));

        expect(["male", "female"]).toContain(person.gender);

        expect(person.date_of_birth).toMatch(/^\d{4}-\d{2}-\d{2}$/);
        expect(person.cpr).toMatch(/^\d{10}$/);
        expect(person.mobile_phone_number).toMatch(/^\d{8}$/);

        // Validate address
        expect(person.address.street).toBeTruthy();
        expect(person.address.number).toBeTruthy();
        expect(person.address.postal_code.postal_code).toMatch(/^\d{4}$/);
        expect(person.address.postal_code.town_name).toBeTruthy();
    }
});


// 3. Generate 100 persons and validate count
test("generate 100 persons", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");
    await page.getByRole("spinbutton").fill("100");

    await page.getByRole("button", { name: "Generate" }).click();

    const output = page.locator("pre");
    const jsonText = await output.textContent();

    const result = JSON.parse(jsonText);

    expect(result.persons).toHaveLength(100);
});


// 4. Reject generating 1 person
test("reject generating 1 person", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");
    await page.getByRole("spinbutton").fill("1");

    // Listen for the failed API response
    const responsePromise = page.waitForResponse(response =>
        response.status() === 422
    );

    await page.getByRole("button", { name: "Generate" }).click();

    const response = await responsePromise;

    expect(response.status()).toBe(422);
});

// 5. Reject generating 101 persons
test("reject generating 101 persons", async ({ page }) => {
    await page.goto("http://localhost:5173/");

    await page.getByRole("combobox").selectOption("persons");
    await page.getByRole("spinbutton").fill("101");

    // Listen for the failed API response
    const responsePromise = page.waitForResponse(response =>
        response.status() === 422
    );

    await page.getByRole("button", { name: "Generate" }).click();

    const response = await responsePromise;

    expect(response.status()).toBe(422);
});