# FinPath: Design System and Screen Inventory

The tokens, components and screens used in the prototype. The live demo has the same content with rendered components: see the **Design system**, **All screens** and **Figma handoff** tabs.

> **No Figma file exists yet.** This document and the handoff tab prepare one. The screens can be imported into Figma with the html.to.design plugin.

## Principles

1. **One number first, and a cautious one.** Safe to spend leads the dashboard and never counts money that hasn't arrived.
2. **Show the math.** Safe to spend and every insight open their numbers and rule.
3. **State in words, not just colour.** Budget status always has a label and an icon.
4. **Respect the user.** No guilt language; optional data uses start off.

## Colour

Ink and canvas carry the structure. Teal is the only accent and marks actions and progress. Green, amber and red only describe budget state.

| Token | Hex | Use |
| --- | --- | --- |
| Ink / 900 | `#0F1C24` | Text, primary buttons, hero |
| Ink / 700 | `#3B4850` | Body text |
| Ink / 500 | `#66737A` | Captions, labels |
| Line / 200 | `#E3E5DF` | Borders, dividers |
| Canvas / 50 | `#F6F6F3` | Screen background |
| Surface / 0 | `#FFFFFF` | Cards, sheets, bars |
| Teal / 600 | `#0E6E63` | Accent: actions, progress |
| Teal / 700 | `#0A5950` | Accent hover |
| Teal / 50 | `#E3F1EE` | Selected fill, accent tint |
| Success / 700 | `#1A7A49` | On track, goal done |
| Warning / 700 | `#995500` | Near limit, demo labels |
| Danger / 700 | `#B42318` | Over budget, delete, errors |

**Chart categories.** Each colour is always paired with an icon and a name.

| Category | Hex |
| --- | --- |
| Housing | `#2F4B7C` |
| Groceries | `#0E6E63` |
| Dining & delivery | `#C46A1C` |
| Transport | `#3A7FC1` |
| Subscriptions | `#7E57C2` |
| Shopping | `#B83B64` |
| Other | `#7D878D` |

## Typography

Manrope for everything; IBM Plex Mono for labels in the page chrome. Both are embedded in `index.html` (SIL Open Font License). Amounts use tabular figures. The Larger text setting scales every style by about 115%.

| Style | Size / line height · weight |
| --- | --- |
| Display / Amount | 42/42 · ExtraBold · −3% tracking |
| Title / Screen | 26/31 · ExtraBold · −2% |
| Heading / Card | 17/22 · ExtraBold |
| Body | 15/22 · Regular |
| Body Strong | 15/21 · Bold |
| Small | 13/18 · Medium |
| Overline | 12/16 · ExtraBold · uppercase +8% |

## Spacing and radius

- **Spacing:** a 4-point scale (4, 8, 12, 16, 20, 24, 32).
  - Screens: 20 px side padding and 16 px between cards.
  - Cards: 16 px padding and 12 px between rows.
- **Radius:**

| Radius | Used for |
| --- | --- |
| 7 | Status chip |
| 12 | Icon button, input |
| 14 | Button, field |
| 18 | Card |
| 22 | Hero |
| 26 | Sheet |
| 999 | Chip, toggle, progress bar |

## Components

17 component specifications, smallest first, so larger components can nest them. The **Auto Layout** column is guidance for rebuilding each component in Figma.

| Component | Variants | Auto Layout |
| --- | --- | --- |
| Button | Type: Primary, Accent, Secondary, Ghost, Danger · Size: Default 48, Small 40 · State: Default, Hover, Disabled, Loading | Horizontal · hug · gap 8 · padding 11/18 · radius 14 |
| Input | State: Default, Focus, Error, Disabled · Prefix: on/off | Vertical (label, field, message) gap 6; field horizontal gap 8, padding 0/14, min height 50 |
| Toggle row | Value: On, Off | Horizontal · fill · gap 12 · padding 14/0 · bottom divider |
| Segmented control | Selected: Week, Month | Horizontal · fill · padding 3 · gap 3 · radius 12 |
| Chip | State: Default, Selected · Icon: on/off | Horizontal · hug · gap 6 · padding 0/14 · height 36 · radius 999 |
| Status chip | Type: On track, Near limit, Over, Neutral, Demo | Horizontal · hug · gap 4 · padding 0/8 · height 24 · radius 7 |
| Progress bar | State: Default, Warning, Over, Done | Fixed height 8; inner fill width = % |
| Card | Padding 16 · radius 18 | Vertical · fill · gap 12 |
| Safe-to-spend hero | State: Default, Over plan | Vertical · fill · gap 14 · padding 20 · radius 22 |
| Budget row | State: On track, Near limit, Over, No limit | Vertical gap 10 → row (icon 38, text fill, icon button) + row (progress fill, status chip) |
| Goal card | State: In progress, Done | Vertical gap 12 → header row, amount row, progress, action row |
| Insight card | Tone: Warning, Danger, Info, Positive | Vertical gap 10 → icon and text row, actions row, feedback row |
| Transaction row | — | Horizontal · fill · gap 12 · padding 10/0 |
| Tab bar | Active: Home, Spending, Budget, Goals, Insights | Horizontal · 5 equal columns · padding 6/6/24 |
| Bottom sheet | Content slot | Vertical: grab, header, scroll body (gap 16, padding 8/20), footer (2 buttons, gap 10) |
| Dialog | Type: Default, Destructive | Vertical gap 12 · padding 22 · radius 22 |
| Empty / error state | Type: Empty, Error | Vertical · centre · gap 10 · padding 28/16 |

**Known gap:** chips (36 px), toggles (30 px), segmented buttons (38 px) and small buttons (40 px) are below the 44 px touch-target goal in NFR-1. They meet the WCAG 2.5.8 minimum of 24 px.

## Screen inventory

22 frames at 390 × 844, rendered by the prototype's own code with sample states. Screenshots are in [`screenshots/`](screenshots/).

| # | Screen | State | Screenshot |
| --- | --- | --- | --- |
| 01 | Onboarding | Welcome | [01](screenshots/01-onboarding-welcome.png) |
| 02 | Onboarding | About you, validation error | [02](screenshots/02-onboarding-about-you-validation.png) |
| 03 | Onboarding | Privacy choices | [03](screenshots/03-onboarding-privacy-choices.png) |
| 04 | Dashboard | Default | [04](screenshots/04-dashboard.png) |
| 05 | Dashboard | Over plan | [05](screenshots/05-dashboard-over-plan.png) |
| 06 | Dashboard | New user (empty) | [06](screenshots/06-dashboard-new-user.png) |
| 07 | Spending | Month | [07](screenshots/07-spending-month.png) |
| 08 | Spending | Category selected | [08](screenshots/08-spending-category-selected.png) |
| 09 | Spending | No search results | [09](screenshots/09-spending-no-results.png) |
| 10 | Budget | Default | [10](screenshots/10-budget.png) |
| 11 | Budget | Edit limit, error | [11](screenshots/11-budget-edit-limit-error.png) |
| 12 | Budget | Empty | [12](screenshots/12-budget-empty.png) |
| 13 | Goals | Default | [13](screenshots/13-goals.png) |
| 14 | Goals | Create goal | [14](screenshots/14-goals-create-goal.png) |
| 15 | Goals | Add money | [15](screenshots/15-goals-add-money.png) |
| 16 | Goals | Empty | [16](screenshots/16-goals-empty.png) |
| 17 | Insights | Ready | [17](screenshots/17-insights.png) |
| 18 | Insights | Loading | [18](screenshots/18-insights-loading.png) |
| 19 | Insights | Error | [19](screenshots/19-insights-error.png) |
| 20 | Insights | Calculation detail | [20](screenshots/20-insights-calculation-detail.png) |
| 21 | Settings | Default | [21](screenshots/21-settings-privacy.png) |
| 22 | Settings | Delete confirmation | [22](screenshots/22-settings-delete-confirmation.png) |

## Prototype connection map

All connections are "On tap → Navigate to" unless marked overlay or delay.

| From | Trigger | To |
| --- | --- | --- |
| 01 Welcome | Get started | 02 About you |
| 01 Welcome | Explore with sample data | 04 Dashboard |
| 02 About you | Continue (valid) | 03 Privacy |
| 02 About you | Continue (invalid) | 02 About you · Error |
| 03 Privacy | Finish setup | 06 Dashboard · New user |
| Any main screen | Tab bar item | 04 / 07 / 10 / 13 / 17 |
| 04 Dashboard | Settings icon | 21 Settings |
| 04 Dashboard | How this is calculated | Safe-to-spend detail sheet (overlay) |
| 04 Dashboard | Budget health · View all | 10 Budget |
| 04 Dashboard | Insight card | 17 Insights |
| 07 Spending | Category row | 08 Category selected |
| 07 Spending | Search with no match | 09 No results |
| 10 Budget | Edit icon | 11 Edit sheet (overlay) |
| 12 Budget empty | Use suggested limits | 10 Budget |
| 13 Goals | New goal | 14 Create sheet (overlay) |
| 13 Goals | Add money | 15 Add money sheet (overlay) |
| 16 Goals empty | Create a goal | 14 Create sheet |
| 17 Insights | How we calculated this | 20 Detail sheet (overlay) |
| 18 Loading | After delay (700 ms) | 17 Insights or 19 Error |
| 19 Error | Try again | 18 Loading |
| 21 Settings | Delete all my data | 22 Delete dialog (overlay) |
| 22 Delete dialog | Delete everything | 01 Welcome |
| 21 Settings | Back | Previous tab |

## Importing into Figma

1. In Figma, run the html.to.design plugin on the live demo URL:
   - add `#screens` to the end for the frames;
   - run it again with `#system` for component states;
   - use a desktop width of 1440.
2. Rename frames to match the inventory and delete page captions.
3. Create colour variables and text styles from the tables above.
4. Rebuild each component, then swap the imported copies for instances.
5. Add the connections from the map, set the device to iPhone 14/15, and set the flow start to 01 Welcome.
