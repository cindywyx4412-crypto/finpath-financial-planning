# FinPath: Verified QA Report

**Result: 96 of 96 automated checks passed in both runs below.** 92 checks drive the prototype like a user; 4 call calculation functions directly.

| Run | Target | Result |
| --- | --- | --- |
| Local, clean checkout | `index.html` opened from disk, all network requests blocked | 96 / 96 passed |
| Live demo | https://majestic-sundae-6965fc.netlify.app/ (only that origin allowed) | 96 / 96 passed |

- **Date:** October 30, 2026.
- **Environment:**
  - Linux;
  - Python 3.13 with Playwright 1.63.0 (headless Chromium);
  - Node 22 with axe-core 4.10.2.
- **How the local run was made:** a fresh copy of this repository, then `npm ci`, then `python tests/qa_suite.py`.
- **Same file:** before testing, the live page was downloaded and its SHA-256 hash matched this repository's `index.html` exactly.

Reproduce with the commands in [`tests/README.md`](../tests/README.md). The committed workflow (`.github/workflows/tests.yml`) runs the same suite on GitHub Actions; it had not yet run on GitHub when this report was written.

## Checks by area

| Area | Checks |
| --- | --- |
| Validation | 16 |
| Calculations | 15 |
| Responsive | 10 |
| Accessibility | 8 |
| Goals | 6 |
| Spending | 6 |
| Insights | 6 |
| Navigation | 5 |
| Privacy | 5 |
| Empty states | 4 |
| Budget | 4 |
| Error handling | 3 |
| Standalone | 3 |
| Persistence | 2 |
| States | 1 |
| Settings | 1 |
| Stability | 1 |

## What these results do and don't show

- **They show** that the implemented features behave as specified in [business-requirements.md](business-requirements.md) and [user-stories.md](user-stories.md), on synthetic data, in Chromium.
- **Accessibility:** automated axe-core rules (WCAG 2.0–2.2 A/AA rule sets) found no violations on 6 screens and 2 open sheets. Automated rules cover only part of WCAG, so this is **not** a conformance claim.
- **Open accessibility item:** chips, toggles, segmented buttons and small buttons are below the 44 px touch-target goal in NFR-1 (they meet the WCAG 2.5.8 minimum of 24 px).
- **Not tested:**
  - usability with real people;
  - screen readers or other assistive technology;
  - real phones;
  - browsers other than Chromium (Safari, Firefox);
  - performance timings (NFR-4);
  - security review.

## Defects found and fixed during QA

| # | Defect | Fix |
| --- | --- | --- |
| 1 | Escape stopped closing a sheet after a quick-adjust chip was tapped, because focus left the phone frame | Escape works wherever focus is; focus returns to the sheet after re-renders |
| 2 | Progress bars had no accessible name (axe: aria-progressbar-name, serious) | Each bar names what it measures |
| 3 | Content behind an open sheet was still exposed to assistive technology | Background is inert and hidden from screen readers while a sheet or dialog is open |
| 4 | The screen board overflowed at 360 px | Frames shrink to the screen width |
| 5 | The top insight could report a 100% drop to $0 (accurate but not useful) | The rule prefers increases of 10% or more |
| 6 | The calculation sheet's scrollable area could not be reached by keyboard (axe: scrollable-region-focusable) | The scroll area is focusable and labelled |

A seventh change was a business-logic correction rather than a code defect: Version 2 revised BR-1, the safe-to-spend rule. See [business-requirements.md](business-requirements.md#why-br-1-changed-in-version-2).

## All checks

| # | Area | Check | Kind | Local | Live |
| --- | --- | --- | --- | --- | --- |
| 1 | Navigation | Fresh start opens Welcome | UI | Pass | Pass |
| 2 | Validation | Onboarding: empty name and income show errors | UI | Pass | Pass |
| 3 | Accessibility | Invalid field marked aria-invalid and focused | UI | Pass | Pass |
| 4 | Validation | Onboarding: non-numeric income rejected | UI | Pass | Pass |
| 5 | Validation | Onboarding: valid name kept after another field fails | UI | Pass | Pass |
| 6 | Validation | Onboarding: income above $50,000 rejected | UI | Pass | Pass |
| 7 | Navigation | Valid profile advances to privacy step | UI | Pass | Pass |
| 8 | Privacy | Optional data uses default to off (BR-6) | UI | Pass | Pass |
| 9 | Navigation | Finish setup lands on dashboard | UI | Pass | Pass |
| 10 | Calculations | Safe to spend = income received − spent − bills due before payday (no goals) | UI | Pass | Pass |
| 11 | Calculations | Per-day amount = floor(safe ÷ days until payday) | UI | Pass | Pass |
| 12 | Calculations | Income not yet received is shown as not counted | UI | Pass | Pass |
| 13 | Calculations | Unpaid bills listed with due dates and set aside | UI | Pass | Pass |
| 14 | Calculations | Calculation sheet itemises bills, shows exclusions, and its total matches the dashboard | UI | Pass | Pass |
| 15 | Empty states | New user sees create-budget and set-goal prompts | UI | Pass | Pass |
| 16 | Empty states | Budget empty state shown | UI | Pass | Pass |
| 17 | Budget | Suggested limits applied from September spending | UI | Pass | Pass |
| 18 | Accessibility | Edit sheet moves focus to the limit field | UI | Pass | Pass |
| 19 | Validation | Budget limit "-50" rejected | UI | Pass | Pass |
| 20 | Validation | Budget limit "12.5" rejected | UI | Pass | Pass |
| 21 | Validation | Budget limit "20000" rejected | UI | Pass | Pass |
| 22 | Validation | Budget limit "" rejected | UI | Pass | Pass |
| 23 | Budget | Enter key saves a valid limit | UI | Pass | Pass |
| 24 | Calculations | Remaining = limit − spent, shown on the row | UI | Pass | Pass |
| 25 | Budget | +10% quick adjust updates the field | UI | Pass | Pass |
| 26 | Accessibility | Escape closes the sheet without saving | UI | Pass | Pass |
| 27 | Calculations | Budget states: <80% ok, ≥80% warn, =100% warn, >100% over | Function | Pass | Pass |
| 28 | Budget | Budgeting more than income shows a warning (BR-3) | UI | Pass | Pass |
| 29 | Empty states | Goals empty state shown | UI | Pass | Pass |
| 30 | Validation | Goal: empty name and target rejected | UI | Pass | Pass |
| 31 | Validation | Goal: saved more than target rejected | UI | Pass | Pass |
| 32 | Validation | Goal: past target month rejected | UI | Pass | Pass |
| 33 | Calculations | Live preview: ceil((1400−200) ÷ 6 months) = $200 | UI | Pass | Pass |
| 34 | Goals | Valid goal is created and saved | UI | Pass | Pass |
| 35 | Calculations | Goal card shows monthly target (BR-4) | UI | Pass | Pass |
| 36 | Validation | Goal: duplicate name rejected (case-insensitive) | UI | Pass | Pass |
| 37 | Validation | Contribution "0" rejected | UI | Pass | Pass |
| 38 | Validation | Contribution "5000" rejected | UI | Pass | Pass |
| 39 | Goals | Contribution adds to saved amount | UI | Pass | Pass |
| 40 | Calculations | Monthly target recalculates after contribution: ceil(1150 ÷ 6) = 192 | Function | Pass | Pass |
| 41 | Calculations | Goal savings reserve = month plan ($200) when less has been added ($50) | Function | Pass | Pass |
| 42 | Calculations | Money added beyond the plan ($1,200) is reserved instead of the plan | Function | Pass | Pass |
| 43 | Goals | Reaching the target marks the goal done | UI | Pass | Pass |
| 44 | Goals | Delete asks for confirmation | UI | Pass | Pass |
| 45 | Goals | Cancel keeps the goal | UI | Pass | Pass |
| 46 | Goals | Confirm deletes the goal | UI | Pass | Pass |
| 47 | Spending | Selecting a category filters transactions | UI | Pass | Pass |
| 48 | Spending | Donut centre shows selected category | UI | Pass | Pass |
| 49 | Spending | Tapping a bar shows that day's amount | UI | Pass | Pass |
| 50 | Spending | Selecting again clears the filter | UI | Pass | Pass |
| 51 | Empty states | Search with no match shows empty state | UI | Pass | Pass |
| 52 | Accessibility | Search keeps focus while typing | UI | Pass | Pass |
| 53 | Spending | Search matches merchant names case-insensitively | UI | Pass | Pass |
| 54 | Spending | Week toggle switches the period | UI | Pass | Pass |
| 55 | Calculations | Category amounts sum to the period total | UI | Pass | Pass |
| 56 | States | Insights show a loading skeleton first | UI | Pass | Pass |
| 57 | Insights | At least 4 insight cards generated from data | UI | Pass | Pass |
| 58 | Insights | Insights are labelled as demo logic, not AI | UI | Pass | Pass |
| 59 | Insights | "How we calculated this" shows numbers and rule | UI | Pass | Pass |
| 60 | Validation | Ask: empty question shows an error | UI | Pass | Pass |
| 61 | Insights | Ask: category question answered from data | UI | Pass | Pass |
| 62 | Insights | Ask: safe-to-spend answer matches the dashboard figure and names what is set aside | UI | Pass | Pass |
| 63 | Insights | Usefulness feedback is stored | UI | Pass | Pass |
| 64 | Error handling | Simulated failure shows error state with retry | UI | Pass | Pass |
| 65 | Error handling | Ask FinPath reports the failure instead of answering | UI | Pass | Pass |
| 66 | Error handling | After the cause is cleared, insights load again | UI | Pass | Pass |
| 67 | Privacy | Turning off insights hides analysis and explains why | UI | Pass | Pass |
| 68 | Privacy | Turning insights back on restores them | UI | Pass | Pass |
| 69 | Validation | Settings: blank income rejected | UI | Pass | Pass |
| 70 | Settings | Profile saves valid income | UI | Pass | Pass |
| 71 | Accessibility | Larger text setting enlarges type | UI | Pass | Pass |
| 72 | Responsive | Larger text causes no horizontal overflow in Settings | UI | Pass | Pass |
| 73 | Persistence | Data survives a page reload | UI | Pass | Pass |
| 74 | Persistence | Reset demo restores the sample user | UI | Pass | Pass |
| 75 | Privacy | Delete all data asks for confirmation (BR-7) | UI | Pass | Pass |
| 76 | Privacy | Delete clears storage and restarts onboarding | UI | Pass | Pass |
| 77 | Calculations | Over plan: safe to spend floors at $0 and explains why | UI | Pass | Pass |
| 78 | Calculations | No income still expected: horizon is rest of month and all remaining bills are set aside | UI | Pass | Pass |
| 79 | Navigation | All five tabs reachable and render | UI | Pass | Pass |
| 80 | Navigation | Settings back returns to the previous tab | UI | Pass | Pass |
| 81 | Accessibility | axe-core 4.10 scan (WCAG 2.0–2.2 A/AA rule sets) of 6 screens: no violations | UI | Pass | Pass |
| 82 | Accessibility | axe-core scan of two open sheets (budget edit, safe-to-spend detail): no violations | UI | Pass | Pass |
| 83 | Accessibility | All buttons and inputs on 6 screens at least 24×24 px (WCAG 2.5.8 minimum) | UI | Pass | Pass |
| 84 | Responsive | 360 px phone: no horizontal page scroll | UI | Pass | Pass |
| 85 | Responsive | 360 px: #screens view has no horizontal page scroll | UI | Pass | Pass |
| 86 | Responsive | 360 px: #system view has no horizontal page scroll | UI | Pass | Pass |
| 87 | Responsive | 360 px: #handoff view has no horizontal page scroll | UI | Pass | Pass |
| 88 | Responsive | Tablet 820 px: prototype view stacks without overflow | UI | Pass | Pass |
| 89 | Responsive | Desktop 1440 px: #prototype view has no horizontal page scroll | UI | Pass | Pass |
| 90 | Responsive | Desktop 1440 px: #screens view has no horizontal page scroll | UI | Pass | Pass |
| 91 | Responsive | Desktop 1440 px: #system view has no horizontal page scroll | UI | Pass | Pass |
| 92 | Responsive | Desktop 1440 px: #handoff view has no horizontal page scroll | UI | Pass | Pass |
| 93 | Standalone | Embedded fonts load with no network (Manrope, IBM Plex Mono) | UI | Pass | Pass |
| 94 | Standalone | Embedded flow diagram renders | UI | Pass | Pass |
| 95 | Standalone | Zero external network requests attempted | UI | Pass | Pass |
| 96 | Stability | No console or page errors during the run | UI | Pass | Pass |
