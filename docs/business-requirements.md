# FinPath: Business Requirements Document

The business requirements for a FinPath MVP pilot, with the implementation status of each requirement in the current prototype. User stories and acceptance criteria are in [user-stories.md](user-stories.md).

**Status key**
- **Implemented:** works in the prototype and is covered by the automated test suite.
- **Partial:** part of the requirement is met; the gap is stated.
- **Demo logic:** works on synthetic data using fixed rules, not a production approach.
- **Concept:** designed or stored only.
- **Not started**

## 1. Purpose

Define what FinPath must achieve for the business and its users in an MVP pilot inside an existing, authenticated banking app.

## 2. Business objectives

All targets are proposed for a pilot and must be confirmed with stakeholders.

| # | Objective | Measure | Proposed target |
| --- | --- | --- | --- |
| 1 | Raise financial confidence among pilot users aged 18–30 | Change in self-reported confidence (1–5) after 60 days | +0.5 |
| 2 | Help new users set up a plan quickly | Share of new users with ≥1 budget and ≥1 goal in the first session | 40% |
| 3 | Build habitual engagement with digital banking | Share of pilot users active in month 2 | 50% |
| 4 | Maintain trust | Insight opt-in rate; privacy-related complaints | 75% opt-in |

## 3. Scope

| In scope (MVP) | Out of scope (MVP) |
| --- | --- |
| Onboarding with life stage, income and privacy choices | Moving money, payments or automatic transfers |
| Dashboard with safe to spend and budget health | Investment, credit or tax advice |
| Spending breakdown by category and over time | Accounts at other institutions (possible after open banking phase one) |
| Category budgets with editable limits | Free-text chat on a live language model |
| Savings goals with contributions and monthly amounts | |
| Insights generated from spending, each with an explanation | |
| Settings, privacy controls and data deletion | |

## 4. Business rules

| ID | Rule | Status |
| --- | --- | --- |
| BR-1 | **Revised in Version 2.** Safe to spend = income already received this month − spending to date − bills still due before the next expected income − this month's goal savings. Goal savings for a goal are the BR-4 amount as of the start of the month, or what was already added this month if that is more. Expected income is not counted until it arrives. Rounded down to the dollar; shown as $0 with the shortfall when negative. The daily amount divides by the days until payday, or the days left in the month if no more income is expected. | Implemented |
| BR-2 | A budget limit is a whole-dollar amount from $0 to $10,000 per category. | Implemented |
| BR-3 | Budgeting more than planned monthly income triggers a warning; it does not block saving. | Implemented |
| BR-4 | Goal monthly amount = (target − saved) ÷ months from the current month up to the target month, rounded up to the dollar; at least 1 month. | Implemented |
| BR-5 | Insights educate and nudge. They never recommend specific financial products or investments. | Content rule, met by the current wording; not enforced in code |
| BR-6 | Optional data uses (personalised tips, analytics sharing) are off until the user turns them on. | Implemented; in the prototype these two switches are stored but have no effect |
| BR-7 | The user can delete all FinPath data at any time, after a confirmation step. | Implemented |

### Why BR-1 changed in Version 2

The original rule was monthly income − spending − goal plan. It counted income that had not arrived yet and ignored bills still due. For the original sample user it showed $405 safe to spend; the corrected rule gives $0 for the same data. The revised rule is deliberately conservative, and the app itemises it on the "How this is calculated" sheet, including what is excluded:
- expected income;
- bills due after the next income;
- money carried over from earlier months.

## 5. Functional requirements

| ID | Requirement | Feature | Priority | Status |
| --- | --- | --- | --- | --- |
| FR-1 | Collect first name, life stage and monthly income during onboarding, with inline validation | Onboarding | Must | Implemented (life stage is stored but does not change the experience yet) |
| FR-2 | Show privacy choices before any analysis starts; optional uses default to off | Onboarding, Settings | Must | Implemented |
| FR-3 | Show safe to spend until the next expected income (or month end), an itemised breakdown, bills still due with dates, what is excluded, and a per-day amount | Dashboard | Must | Implemented |
| FR-4 | Show spending by category as a chart; selecting a category filters the transaction list | Spending | Must | Implemented |
| FR-5 | Show spending by day for the current month or week | Spending | Should | Implemented |
| FR-6 | Search transactions by merchant name; show an empty state when nothing matches | Spending | Should | Implemented |
| FR-7 | Create and edit category budget limits; recalculate remaining amounts immediately | Budget | Must | Implemented |
| FR-8 | Flag categories at 80% or more of their limit (warning) and over 100% (over budget) | Budget, Dashboard | Must | Implemented |
| FR-9 | Create a savings goal with name, target amount, target month and starting amount; validate each field | Goals | Must | Implemented |
| FR-10 | Add contributions to a goal; show progress, amount left and monthly amount (BR-4); mark goals complete | Goals | Must | Implemented (contributions are logged; no money moves) |
| FR-11 | Delete a goal after an in-page confirmation | Goals | Should | Implemented |
| FR-12 | Generate insight cards from spending data, each with a plain-language explanation of how it was calculated | Insights | Must | Demo logic (5 fixed rules) |
| FR-13 | Show loading and error states for insights, with a retry action | Insights | Must | Implemented (delay and connection error are simulated) |
| FR-14 | Answer a small set of questions about spending from local data | Insights | Could | Demo logic (keyword matching, not AI) |
| FR-15 | Let users edit profile and income, change privacy switches, increase text size, and delete all data | Settings | Must | Implemented |
| FR-16 | Save the user's demo data on the device between sessions; provide a reset | All | Must (prototype) | Implemented (browser localStorage) |

## 6. Non-functional requirements

| ID | Category | Requirement | Status |
| --- | --- | --- | --- |
| NFR-1 | Accessibility | Meet WCAG 2.2 AA: 4.5:1 text contrast, visible focus, 44×44 px touch targets, labels on every control, no information by colour alone | **Partial.** An automated axe-core scan finds 0 violations on 6 screens and 2 sheets, and all controls are ≥ 24 px (WCAG 2.5.8 minimum). Chips, toggles and small buttons are below the 44 px target. Not tested with a screen reader. |
| NFR-2 | Privacy | Collect the minimum data; explain each use in plain language at the point of choice; deletion within the app | Implemented in the prototype (no real data is collected) |
| NFR-3 | Security | Production: runs inside the bank's authenticated session; FinPath stores no credentials. Prototype: synthetic data only | Prototype: synthetic data only, no login, no network requests. Production security not reviewed. |
| NFR-4 | Performance | Screens respond to input within 100 ms; insights show a loading state if they take longer than 300 ms | Loading state implemented; response times not measured |
| NFR-5 | Explainability | Every insight shows its data and rule; no unexplained scores | Implemented for insights and safe to spend |
| NFR-6 | Responsiveness | Layout works from 360 px to 430 px phones and on desktop | Tested at 360 px, 820 px and 1440 px |
| NFR-7 | Reliability | Errors never lose user-entered data; failed actions can be retried | Partial: validation keeps entries; insights can be retried |
| NFR-8 | Language | Plain language at about grade 8 reading level; English first, French before launch | English only; reading level not measured |

## 7. Constraints and dependencies

- **Constraint:** a pilot must run inside an existing authenticated banking app. FinPath collects no new data beyond what the bank already holds, plus the goals and budgets users enter.
- **Dependencies:**
  - a transaction categorisation service;
  - a bill and income schedule (could reuse NOMI Forecast predictions);
  - a notification service;
  - a privacy impact assessment;
  - an accessibility audit.
