# FinPath: User Stories and Acceptance Criteria

The prioritized MVP backlog. Priority uses MoSCoW. Story points are relative planning estimates, not measured effort. The **Status** column states what the prototype actually does.

| ID | User story | Priority | Points | Status |
| --- | --- | --- | --- | --- |
| US-1 | As a new user, I want to set up FinPath in a few steps so I can see my plan quickly | Must | 5 | Implemented |
| US-2 | As a privacy-conscious user, I want to choose what my data is used for | Must | 3 | Implemented |
| US-3 | As a student, I want to know what's safe to spend before my next income | Must | 3 | Implemented |
| US-4 | As a user, I want to see which categories take most of my money | Must | 5 | Implemented |
| US-5 | As a user, I want to set a limit for each category | Must | 5 | Implemented |
| US-6 | As a user, I want a warning before I overspend | Must | 2 | Implemented (in-app only) |
| US-7 | As a young professional, I want to create a savings goal with a deadline | Must | 5 | Implemented |
| US-8 | As a saver, I want to log contributions and see progress | Must | 3 | Implemented |
| US-9 | As a user, I want insights that tell me what changed and why | Must | 8 | Demo logic |
| US-10 | As a user, I want clear feedback when insights can't load | Must | 2 | Implemented (simulated failure) |
| US-11 | As a user, I want to ask a quick question about my spending | Could | 5 | Demo logic |
| US-12 | As a user, I want to delete my data | Must | 2 | Implemented |
| US-13 | As a user with low vision, I want larger text | Should | 3 | Implemented |
| US-14 | As a user, I want a check-in reminder each month | Could | 3 | Concept (switch stored; nothing sent) |
| US-15 | As a user with accounts at other banks, I want them included | Won't (now) | — | Not started; depends on open banking phase one |

## Acceptance criteria

### US-1 · Set up in a few steps
- Given I open FinPath for the first time, when I enter name, life stage and income and finish the privacy step, then I land on the dashboard.
- Income must be a number from $1 to $50,000. Name allows letters, spaces, hyphens and apostrophes, up to 30 characters.
- Errors appear under the field, the first invalid field receives focus, and my other entries are kept.
- I can instead choose "Explore with sample data".

### US-2 · Choose what my data is used for
- The privacy step shows each data use as a switch with a one-line explanation.
- Spending insights start on; personalised tips and anonymous usage sharing start off (BR-6).
- Changes take effect immediately and are saved.

### US-3 · Know what's safe to spend before my next income
- Given income has been received and a deposit is still expected this month, the dashboard shows safe to spend until that payday. The amount is income received, minus spending to date, minus bills due before payday, minus this month's goal savings, rounded down (BR-1).
- The expected deposit is named and excluded.
- A per-day amount divides by the days until payday.
- If no more income is expected, the figure runs to the end of the month and sets aside all remaining bills.
- When the result is negative, it shows $0 and the shortfall.
- "How this is calculated" itemises every line and lists what is not included.

### US-4 · See which categories take most of my money
- A chart shows each category's share and amount, with names and percentages as text.
- Selecting a category, in the chart or a list, filters the transactions and daily bars and updates the chart centre. Selecting it again clears the filter.

### US-5 · Set a limit for each category
- I can edit any category limit.
- Values outside $0–$10,000, decimals and non-numbers show an error and are not saved (BR-2).
- Remaining amounts and totals update immediately.
- Quick adjustments (−20%, −10%, +10%, +20%, suggested) fill the field.
- Escape or Cancel closes without saving.

### US-6 · Warn before I overspend
- A category at 80% or more of its limit shows a warning state.
- Above 100%, it shows an over-budget state with the amount over.
- Each state uses text and an icon, not colour alone.
- Budgeting more than planned income shows a warning (BR-3).

### US-7 · Create a savings goal with a deadline
- Name: 1–30 characters, unique (case-insensitive).
- Target: $1–$1,000,000.
- Target month: November 2026 or later, within 10 years.
- Starting amount: no more than the target.
- Each invalid field shows a specific message. A live preview shows the monthly amount (BR-4).

### US-8 · Log contributions and see progress
- Amounts from $1 up to the amount left are accepted; others show an error.
- Progress and the monthly amount update immediately.
- Reaching the target marks the goal complete.
- Money added this month is set aside in safe to spend.

### US-9 · Insights that explain what changed and why
- At least 3 insight types are generated from data; the prototype has 5:
  - category change versus the same days last month;
  - budget pace;
  - subscriptions;
  - goal pace;
  - top merchant.
- Each opens "How we calculated this" with its numbers and rule.
- Insights are labelled as demo logic, not AI.

### US-10 · Clear feedback when insights can't load
- A loading state appears while analysis runs.
- On failure, an error message and a "Try again" button appear, and retry succeeds once the cause is cleared.
- In the prototype, the failure is simulated from Settings → Demo.

### US-11 · Ask a quick question
- Typed questions about a category, the month total, what's safe to spend, or goals return an answer computed from local data.
- The safe-to-spend answer matches the dashboard.
- Empty questions show an error. Unknown questions return a helpful fallback.
- Labelled as keyword matching, not a chatbot.

### US-12 · Delete my data
- "Delete all my data" requires confirmation in the page.
- Afterwards, saved data is cleared and onboarding starts fresh.

### US-13 · Larger text
- A "Larger text" switch increases type size across the app without horizontal overflow.

### US-14 · Monthly check-in reminder
- Concept only: the switch is saved, but no notification is sent.

### US-15 · Include accounts at other banks
- Out of MVP scope; depends on open banking phase one.
