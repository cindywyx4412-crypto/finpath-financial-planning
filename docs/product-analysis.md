# FinPath: Product Analysis

Problem framing, users, stakeholders, competitive analysis, journey and success measures for FinPath, an independent product concept. This document matches the [Case Study, Version 2](case-study/FinPath_Case_Study_Version_2.pdf) (October 30, 2026).

> **How to read this document.** Each claim is one of four kinds:
> - **Fact:** taken from a cited public source.
> - **Assumption:** not yet validated with real users; carries an ID (A-1 to A-10).
> - **Proposed:** a target for a future pilot, not a measured result.
> - **Implemented:** works in the prototype and is covered by the automated test suite.
>
> No interviews, surveys or usability tests have been run. All prototype data is synthetic.

## Contents

1. [Problem statement](#1-problem-statement)
2. [Public evidence](#2-public-evidence)
3. [Opportunity assessment](#3-opportunity-assessment)
4. [Assumptions register](#4-assumptions-register)
5. [Target users](#5-target-users)
6. [Value proposition](#6-value-proposition)
7. [Stakeholder analysis](#7-stakeholder-analysis)
8. [Competitive analysis: RBC NOMI](#8-competitive-analysis-rbc-nomi)
9. [User journey and service blueprint](#9-user-journey-and-service-blueprint)
10. [Business case](#10-business-case)
11. [Success metrics](#11-success-metrics)
12. [MVP scope](#12-mvp-scope)
13. [Sources](#13-sources)

## 1. Problem statement

Canadian students and early-career workers can see their transactions in a banking app, but they struggle to turn that record into a plan. They still have to work out what they can safely spend before the next deposit, whether a budget is realistic, and how to make steady progress toward a goal. This plausibly contributes to the low confidence and frequent stress in the survey data below. Whether FinPath's approach reduces it is the central hypothesis to test.

## 2. Public evidence

| Fact | Source |
| --- | --- |
| 37% of Gen Z Canadians said they feel in control of their money. | TD Bank Group / Edelman DXI, Harris Poll Omni, fielded July 28–29, 2025; n = 3,037 Canadians, about 500 aged 18–28 [1] |
| 64% of Gen Z reported financial stress several times a week, the highest of any generation. | Same survey [1] |
| 20% of Gen Z said they don't know where to start managing their money; 47% named cost of living as their biggest obstacle. | Same survey [1] |
| Mint, a free budgeting app with about 3.6 million active users in 2021, closed on January 1, 2024. | CNBC, Nov 7, 2023 [2] |
| Canada's Consumer-Driven Banking Act received royal assent in March 2026. Draft regulations published June 27, 2026 set up phase-one, read-only data sharing through accredited providers, supervised by the Bank of Canada. No consumer launch date is set. | Canada Gazette, Part I [3] |

## 3. Opportunity assessment

| Factor | Assessment |
| --- | --- |
| Need | Strong public signal on stress and low confidence. Student-specific needs, such as irregular income, are assumptions (A-1, A-5). |
| Existing tools | RBC NOMI already covers spending insights, suggested budgets, a 7-day payment forecast and automated saving (section 8). FinPath has to add to these, not repeat them. |
| Timing | Open banking read access could later let users include accounts from other institutions. The MVP does not depend on it. |
| Risk | Privacy expectations, explainability, and the line between education and advice. |

## 4. Assumptions register

Ordered by risk. None has been validated.

| ID | Assumption | Risk if wrong | How to validate |
| --- | --- | --- | --- |
| A-1 | Students and early-career users want guidance on what to do next, not only a record of what they spent | High: core value proposition fails | 8–10 problem interviews; fake-door test of an insight card |
| A-2 | Users will trust a bank-built tool with spending analysis if data use is explained in plain language | High: low opt-in to insights | Concept test of the privacy screen; opt-in rate in pilot |
| A-3 | A "safe to spend" number is easier to act on than a full budget table | High: dashboard design changes | A/B test two dashboard variants (task: "Can I afford this?") |
| A-4 | Goal-based saving (named goals with dates) motivates more than generic saving prompts | Medium | Compare goal creation and contribution rates in pilot |
| A-5 | Irregular income (part-time work, co-op, student aid) makes fixed monthly budgets break for students | Medium: budgeting model needs flexible periods | Diary study across one term |
| A-6 | Rule-based insights are useful enough for an MVP before any ML model is built | Medium | Rate the usefulness of each insight card in testing (1–5) |
| A-7 | Users will set up a budget in under 3 minutes if categories are pre-filled from spending | Medium | Timed task in moderated usability test |
| A-8 | Students prefer category limits they can adjust over a strict 50/30/20 template | Low | Card sort or preference test |
| A-9 | A monthly check-in notification increases return visits without feeling intrusive | Low | Opt-in rate and 30-day retention in pilot |
| A-10 | Young users would discover FinPath inside an existing banking app rather than as a separate download | Medium: affects go-to-market | Interviews with digital channel owners |

## 5. Target users

Proto-personas are **assumption-based**. Names and details are illustrative, written to make assumptions testable, not drawn from interviews.

| Segment | Proto-persona | Situation | Job to be done | Key assumptions |
| --- | --- | --- | --- | --- |
| University student | Maya, 20, third-year student in Toronto | Part-time job plus term-based student aid; shares rent with roommates | "Make my money last until the next deposit." | A-1, A-5, A-8 |
| New graduate | Jordan, 23, first full-time role | Steady salary for the first time; student loan repayment starting | "Set up a budget that sticks and start an emergency fund." | A-3, A-4, A-7 |
| Young professional | Priya, 27, saving for a down payment | Higher income, more fixed costs, competing goals | "See if I'm on track without building spreadsheets." | A-4, A-9 |

Life stage is captured during onboarding but does not yet change the prototype experience.

## 6. Value proposition

> For Canadian students and young professionals, FinPath turns transactions into one conservative **safe-to-spend** figure, a **budget** they can adjust in minutes, and **goals** with a monthly amount. Every insight shows its numbers and rule.

| Customer job | Pain | FinPath response | Status |
| --- | --- | --- | --- |
| Know what I can spend | A balance ignores upcoming bills, goals and when income arrives | Safe to spend counts only income received, then subtracts spending, bills due before the next income and this month's goal savings | Implemented |
| See where money goes | Transaction lists are hard to read | Category chart that filters the transaction list and daily bars | Implemented |
| Build a budget | Blank templates feel like homework | Limits pre-filled from last month, editable in one step | Implemented |
| Save for something | Saving feels abstract | Named goals with a target month and monthly amount | Implemented |
| Know what to change | Generic tips | Insights that show their numbers and rule | Implemented (rule-based demo logic) |
| Feel safe | Unclear data use | One switch per data use; optional uses start off | Implemented (two switches are stored only) |

## 7. Stakeholder analysis

These are the roles a bank-hosted product like FinPath would need to involve. None has been consulted; the needs listed are expected concerns.

| Stakeholder | Influence | Interest | Approach | Expected needs and concerns | Engagement |
| --- | --- | --- | --- | --- | --- |
| End users (students, young professionals) | Medium | High | Keep informed, co-design | Simple, non-judgmental guidance; control over data | Interviews, usability tests, pilot feedback |
| Executive sponsor (digital banking) | High | High | Manage closely | Engagement with a young segment; fit with app strategy | Business case, demo, pilot read-out |
| Product owner / digital channel team | High | High | Manage closely | Roadmap fit, release capacity, overlap with NOMI | Backlog reviews, sprint demos |
| Privacy and legal | High | Medium | Keep satisfied | Consent, data minimisation, plain-language disclosures; education vs. advice | Privacy impact assessment before pilot |
| Compliance and risk | High | Medium | Keep satisfied | Fair treatment, no misleading claims, model risk for any future ML | Review insight wording and logic |
| Data and analytics | Medium | High | Keep informed | Categorisation accuracy, metric definitions | Metric definitions, data contracts |
| Engineering and security | Medium | Medium | Keep informed | Feasibility, authentication, secure storage | Architecture review |
| Accessibility specialists | Medium | Medium | Keep informed | WCAG 2.2 AA | Audit before pilot |
| Client support / advisors | Low | Medium | Monitor | Questions they will receive; hand-off to advisors | Briefing, FAQ |
| Campus partners | Low | Medium | Monitor | Financial literacy outreach | Optional pilot channel |

## 8. Competitive analysis: RBC NOMI

NOMI already lives in the RBC Mobile app. The table separates what RBC documents publicly from what FinPath's prototype does. Where a source doesn't describe a NOMI capability, the table says so; it does **not** treat that as a confirmed gap.

| Capability | RBC NOMI (as documented in sources) | FinPath concept (prototype) | Assessment |
| --- | --- | --- | --- |
| Spending insights | **Fact:** NOMI Insights analyses monthly cash flow, categorises spending and shows "where your money is going and what's coming up." [4] | **Implemented:** category chart with filters; 5 rule-based insight types, each showing its numbers and rule | Overlap. Showing the calculation is FinPath's proposed difference; whether NOMI explains its insights is not described in the sources reviewed. |
| Budgets | **Fact:** NOMI Budgets (2019) recommends budgets from spending history, lets clients adjust them, and notifies at 50%, 75% and 100%. [5] | **Implemented:** limits pre-filled from last month for 7 categories, all editable; in-app warning at 80% and over-budget state. No notifications. | Overlap; NOMI is ahead on proactive notifications. NOMI's current categories may have changed since 2019. |
| Upcoming payments | **Fact:** NOMI Forecast (2021) gives a 7-day view of upcoming pre-authorised payments, later extended to bill payments, e-transfers, investment contributions and salary; 900,000+ clients had used it by April 2023. [6][7] | **Implemented:** bills still due this month and expected income feed one safe-to-spend figure (synthetic schedule) | Strong overlap in data. FinPath's bet is the combination of bills, income timing and goal savings in one number; a real build should reuse Forecast's predictions. |
| Automated saving | **Fact:** NOMI Find & Save sets aside amounts clients are unlikely to miss; clients had saved more than $83 million by February 2019. [5][8] | Not offered. Goal contributions are logged by the user; no money moves. | NOMI ahead. FinPath does not compete here and could point goals at Find & Save. |
| Named goals with a date | Not described in the sources reviewed. | **Implemented:** name, target, month, monthly amount (BR-4), contributions, completion | Unverified. Check the current RBC Mobile app before claiming a gap. |
| Questions | **Fact:** Ask NOMI answers questions about recent transactions, helps cancel an e-Transfer and guides clients around the app. [4] | Ask FinPath: keyword matching on synthetic data. Not AI. | NOMI ahead: live, on real data. |

**Positioning.** An extension inside RBC Mobile that builds on NOMI's data (categories, Forecast predictions, Find & Save), not a competing app.

**Differentiation bets (unvalidated):**
- **B1:** one conservative number that reserves bills, income timing and goal savings is easier to act on (A-3).
- **B2:** goal-first planning motivates saving (A-4).
- **B3:** showing the math builds trust (A-2).

## 9. User journey and service blueprint

The journey follows the student proto-persona through her first month. Feelings are hypothesised, not observed.

| | Discover | Set up | First look | Plan | Live with it | Review |
| --- | --- | --- | --- | --- | --- | --- |
| **Goal** | Find out if it can help | Start without effort | See where money goes | Make a budget and a goal | Stay on track daily | See progress, adjust |
| **Actions** | Sees entry point in banking app | Name, life stage, income; privacy choices | Reads dashboard; taps biggest category | Edits limits; creates emergency fund | Checks safe to spend before buying | Reads insights; adds a contribution |
| **Feeling (assumed)** | Curious, sceptical | Cautious about data | Surprised by delivery total | In control | Reassured, or anxious if over | Motivated |
| **Frontstage** | Home banner | Onboarding 1–3 | Dashboard, Spending | Budget, Goals | Dashboard, bills card | Insights, Goals |
| **Backstage** | Eligibility check | Consent stored | Categorisation | Pre-fill from last month | Bill and income schedule (could reuse NOMI Forecast) | Monthly insight rules |
| **Pain to watch** | Unclear benefit | Too many questions | Wrong categories | Blank-page budgeting | Irregular income; bills due before payday (A-5) | Generic advice |
| **Design response** | One-line value proposition | Two short steps, or sample data | Tap a category to filter | Suggested limits | Safe to spend counts only money received, after bills and goals | "How we calculated this" |

## 10. Business case

| Customer problem | FinPath feature | Pilot outcome measure | Potential business value |
| --- | --- | --- | --- |
| Don't know what's safe to spend. Only 37% of Gen Z feel in control of their money. **(Fact)** | Safe to spend that counts only money received and reserves bills and goal savings; itemised on request. **(Implemented)** | Weekly use of the safe-to-spend view; self-reported confidence +0.5 after 60 days. **(Proposed)** | More frequent digital engagement. Could reduce overdraft or NSF events if pilot data confirms it. **(Hypothesis)** |
| Don't know where to start. 20% say so. **(Fact)** | Budget limits pre-filled from last month, editable in one step. **(Implemented)** | Setup completion 70%; first-session plan (≥1 budget and ≥1 goal) 40%. **(Proposed)** | An earlier primary banking relationship with clients at the start of their financial lives. **(Hypothesis)** |
| Saving feels abstract. **(Assumption A-4)** | Named goals with a target month and monthly amount. **(Implemented)** | Share of users contributing to a goal in month 2; baseline set in the pilot. **(Proposed)** | Savings deposit growth if goals were later linked to real accounts or Find & Save (outside MVP; needs compliance review). **(Hypothesis)** |
| Generic advice; unclear data use. **(Assumptions A-1, A-2)** | Insights that show their math; a switch for each data use. **(Implemented; insights are rule-based)** | Insight opt-in 75%; usefulness ≥ 3.8 of 5. The prototype already records "Useful? Yes/No". **(Proposed)** | Trust in digital guidance; evidence on whether ML insights are worth building over rules (A-6). **(Hypothesis)** |

**Business model.** Free feature inside the existing banking app; no subscription. Value comes from engagement, retention and trust, not direct revenue. No revenue, cost or ROI figures are estimated; they need finance and product-owner input and pilot data.

## 11. Success metrics

**North-star metric (proposed):** share of active users who stay within budget and contribute to a goal in the same month. Baseline set in the pilot.

| Metric | Definition | Type | Proposed pilot target |
| --- | --- | --- | --- |
| Setup completion | Users who finish onboarding ÷ users who start | Activation | 70% |
| First-session plan | Users with ≥1 budget and ≥1 goal in the first session | Activation | 40% |
| Month-2 activity | Users active in month 2 ÷ month-1 users | Retention | 50% |
| Insight usefulness | Average rating of insight cards (1–5) | Value | ≥ 3.8 |
| Insight opt-in | Users who keep insights on | Trust | 75% |
| Confidence change | Change in self-reported confidence (1–5) after 60 days | Outcome | +0.5 |
| Task success | Users who create a budget unaided in usability testing | Usability | 80% |
| Accessibility defects | Open WCAG 2.2 AA issues at launch | Quality | 0 critical |

None of these has been measured. They are starting points to agree with stakeholders.

## 12. MVP scope

| Included in MVP | Deferred |
| --- | --- |
| Onboarding with privacy choices | Linking accounts at other institutions |
| Dashboard with safe to spend | Automatic savings transfers |
| Spending breakdown and search | Recategorising transactions |
| Editable category budgets with warnings | Shared budgets (roommates, couples) |
| Savings goals with contributions | Term-based budgets for irregular income (A-5) |
| Rule-based insights with explanations | Machine-learning insights; live language-model chat |
| Settings, larger text, data deletion | Push notifications and monthly check-in |

**Rationale.** MVP items test the riskiest assumptions (A-1 to A-4) with the least build effort. Deferred items depend on external change (open banking), need validated demand first, or carry higher model and privacy risk.

## 13. Sources

1. [TD Bank Group: Gen Z financial pressure survey (Oct 14, 2025)](https://www.newswire.ca/en/releases/archive/October2025/14/c5267.html)
2. [CNBC: Budgeting app Mint is shutting down (Nov 7, 2023)](https://www.cnbc.com/2023/11/07/budgeting-app-mint-is-shutting-down-users-are-disappointed.html)
3. [Canada Gazette, Part I, Vol. 160, No. 26: Consumer-Driven Banking Regulations (June 27, 2026)](https://gazette.gc.ca/rp-pr/p1/2026/2026-06-27/html/reg3-eng.html)
4. [RBC: NOMI features in the RBC Mobile app](https://www.rbcroyalbank.com/mobile/feature/nomi/)
5. [RBC: NOMI Budgets launch (Apr 25, 2019)](https://newswire.ca/news-releases/rbc-first-bank-in-canada-to-launch-a-personalized-ai-powered-budget-solution-through-award-winning-mobile-app-825300571.html)
6. [RBC: NOMI Forecast launch (Sep 23, 2021)](https://newswire.ca/news-releases/rbc-introduces-new-digital-tools-to-give-clients-more-trust-and-confidence-in-managing-their-money-every-day-804049020.html)
7. [RBC: NOMI Forecast award and usage (Apr 28, 2023)](https://newswire.ca/news-releases/rbc-wins-best-use-of-ai-for-customer-experience-for-nomi-forecast-882322906.html)
8. [RBC: What is NOMI Find & Save](https://rbcroyalbank.com/ways-to-bank/tutorials/financial-advice/what-is-nomi-find-and-save.html)
