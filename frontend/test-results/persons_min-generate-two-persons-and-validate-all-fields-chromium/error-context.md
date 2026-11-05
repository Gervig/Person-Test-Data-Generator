# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: persons_min.spec.js >> generate two persons and validate all fields
- Location: tests\persons_min.spec.js:3:1

# Error details

```
TypeError: expect(received).toHaveLength(expected)

Matcher error: received value must have a length property whose value must be a number

Received has type:  object
Received has value: {"persons": [{"address": {"door": "42", "floor": "58", "number": "812K", "postal_code": {"postal_code": "8444", "town_name": "Balle"}, "street": "TYYxoAmO"}, "cpr": "2504470054", "date_of_birth": "1947-04-25", "first_name": "Alberte J.", "gender": "female", "last_name": "Sørensen", "mobile_phone_number": "47842561"}, {"address": {"door": "30", "floor": "31", "number": "436", "postal_code": {"postal_code": "4592", "town_name": "Sejerø"}, "street": "nUIzSFQLN"}, "cpr": "3007476695", "date_of_birth": "1947-07-30", "first_name": "Johan S.", "gender": "male", "last_name": "Henriksen", "mobile_phone_number": "34669197"}]}
```

# Page snapshot

```yaml
- main [ref=e3]:
  - heading "Person Test Data Generator" [level=1] [ref=e4]
  - combobox [ref=e5]:
    - option "Person"
    - option "Persons" [selected]
    - option "CPR"
    - option "Name"
    - option "Address"
    - option "Name and birth date"
    - option "CPR and name"
    - option "CPR, name and birth date"
    - option "Mobile phone number"
  - spinbutton [ref=e6]: "02"
  - button "Generate" [ref=e7]
  - generic [ref=e8]: "{ \"persons\": [ { \"first_name\": \"Alberte J.\", \"last_name\": \"Sørensen\", \"gender\": \"female\", \"date_of_birth\": \"1947-04-25\", \"cpr\": \"2504470054\", \"mobile_phone_number\": \"47842561\", \"address\": { \"street\": \"TYYxoAmO\", \"number\": \"812K\", \"floor\": \"58\", \"door\": \"42\", \"postal_code\": { \"postal_code\": \"8444\", \"town_name\": \"Balle\" } } }, { \"first_name\": \"Johan S.\", \"last_name\": \"Henriksen\", \"gender\": \"male\", \"date_of_birth\": \"1947-07-30\", \"cpr\": \"3007476695\", \"mobile_phone_number\": \"34669197\", \"address\": { \"street\": \"nUIzSFQLN\", \"number\": \"436\", \"floor\": \"31\", \"door\": \"30\", \"postal_code\": { \"postal_code\": \"4592\", \"town_name\": \"Sejerø\" } } } ] }"
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test("generate two persons and validate all fields", async ({ page }) => {
  4  |     await page.goto("http://localhost:5173/");
  5  | 
  6  |     await page.getByRole("combobox").selectOption("persons");
  7  | 
  8  |     await page.getByRole("spinbutton").fill("02");
  9  | 
  10 |     await page.getByRole("button", { name: "Generate" }).click();
  11 | 
  12 |     // Get the generated JSON
  13 |     const output = page.locator("pre");
  14 |     const jsonText = await output.textContent();
  15 | 
  16 |     // Convert JSON string into a JavaScript object
  17 |     const persons = JSON.parse(jsonText);
  18 | 
  19 |     // Check that exactly two persons were generated
> 20 |     expect(persons).toHaveLength(2);
     |                     ^ TypeError: expect(received).toHaveLength(expected)
  21 | 
  22 |     // Validate every person
  23 |     for (const person of persons) {
  24 | 
  25 |         expect(person.first_name).toBeTruthy();
  26 |         expect(person.last_name).toBeTruthy();
  27 | 
  28 |         expect(["male", "female"]).toContain(person.gender);
  29 | 
  30 |         expect(person.date_of_birth).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  31 | 
  32 |         expect(person.cpr).toMatch(/^\d{10}$/);
  33 | 
  34 |         expect(person.mobile_phone_number).toMatch(/^\d{8}$/);
  35 | 
  36 |         // Validate address
  37 |         expect(person.address.street).toBeTruthy();
  38 |         expect(person.address.number).toBeTruthy();
  39 |         expect(person.address.postal_code.postal_code).toMatch(/^\d{4}$/);
  40 |         expect(person.address.postal_code.town_name).toBeTruthy();
  41 |     }
  42 | });
```