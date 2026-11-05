# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: adress.spec.js >> generate a random adress
- Location: tests\adress.spec.js:3:1

# Error details

```
TypeError: Cannot read properties of undefined (reading 'street')
```

# Page snapshot

```yaml
- main [ref=e3]:
  - heading "Person Test Data Generator" [level=1] [ref=e4]
  - combobox [ref=e5]:
    - option "Person"
    - option "Persons"
    - option "CPR"
    - option "Name"
    - option "Address" [selected]
    - option "Name and birth date"
    - option "CPR and name"
    - option "CPR, name and birth date"
    - option "Mobile phone number"
  - button "Generate" [ref=e6]
  - generic [ref=e7]: "{ \"street\": \"OnMuFUycHGek\", \"number\": \"143R\", \"floor\": \"64\", \"door\": \"25\", \"postal_code\": { \"postal_code\": \"8592\", \"town_name\": \"Anholt\" } }"
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test("generate a random adress", async ({ page }) => {
  4  |   await page.goto("http://localhost:5173/");
  5  | 
  6  |   await page.getByRole('combobox').selectOption('address');
  7  |   await page.getByRole('button', { name: 'Generate' }).click();
  8  | 
  9  |     // Get the generated JSON
  10 |   const output = page.locator("pre");
  11 |   const jsonText = await output.textContent();
  12 | 
  13 |   // Convert JSON string into a JavaScript object
  14 |   const person = JSON.parse(jsonText);
  15 |   
  16 |   // Validate address
> 17 |   expect(person.address.street).toBeTruthy();
     |                         ^ TypeError: Cannot read properties of undefined (reading 'street')
  18 |   expect(person.address.number).toBeTruthy();
  19 |   expect(person.address.postal_code.postal_code).toMatch(/^\d{4}$/);
  20 |   expect(person.address.postal_code.town_name).toBeTruthy();
  21 | });
```