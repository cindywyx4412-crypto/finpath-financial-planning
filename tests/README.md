# FinPath automated tests

`qa_suite.py` drives the prototype in headless Chromium with [Playwright](https://playwright.dev/python/). It types, clicks, presses Enter and Escape, and reloads the page the way a user would. A small number of checks call the prototype's calculation functions directly; these are marked `"kind": "fn"` in the results. Accessibility checks use [axe-core](https://github.com/dequelabs/axe-core).

## What the suite covers

| Area | What is checked |
| --- | --- |
| Validation | Every form rejects empty, non-numeric, out-of-range and duplicate input with a specific message, keeps valid entries, and focuses the first invalid field |
| Calculations | Safe to spend (BR-1) recomputed independently from the raw synthetic data; per-day amount; expected income excluded; unpaid bills; itemised sheet total; goal-savings reserve before and after contributions; rest-of-month horizon; $0 floor with reason; budget states; goal monthly amount (BR-4); category totals |
| Responsive | No horizontal page scroll in all four views at 360 px and 1440 px; prototype view at 820 px; larger text |
| Accessibility | axe-core scan (WCAG 2.0–2.2 A/AA rule sets) of 6 screens and 2 open sheets; aria-invalid on errors; focus management; Escape closes sheets; all buttons and inputs ≥ 24 px |
| Goals, Spending, Insights, Budget | Create, contribute, complete and delete goals; filters, search and charts; insight generation and explanations; budget editing and warnings |
| Navigation, Privacy, Persistence | Onboarding path and tabs; privacy defaults and data deletion; reload persistence and demo reset |
| Error handling | Simulated connection failure, retry and recovery |
| Standalone | Embedded fonts and diagram load, and zero external network requests are attempted |
| Stability | No console or page errors during the whole run |

Automated accessibility rules cover only part of WCAG. A passing scan is not a conformance claim.

## Run locally

Requirements: Node.js 18+ and Python 3.10+.

```bash
# from the repository root
npm ci                                   # installs axe-core
pip install -r tests/requirements.txt    # installs Playwright for Python
python -m playwright install chromium    # downloads the browser (add --with-deps on Linux CI)

python tests/qa_suite.py                 # tests ./index.html from disk with the network blocked
```

To test a deployed copy instead:

```bash
python tests/qa_suite.py --url https://majestic-sundae-6965fc.netlify.app/
```

In `--url` mode, requests to the site's own origin are allowed and everything else is blocked and reported.

## Output

- Console: one `PASS` / `FAIL` line per check, then a total.
- `tests/results/qa-results.json`: every check with its area, result and detail.
- `tests/results/qa-summary.md`: a readable summary.

The script exits with code `0` only when every check passes, so it can gate CI. `tests/results/` is git-ignored; the committed, verified run is recorded in [`docs/qa-report.md`](../docs/qa-report.md).

## Continuous integration

`.github/workflows/tests.yml` runs the same suite on GitHub Actions for pushes to `main`, pull requests, and manual runs, and uploads `tests/results/` as an artifact. The workflow file has been checked for valid YAML. It had not yet run on GitHub when [`docs/qa-report.md`](../docs/qa-report.md) was written.
