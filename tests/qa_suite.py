"""
FinPath automated QA suite.

Drives the FinPath prototype in headless Chromium (Playwright) the way a user would:
typing, clicking, pressing Enter and Escape, reloading. A few checks call the
prototype's calculation functions directly (marked kind="fn" in the results).

Usage (from the repository root):
    python tests/qa_suite.py                      # tests ./index.html opened from disk, network blocked
    python tests/qa_suite.py --url https://...    # tests a deployed copy (only that site's origin allowed)

Results are written to tests/results/qa-results.json and tests/results/qa-summary.md.
Exit code is 0 only when every check passes.
"""
import argparse, asyncio, json, math, pathlib, sys
from urllib.parse import urlparse
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(description='FinPath QA suite')
ap.add_argument('--url', help='URL of a deployed copy (default: ./index.html from disk)')
ARGS = ap.parse_args()
URL = ARGS.url or (ROOT / 'index.html').as_uri()
if not URL.startswith('file:') and not URL.endswith('/') and '#' not in URL and not URL.endswith('.html'):
    URL += '/'
ORIGIN = None if URL.startswith('file:') else '{0.scheme}://{0.netloc}'.format(urlparse(URL))
AXE = ROOT / 'node_modules' / 'axe-core' / 'axe.min.js'
if not AXE.exists():
    sys.exit('axe-core not found. Run "npm ci" in the repository root first.')
RESULTS = ROOT / 'tests' / 'results'

# Every request outside the page itself is blocked and recorded, so the
# "Zero external network requests" check proves the page is self-contained.
BLOCKED = []
async def offline(page):
    async def h(route):
        u = route.request.url
        if u.startswith(('file:', 'data:', 'blob:')) or (ORIGIN and u.startswith(ORIGIN)): await route.continue_()
        else: BLOCKED.append(u); await route.abort()
    await page.route('**/*', h)
    return page
R = []
def rec(area, name, ok, detail='', kind='ui'):
    R.append({'area': area, 'test': name, 'pass': bool(ok), 'detail': str(detail), 'kind': kind})
    print(('PASS ' if ok else 'FAIL ') + area + ' | ' + name + ('' if ok else '  -> ' + str(detail)))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1440, 'height': 1000})
        pg = await offline(await ctx.new_page())
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(500)
        d = pg.locator('#device')
        async def click(sel): await d.locator(sel).first.click(); await pg.wait_for_timeout(60)
        async def fill(id, v):
            el = d.locator('#' + id); await el.fill(''); await el.type(str(v)); await pg.wait_for_timeout(30)
        txt = lambda: d.inner_text()

        # ---------- Onboarding ----------
        rec('Navigation', 'Fresh start opens Welcome', 'Know what you can spend' in await txt())
        await click('[data-act="ob:start"]')
        await click('[data-act="ob:about"]')
        t = await txt()
        rec('Validation', 'Onboarding: empty name and income show errors', 'Enter your first name.' in t and 'Enter your monthly income as a number.' in t, t[:200])
        rec('Accessibility', 'Invalid field marked aria-invalid and focused', await pg.evaluate("document.activeElement.id==='name' && document.activeElement.getAttribute('aria-invalid')==='true'"))
        await fill('name', 'Maya'); await fill('income', 'abc'); await click('[data-act="ob:about"]')
        rec('Validation', 'Onboarding: non-numeric income rejected', 'Enter your monthly income as a number.' in await txt())
        rec('Validation', 'Onboarding: valid name kept after another field fails', await d.locator('#name').input_value() == 'Maya')
        await fill('income', '60000'); await click('[data-act="ob:about"]')
        rec('Validation', 'Onboarding: income above $50,000 rejected', 'from $1 to $50,000' in await txt())
        await click('[data-act="set:stage:grad"]')
        await fill('income', '2400'); await click('[data-act="ob:about"]')
        t = await txt()
        rec('Navigation', 'Valid profile advances to privacy step', 'Your data, your choice' in t)
        st = await pg.evaluate("[...document.querySelectorAll('#device .sw-btn')].map(b=>b.getAttribute('aria-checked'))")
        rec('Privacy', 'Optional data uses default to off (BR-6)', st == ['true', 'false', 'false'], st)
        await click('[data-act="ob:finish"]')
        D = await pg.evaluate("window.__fp.D")
        rec('Navigation', 'Finish setup lands on dashboard', 'Safe to spend' in await txt() and D['onboarded'] and D['profile']['stage'] == 'grad')

        # ---------- Dashboard math (BR-1) ----------
        raw = await pg.evaluate("({spent:window.__fp.OCT_TOTAL, recur:window.__fp.RECUR, inc:window.__fp.INCOME, day:window.__fp.DAY})")
        DAYN = raw['day']; SPENT = raw['spent']
        RECEIVED = sum(i['amount'] for i in raw['inc'] if i['day'] <= DAYN)
        NEXT = min(i['day'] for i in raw['inc'] if i['day'] > DAYN)
        BILLS_PAYDAY = round(sum(b['amount'] for b in raw['recur'] if DAYN < b['day'] < NEXT), 2)
        BILLS_MONTH = round(sum(b['amount'] for b in raw['recur'] if b['day'] > DAYN), 2)
        exp_safe = max(0, math.floor(RECEIVED - SPENT - BILLS_PAYDAY))
        hero = await d.locator('.hero .amt').inner_text()
        rec('Calculations', 'Safe to spend = income received − spent − bills due before payday (no goals)', hero == f"${exp_safe:,}", f"{hero} vs {exp_safe}")
        sub = await d.locator('.hero .sub').inner_text()
        rec('Calculations', 'Per-day amount = floor(safe ÷ days until payday)', f"${exp_safe // (NEXT - DAYN):,} a day for the next {NEXT - DAYN} days" in sub, sub)
        ht = await d.locator('.hero').inner_text()
        rec('Calculations', 'Income not yet received is shown as not counted', '$400 expected on Oct 30 isn' in ht and f'until Oct {NEXT} payday' in ht, ht)
        bt = await d.locator('.card.bills').inner_text()
        rec('Calculations', 'Unpaid bills listed with due dates and set aside', 'Due Oct 24' in bt and 'Set aside' in bt and bt.count('Due Oct') == sum(1 for b in raw['recur'] if b['day'] > DAYN), bt)
        await click('[data-act="safe:open"]'); await pg.wait_for_timeout(300)
        st_ = await d.locator('.sheet').inner_text()
        rec('Calculations', 'Calculation sheet itemises bills, shows exclusions, and its total matches the dashboard', all(b['merchant'] in st_ for b in raw['recur'] if DAYN < b['day'] < NEXT) and 'not included' in st_.lower() and f"${exp_safe:,}" in st_.split('Safe to spend, ')[-1], st_[-400:])
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(80)
        rec('Empty states', 'New user sees create-budget and set-goal prompts', 'Create your first budget' in await txt() and 'Set a savings goal' in await txt())

        # ---------- Budget ----------
        await click('[data-act="tab:budget"]')
        rec('Empty states', 'Budget empty state shown', 'No budget yet' in await txt())
        await click('[data-act="budget:suggest"]')
        D = await pg.evaluate("window.__fp.D"); SUG = await pg.evaluate("window.__fp.SUGGESTED")
        rec('Budget', 'Suggested limits applied from September spending', D['budgets'] == SUG, D['budgets'])
        await click('[data-act="budget:edit:dining"]')
        rec('Accessibility', 'Edit sheet moves focus to the limit field', await pg.evaluate("document.activeElement.id==='limit'"))
        for v, msg in [('-50', 'from $0 to $10,000'), ('12.5', 'whole dollars'), ('20000', 'from $0 to $10,000'), ('', 'Enter a number.')]:
            await fill('limit', v); await click('[data-act="submit:budget"]')
            rec('Validation', f'Budget limit "{v}" rejected', msg in (await txt()), (await txt())[-300:])
        await fill('limit', '250'); await d.locator('#limit').press('Enter'); await pg.wait_for_timeout(100)
        D = await pg.evaluate("window.__fp.D"); OC = await pg.evaluate("window.__fp.OCT_CAT")
        rec('Budget', 'Enter key saves a valid limit', D['budgets']['dining'] == 250 and await d.locator('.sheet').count() == 0)
        row = await d.locator('.brow', has_text='Dining & delivery').inner_text()
        left = 250 - OC['dining']
        rec('Calculations', 'Remaining = limit − spent, shown on the row', f"${left:,.2f} left" in row or left < 0, row)
        await click('[data-act="budget:edit:dining"]'); await click('[data-act="limit:10"]')
        rec('Budget', '+10% quick adjust updates the field', await d.locator('#limit').input_value() == '275')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(60)
        rec('Accessibility', 'Escape closes the sheet without saving', await d.locator('.sheet').count() == 0 and (await pg.evaluate("window.__fp.D.budgets.dining")) == 250)
        bs = await pg.evaluate("[[79,100],[80,100],[100,100],[101,100],[0,0],[5,0]].map(([s,l])=>window.__fp.budgetState(s,l).k)")
        rec('Calculations', 'Budget states: <80% ok, ≥80% warn, =100% warn, >100% over', bs == ['ok', 'warn', 'warn', 'over', 'ok', 'over'], bs, 'fn')
        await click('[data-act="budget:edit:groceries"]'); await fill('limit', '3000'); await click('[data-act="submit:budget"]')
        rec('Budget', 'Budgeting more than income shows a warning (BR-3)', 'more than your income' in await txt())
        await click('[data-act="budget:edit:groceries"]'); await click('[data-act="limit:sug"]'); await click('[data-act="submit:budget"]')

        # ---------- Goals ----------
        await click('[data-act="tab:goals"]')
        rec('Empty states', 'Goals empty state shown', 'No goals yet' in await txt())
        await click('[data-act="goal:new"]')
        await click('[data-act="submit:goal"]')
        t = await txt()
        rec('Validation', 'Goal: empty name and target rejected', 'Give your goal a name.' in t and 'Enter a target amount.' in t)
        await fill('gname', 'New laptop'); await fill('gtarget', '1400'); await fill('gsaved', '1500'); await click('[data-act="submit:goal"]')
        rec('Validation', 'Goal: saved more than target rejected', 'can’t be more than the target' in await txt())
        await fill('gsaved', '200')
        await d.locator('#gdate').fill('2026-09'); await click('[data-act="submit:goal"]')
        rec('Validation', 'Goal: past target month rejected', 'November 2026 or later' in await txt())
        await d.locator('#gdate').fill('2027-04'); await pg.wait_for_timeout(50)
        prev = await d.locator('[data-form="goal"] .note').inner_text()
        rec('Calculations', 'Live preview: ceil((1400−200) ÷ 6 months) = $200', '$200 a month' in prev and '6 months' in prev, prev)
        await click('[data-act="submit:goal"]')
        D = await pg.evaluate("window.__fp.D")
        g = D['goals'][0] if D['goals'] else None
        rec('Goals', 'Valid goal is created and saved', g and g['name'] == 'New laptop' and g['target'] == 1400 and g['saved'] == 200 and g['date'] == '2027-04', g)
        rec('Calculations', 'Goal card shows monthly target (BR-4)', '$200/month' in await txt())
        await click('[data-act="goal:new"]'); await fill('gname', 'new LAPTOP'); await fill('gtarget', '100'); await click('[data-act="submit:goal"]')
        rec('Validation', 'Goal: duplicate name rejected (case-insensitive)', 'already have a goal' in await txt())
        await click('.sheet .sf [data-act="sheet:close"]')
        gid = g['id']
        await click(f'[data-act="goal:add:{gid}"]')
        for v, msg in [('0', 'at least $1'), ('5000', 'more than the $1,200 left')]:
            await fill('amt', v); await click('[data-act="submit:contrib"]')
            rec('Validation', f'Contribution "{v}" rejected', msg in await txt(), (await txt())[-200:])
        await fill('amt', '50'); await click('[data-act="submit:contrib"]')
        rec('Goals', 'Contribution adds to saved amount', (await pg.evaluate("window.__fp.D.goals[0].saved")) == 250)
        mon = await pg.evaluate("window.__fp.goalMonthly(window.__fp.D.goals[0])")
        rec('Calculations', 'Monthly target recalculates after contribution: ceil(1150 ÷ 6) = 192', mon == 192, mon, 'fn')
        k = await pg.evaluate("window.__fp.calc(window.__fp.D)")
        rec('Calculations', 'Goal savings reserve = month plan ($200) when less has been added ($50)', k['safe'] == max(0, math.floor(RECEIVED - SPENT - BILLS_PAYDAY - 200)) and k['goals'] == 200, k, 'fn')
        await click(f'[data-act="goal:add:{gid}"]'); await fill('amt', '1150'); await click('[data-act="submit:contrib"]')
        k = await pg.evaluate("window.__fp.calc(window.__fp.D)")
        rec('Calculations', 'Money added beyond the plan ($1,200) is reserved instead of the plan', k['goals'] == 1200 and k['safe'] == max(0, math.floor(RECEIVED - SPENT - BILLS_PAYDAY - 1200)), k, 'fn')
        rec('Goals', 'Reaching the target marks the goal done', 'Goal reached' in await txt() and 'Done' in await txt())
        await click(f'[data-act="goal:del:{gid}"]')
        rec('Goals', 'Delete asks for confirmation', await d.locator('[role="alertdialog"]').count() == 1)
        await click('[role="alertdialog"] [data-act="sheet:close"]')
        rec('Goals', 'Cancel keeps the goal', len(await pg.evaluate("window.__fp.D.goals")) == 1)
        await click(f'[data-act="goal:del:{gid}"]'); await click(f'[data-act="do:goal:{gid}"]')
        rec('Goals', 'Confirm deletes the goal', len(await pg.evaluate("window.__fp.D.goals")) == 0)

        # ---------- Spending ----------
        await click('[data-act="tab:spending"]')
        rows = await d.locator('.tx').count()
        await click('.crow[data-act="cat:dining"]')
        cats = await pg.evaluate("[...document.querySelectorAll('#device .card:last-of-type .tx .t-s')].map(e=>e.textContent.split(' · ')[0])")
        rec('Spending', 'Selecting a category filters transactions', len(cats) > 0 and all(c == 'Dining & delivery' for c in cats), cats[:5])
        ctr = await d.locator('.donut .ctr').inner_text()
        rec('Spending', 'Donut centre shows selected category', 'Dining' in ctr, ctr)
        await click('rect.b[data-act^="bar:"]')
        rec('Spending', 'Tapping a bar shows that day\'s amount', 'October' in await d.locator('.tip').inner_text())
        await click('.crow[data-act="cat:dining"]')
        rec('Spending', 'Selecting again clears the filter', await d.locator('.tx').count() == rows)
        await d.locator('#q').type('zzz'); await pg.wait_for_timeout(80)
        rec('Empty states', 'Search with no match shows empty state', 'No transactions match "zzz"' in await txt())
        rec('Accessibility', 'Search keeps focus while typing', await pg.evaluate("document.activeElement.id==='q'"))
        await click('[data-act="spend:clear"]')
        await d.locator('#q').type('quickbite'); await pg.wait_for_timeout(80)
        names = await pg.evaluate("[...document.querySelectorAll('#device .tx .t-bs')].map(e=>e.textContent)")
        rec('Spending', 'Search matches merchant names case-insensitively', len(names) > 0 and all('QuickBite' in n for n in names), names[:3])
        await d.locator('#q').fill(''); await pg.wait_for_timeout(50)
        await click('[data-act="period:week"]')
        rec('Spending', 'Week toggle switches the period', 'Last 7 days' in await txt())
        tot = await pg.evaluate("Math.round([...document.querySelectorAll('#device .crow .amt')].reduce((s,e)=>s+Number(e.textContent.replace(/[$,]/g,'')),0)*100)/100")
        shown = float((await d.locator('.card').first.locator('.t-num').first.inner_text()).replace('$', '').replace(',', ''))
        rec('Calculations', 'Category amounts sum to the period total', abs(tot - shown) < 0.02, f"{tot} vs {shown}")

        # ---------- Insights ----------
        await click('[data-act="tab:insights"]')
        rec('States', 'Insights show a loading skeleton first', await d.locator('[aria-busy="true"]').count() >= 1)
        await pg.wait_for_timeout(900)
        n = await d.locator('.card.ins').count()
        rec('Insights', 'At least 4 insight cards generated from data', n >= 4, n)
        rec('Insights', 'Insights are labelled as demo logic, not AI', 'not generated by an AI model' in await txt())
        await click('[data-act^="ins:open:"]')
        rec('Insights', '"How we calculated this" shows numbers and rule', await d.locator('.sheet .calc').count() == 1 and 'rule' in (await d.locator('.sheet').inner_text()).lower())
        await click('.sheet [data-act="sheet:close"]')
        await d.locator('#askq').fill(''); await d.locator('#askq').press('Enter'); await pg.wait_for_timeout(80)
        rec('Validation', 'Ask: empty question shows an error', 'Type a question first.' in await txt())
        await d.locator('#askq').type('How much on groceries?'); await d.locator('#askq').press('Enter'); await pg.wait_for_timeout(800)
        exp = f"{OC['groceries']:,.2f}"
        rec('Insights', 'Ask: category question answered from data', exp in await txt(), exp)
        await click('[data-act="ask:What can I safely spend?"]'); await pg.wait_for_timeout(800)
        ans = await d.locator('.bubble.a').last.inner_text(); kk = await pg.evaluate("window.__fp.calc(window.__fp.D)")
        rec('Insights', 'Ask: safe-to-spend answer matches the dashboard figure and names what is set aside', f"safely spend ${kk['safe']:,}" in ans and 'sets aside' in ans, ans)
        await click('[data-act="fb:change:y"]')
        rec('Insights', 'Usefulness feedback is stored', (await pg.evaluate("window.__fp.D.feedback.change")) == 'y')

        # ---------- Settings, privacy, errors ----------
        await click('[data-act="tab:home"]'); await click('[data-act="nav:settings"]')
        await click('[data-act="sim:offline"]')
        await click('[data-act="nav:back"]'); await click('[data-act="tab:insights"]'); await pg.wait_for_timeout(900)
        rec('Error handling', 'Simulated failure shows error state with retry', "Couldn't load insights" in await txt() and await d.locator('[data-act="ins:retry"]').count() == 1)
        await click('[data-act="ask:How are my goals?"]'); await pg.wait_for_timeout(800)
        rec('Error handling', 'Ask FinPath reports the failure instead of answering', 'Couldn’t answer right now' in await txt())
        await click('[data-act="tab:home"]'); await click('[data-act="nav:settings"]'); await click('[data-act="sim:offline"]')
        await click('[data-act="nav:back"]'); await click('[data-act="tab:insights"]'); await pg.wait_for_timeout(900)
        rec('Error handling', 'After the cause is cleared, insights load again', await d.locator('.card.ins').count() >= 4)
        await click('[data-act="tab:home"]'); await click('[data-act="nav:settings"]')
        await click('[data-act="priv:insights"]'); await click('[data-act="nav:back"]'); await click('[data-act="tab:insights"]')
        rec('Privacy', 'Turning off insights hides analysis and explains why', 'Insights are off' in await txt())
        await click('[data-act="priv:insights"]'); await pg.wait_for_timeout(900)
        rec('Privacy', 'Turning insights back on restores them', await d.locator('.card.ins').count() >= 4)
        await click('[data-act="tab:home"]'); await click('[data-act="nav:settings"]')
        await fill('income', ''); await d.locator('#income').press('Enter'); await pg.wait_for_timeout(80)
        rec('Validation', 'Settings: blank income rejected', 'Enter your monthly income as a number.' in await txt())
        await fill('income', '3100'); await click('button[type="submit"]')
        rec('Settings', 'Profile saves valid income', (await pg.evaluate("window.__fp.D.profile.income")) == 3100)
        await click('[data-act="a11y:large"]')
        rec('Accessibility', 'Larger text setting enlarges type', await d.locator('.scr.lg').count() == 1)
        ow = await pg.evaluate("[...document.querySelectorAll('#device .body *')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflowX==='visible'&&e.clientWidth>0).length")
        rec('Responsive', 'Larger text causes no horizontal overflow in Settings', ow == 0, ow)
        await click('[data-act="a11y:large"]')

        # ---------- Persistence ----------
        await pg.reload(); await pg.wait_for_timeout(700)
        D = await pg.evaluate("window.__fp.D")
        rec('Persistence', 'Data survives a page reload', D['onboarded'] and D['profile']['income'] == 3100 and D['budgets']['dining'] == 250 and D['feedback'].get('change') == 'y')
        await click('[data-act="nav:settings"]'); await click('[data-act="confirm:reset"]'); await click('[data-act="do:reset"]')
        D = await pg.evaluate("window.__fp.D")
        rec('Persistence', 'Reset demo restores the sample user', D['profile']['name'] == 'Maya' and len(D['goals']) == 3)
        await click('[data-act="nav:settings"]'); await click('[data-act="confirm:delete"]')
        rec('Privacy', 'Delete all data asks for confirmation (BR-7)', await d.locator('[role="alertdialog"]').count() == 1)
        await click('[data-act="do:delete"]')
        stored = await pg.evaluate("localStorage.getItem('finpath-demo-v2')")
        rec('Privacy', 'Delete clears storage and restarts onboarding', stored is None and 'Know what you can spend' in await txt())

        # ---------- Over-plan state ----------
        base = "{v:2,onboarded:true,profile:{name:'Maya',stage:'student',income:%s},privacy:{insights:true,personal:false,analytics:false,reminders:false},largeText:false,budgets:{},goals:%s,feedback:{},sim:{offline:false}}"
        await pg.evaluate("localStorage.setItem('finpath-demo-v2', JSON.stringify(" + base % ('2400', "[{id:'x',name:'Tuition top-up',icon:'book',target:900,saved:0,added:0,date:'2026-11'}]") + "))")
        await pg.reload(); await pg.wait_for_timeout(600)
        rec('Calculations', 'Over plan: safe to spend floors at $0 and explains why', (await d.locator('.hero .amt').inner_text()) == '$0' and "more than the income you've received" in await txt())
        await pg.evaluate("localStorage.setItem('finpath-demo-v2', JSON.stringify(" + base % ('1500', '[]') + "))")
        await pg.reload(); await pg.wait_for_timeout(600)
        ht = await d.locator('.hero').inner_text(); exp2 = max(0, math.floor(RECEIVED - SPENT - BILLS_MONTH))
        rec('Calculations', 'No income still expected: horizon is rest of month and all remaining bills are set aside', 'rest of October' in ht and 'expected on' not in ht and f"${exp2:,}" in ht and f"next {31 - DAYN + 1} days" in ht, ht)

        # ---------- Navigation coverage ----------
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(400)
        await click('[data-act="ob:sample"]')
        okn = True
        for tab, word in [('spending', 'Total spent'), ('budget', 'Spent of budgeted'), ('goals', 'Saved across goals'), ('insights', 'Ask FinPath'), ('home', 'Safe to spend')]:
            await click(f'[data-act="tab:{tab}"]'); okn = okn and word in await txt()
        rec('Navigation', 'All five tabs reachable and render', okn)
        await click('[data-act="nav:settings"]'); await click('[data-act="nav:back"]')
        rec('Navigation', 'Settings back returns to the previous tab', 'Safe to spend' in await txt())

        # ---------- Accessibility scan (axe-core) ----------
        await pg.add_script_tag(path=str(AXE))
        viol = {}
        for r in ['home', 'spending', 'budget', 'goals', 'insights', 'settings']:
            await pg.evaluate(f"document.querySelector('[data-jump=\"{r}\"]').click()"); await pg.wait_for_timeout(900)
            res = await pg.evaluate("axe.run('#device',{runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,ex:v.nodes.slice(0,2).map(n=>n.target.join(' '))})))")
            viol[r] = res
        flat = [(r, v['id'], v['impact'], v['n'], v['ex']) for r, vs in viol.items() for v in vs]
        rec('Accessibility', 'axe-core 4.10 scan (WCAG 2.0–2.2 A/AA rule sets) of 6 screens: no violations', len(flat) == 0, flat)
        TAGS = "['wcag2a','wcag2aa','wcag21aa','wcag22aa']"
        sres = []
        await pg.evaluate("document.querySelector('[data-jump=\"budget\"]').click()"); await pg.wait_for_timeout(300); await click('[data-act="budget:edit:dining"]'); await pg.wait_for_timeout(400)
        sres += await pg.evaluate("axe.run('#device',{runOnly:" + TAGS + "}).then(r=>r.violations.map(v=>'budget-sheet '+v.id+':'+v.nodes.length))")
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(100)
        await pg.evaluate("document.querySelector('[data-jump=\"home\"]').click()"); await pg.wait_for_timeout(300); await click('[data-act="safe:open"]'); await pg.wait_for_timeout(400)
        sres += await pg.evaluate("axe.run('#device',{runOnly:" + TAGS + "}).then(r=>r.violations.map(v=>'safe-sheet '+v.id+':'+v.nodes.length))")
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(100)
        rec('Accessibility', 'axe-core scan of two open sheets (budget edit, safe-to-spend detail): no violations', len(sres) == 0, sres)
        small = []; small44 = set()
        for r in ['home', 'spending', 'budget', 'goals', 'insights', 'settings']:
            await pg.evaluate(f"document.querySelector('[data-jump=\"{r}\"]').click()"); await pg.wait_for_timeout(900)
            small += await pg.evaluate("[...document.querySelectorAll('#device button,#device input')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<24||r.width<24)}).map(e=>e.outerHTML.slice(0,60))")
            small44 |= set(await pg.evaluate("[...document.querySelectorAll('#device button,#device input')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height<44}).map(e=>e.className.split(' ')[0]||e.tagName)"))
        rec('Accessibility', 'All buttons and inputs on 6 screens at least 24×24 px (WCAG 2.5.8 minimum)', len(small) == 0, small[:4])
        print('INFO controls under 44 px tall:', sorted(small44))

        # ---------- Responsive ----------
        m = await offline(await b.new_page(viewport={'width': 360, 'height': 740}))
        await m.goto(URL); await m.wait_for_timeout(500)
        rec('Responsive', '360 px phone: no horizontal page scroll', not await m.evaluate("document.documentElement.scrollWidth>innerWidth"))
        for h in ['screens', 'system', 'handoff']:
            await m.goto(URL + '#' + h); await m.wait_for_timeout(300)
            rec('Responsive', f'360 px: #{h} view has no horizontal page scroll', not await m.evaluate("document.documentElement.scrollWidth>innerWidth"))
        t = await offline(await b.new_page(viewport={'width': 820, 'height': 1180}))
        await t.goto(URL); await t.wait_for_timeout(400)
        rec('Responsive', 'Tablet 820 px: prototype view stacks without overflow', not await t.evaluate("document.documentElement.scrollWidth>innerWidth"))
        for h in ['prototype', 'screens', 'system', 'handoff']:
            await pg.goto(URL + '#' + h); await pg.wait_for_timeout(300)
            rec('Responsive', f'Desktop 1440 px: #{h} view has no horizontal page scroll', not await pg.evaluate("document.documentElement.scrollWidth>innerWidth"))

        await pg.goto(URL); await pg.wait_for_timeout(800)
        fonts = await pg.evaluate("Promise.all(['400','500','600','700','800'].map(w=>document.fonts.load(w+' 16px Manrope')).concat(['400','500','600'].map(w=>document.fonts.load(w+' 12px \"IBM Plex Mono\"')))).then(r=>r.map(f=>f.length>0&&f.every(x=>x.status==='loaded')))")
        rec('Standalone', 'Embedded fonts load with no network (Manrope, IBM Plex Mono)', all(fonts), fonts)
        await pg.goto(URL + '#handoff'); await pg.wait_for_timeout(500)
        nw = await pg.evaluate("(()=>{const i=document.querySelector('.pg-flow img');return i&&i.complete?i.naturalWidth:0})()")
        rec('Standalone', 'Embedded flow diagram renders', nw > 0, nw)
        rec('Standalone', 'Zero external network requests attempted', len(BLOCKED) == 0, BLOCKED[:5])
        rec('Stability', 'No console or page errors during the run', len(errs) == 0, errs[:5])
        await b.close()
    RESULTS.mkdir(parents=True, exist_ok=True)
    passed = sum(r['pass'] for r in R)
    json.dump({'target': URL, 'total': len(R), 'passed': passed, 'checks': R}, open(RESULTS / 'qa-results.json', 'w'), indent=1)
    by = {}
    for r in R: by.setdefault(r['area'], [0, 0]); by[r['area']][0] += r['pass']; by[r['area']][1] += 1
    lines = [f"# FinPath QA summary", "", f"Target: `{URL}`", "", f"**{passed} of {len(R)} checks passed** "
             f"({sum(r['kind']=='ui' for r in R)} drive the UI, {sum(r['kind']=='fn' for r in R)} call calculation functions directly).", "",
             "| Area | Passed | Checks |", "| --- | --- | --- |"] + [f"| {a} | {v[0]} | {v[1]} |" for a, v in sorted(by.items(), key=lambda x: -x[1][1])] + \
            ["", "| Result | Area | Check |", "| --- | --- | --- |"] + [f"| {'PASS' if r['pass'] else 'FAIL'} | {r['area']} | {r['test']} |" for r in R]
    (RESULTS / 'qa-summary.md').write_text('\n'.join(lines) + '\n')
    print(f"\n{passed}/{len(R)} passed; ui={sum(r['kind']=='ui' for r in R)} fn={sum(r['kind']=='fn' for r in R)}")
    return passed == len(R)

if __name__ == '__main__':
    sys.exit(0 if asyncio.run(main()) else 1)
