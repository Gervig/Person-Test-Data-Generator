# Personal Test Data Generator

## 1. Assignment Overview

Design and implement **unit, integration, API, and end-to-end tests** for an application that generates fake personal data for testing other applications.

The assignment must be completed in groups of **4 or 5 students**.

If exceptional circumstances prevent you from working in a group, request a dispensation from the Head of Education, Marc Kluge, at [klu@ek.dk](mailto:klu@ek.dk).

Please form your groups and enter your names in the Excel file **Groups - First Mandatory Assignment.xlsx**, available in Microsoft Teams.

## 2. System Under Test

The application generates fake information for non-existing Danish persons and consists of two main components:

- **Backend:** Provides the requested information through an API.
- **Frontend:** A graphical user interface (GUI) that consumes the API.

The backend must expose a series of functions or a class with public methods that generate the information described below.

### 2.1. Name and Gender

Name and gender are treated as compound information consisting of:

- First name
- Last name
- Gender

Names and gender must be randomly selected from the provided `person-names.json` file.

### 2.2. CPR Number

A CPR number must consist of exactly **10 numeric digits**.

- The first six digits identify the date of birth in the format `ddMMyy`.
- The last four digits are randomly generated.
- For female persons, the final digit must be even.
- For male persons, the final digit must be odd.

### 2.3. Date of Birth

The date of birth must match the date encoded in the CPR number.

### 2.4. Address

An address consists of the following components:

| Component | Requirements |
|---|---|
| Street | A random assortment of alphabetic characters |
| Number | A number from 1 to 999, optionally followed by an uppercase letter, e.g. `43B` |
| Floor | Either `st` or a number from 1 to 99 |
| Door | `th`, `mf`, `tv`, a number from 1 to 50, or a lowercase letter optionally followed by a dash and then one to three numeric digits, e.g. `c3` or `d-14` |
| Postal code and town | Randomly selected from the provided `addresses.sql` database |

For more information, see [Danish address rules and guidance](https://danmarksadresser.dk/regler-og-vejledning/adresser).

### 2.5. Mobile Phone Number

A mobile phone number must satisfy the following requirements:

- Consist of exactly **8 numeric digits**.
- Start with one of the permitted prefixes listed below.

#### Permitted prefixes

| Prefix length | Allowed prefixes |
|---|---|
| 1 digit | `2` |
| 2 digits | `30`, `31`, `40`, `41`, `42`, `50`, `51`, `52`, `53`, `60`, `61`, `71`, `81`, `91`, `92`, `93` |
| 3 digits | `342`, `344–349`, `356–357`, `359`, `362`, `365–366`, `389`, `398`, `431`, `441`, `462`, `466`, `468`, `472`, `474`, `476`, `478`, `485–486`, `488–489`, `493–496`, `498–499`, `542–543`, `545`, `551–552`, `556`, `571–574`, `577`, `579`, `584`, `586–587`, `589`, `597–598`, `627`, `629`, `641`, `649`, `658`, `662–665`, `667`, `692–694`, `697`, `771–772`, `782–783`, `785–786`, `788–789`, `826–827`, `829` |

For more information, see the [Danish numbering plan guidance (2025)](https://digst.dk/media/4knkrjpk/nummervejledning-2025.pdf).

### 2.6. Functional Requirements

The backend must provide **one function or method and one corresponding API endpoint** for each of the following functionalities:

1. Return a fake CPR number.
2. Return a fake first name, last name, and gender.
3. Return a fake first name, last name, gender, and date of birth.
4. Return a fake CPR number, first name, last name, and gender.
5. Return a fake CPR number, first name, last name, gender, and date of birth.
6. Return a fake address.
7. Return a fake mobile phone number.
8. Return all information for a fake person:
   - CPR number
   - First name
   - Last name
   - Gender
   - Date of birth
   - Address
   - Mobile phone number
9. Return fake person information in bulk, generating all information for **2 to 100 persons**.

### API endpoints

The backend exposes the required functionality through these `GET` endpoints:

| Endpoint | Response |
|---|---|
| `/cpr` | A fake CPR number |
| `/name` | First name, last name, and gender |
| `/name-and-birth-date` | Name and gender plus date of birth |
| `/cpr-and-name` | CPR number, name, and gender |
| `/cpr-name-and-birth-date` | CPR number, name, gender, and date of birth |
| `/address` | A fake address |
| `/mobile-phone-number` | A fake Danish mobile phone number |
| `/person` | All information for one fake person |
| `/persons?count=2` through `/persons?count=100` | The requested number of complete fake persons |
| `/postal-codes` | Postal codes loaded from the address database |

### 2.7. Implementation Choices

The group may choose:

- Programming language(s) and framework(s).
- API format, e.g. REST.
- Database technology. If a database other than MySQL/MariaDB is selected, a data migration is required.
- Output format for functions, methods, and API responses, e.g. JSON, XML, CSV, formatted text, or standard output.

### 2.8. Reference Implementations

You may use the following existing application code directly or as inspiration:

- **Backend:** [fake_info — MariaDB / PHP 8, Dockerized](https://github.com/arturomorarioja/fake_info/)
- **Frontend:** [js_fake_info_frontend — JavaScript / CSS3 / HTML5](https://github.com/arturomorarioja/js_fake_info_frontend)

## 3. Testing Requirements

### 3.1. Unit and Integration Testing

- Write unit tests wherever appropriate.
- Write integration tests wherever appropriate.

### 3.2. API Testing

- Implement API tests.
- Provide test scripts using Postman, Insomnia, Thunder Client, or a similar tool.

### 3.3. Test Case Design

Design test cases using all three of the following approaches:

- **Black-box testing:** Manual analysis of the application's requirements and behaviour.
- **White-box testing:** Automated analysis based on the application's internal structure and code.
- **Experience-based testing:** Identify edge cases, business-logic-derived cases, and other interesting scenarios.

### 3.4. Static Code Analysis

- Use static code analysis tools beyond basic linters to analyse and improve the code.
- Include a code coverage tool if the chosen unit testing framework does not already provide coverage.

### 3.5. Continuous Integration and Testing

- Create a continuous integration (CI) job or pipeline that tests the integration of the application.
- Configure the CI process to run all of the following:
  - Unit tests
  - Integration tests
  - API tests
  - Static code analysis

### 3.6. End-to-End Testing

- Design and implement end-to-end tests using Selenium WebDriver, Cypress, Playwright, or a similar framework.
- **Selenium IDE is not permitted.**

## 4. Delivery Requirements

Submit the assignment through Itslearning as **one ZIP file**.

**Deadline: 19 October 2026 at 23:59.**

The ZIP file must contain:

1. **Application source code**, if different from the provided reference implementation.
2. **Database creation and population script**, if different from the provided script.
3. **Test source code**, including:
   - Unit tests
   - Integration tests
   - End-to-end tests
4. **CI configuration files**, such as YAML, XML, or another format used by the selected CI tool. A screenshot is also acceptable.
5. **A PDF documenting black-box test design techniques**, including relevant techniques such as:
   - Valid and invalid equivalence partitions
   - Boundary value analysis
   - Decision tables, where applicable
6. **Screenshots of static testing tools** demonstrating the value they contributed to the testing activities.

## 5. Presentation

Each group must present its work to the rest of the class on **20 October 2026**.

The presentation is limited to **10 minutes per group**, and **all group members must present a part**.

### 5.1. Required Presentation Content

The presentation must demonstrate and explain:

1. The application running.
2. The application source code.
3. The unit, integration, and end-to-end test code. The end-to-end tests must be executed during the presentation.
4. The API test scripts in Postman or a similar tool.
5. The criteria used to design test cases:
   - Black-box testing techniques
   - White-box testing techniques
6. The value provided by static testing tools, including code coverage where appropriate.
7. The CI job or pipeline:
   - Walkthrough of the configuration.
   - Demonstration of the pipeline running.

### 5.2. Presentation Checklist

- [ ] Demonstrate the application.
- [ ] Explain the application code.
- [ ] Show unit and integration tests.
- [ ] Run the end-to-end tests.
- [ ] Demonstrate the API tests.
- [ ] Explain black-box and white-box test design.
- [ ] Demonstrate the static analysis tools.
- [ ] Walk through and run the CI pipeline.
- [ ] Ensure every group member presents a part.

## 6. Important Dates

| Event | Date |
|---|---|
| Assignment submission deadline | **19 October 2026, 23:59** |
| Group presentations | **20 October 2026** |

## 7. Final Notes

The goal is not only to build a working fake personal data generator, but also to demonstrate a structured and comprehensive testing process covering the application's individual components, integrations, API, and user interface.

Ensure that all required tests, analysis tools, CI configuration, documentation, and presentation materials are included in the final delivery.
