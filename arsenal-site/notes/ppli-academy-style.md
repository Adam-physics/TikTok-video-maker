# Style reference: Arsenal PPLI Academy (ppli-academy.netlify.app)

Reviewed October 2026 with frame bursts on scroll, every interaction, dark mode, mobile, the CSS, and the trailer frame by frame.

## Design system

**Colour.** One accent (teal), plus two colours that carry meaning, never decoration.

| Token | Light | Dark |
|---|---|---|
| Background | `#f6f7f9` | `#0f1724` |
| Surface | `#ffffff` | `#172235` |
| Ink | `#0b1f3a` | `#edf2f8` |
| Muted | `#64728a` | `#93a1b6` |
| Teal (accent) | `#007c7a`, `#00a3a1` | `#5ccbc6` |
| Gold (money) | gold | gold |
| Red (tax / no) | `#c4283a` | `#ff8a93` |

**Type.** Four families, each with a fixed job.
- Plus Jakarta Sans: headlines, tight tracking.
- Inter: body text.
- JetBrains Mono: small uppercase eyebrows and metadata.
- Instrument Serif: italic, used for emotional accents, mainly in the videos.

**Shape and depth.**
- Radius: 20px for cards, 12px for small elements, 999px for pills.
- Shadows have two layers and are tinted navy, never grey: `0 1px 2px … , 0 10px 30px -14px rgba(11,31,58,.18)`.

**Motion.**
- 44 named animations.
- UI transitions run .15–.3s.
- The easing overshoots slightly, like a spring: `cubic-bezier(.2,.8,.2,1.1–1.4)`.
- Illustrations loop slowly.
- Animations explain something or respond to the visitor; none is decoration.

**Dark mode.** Fully designed, illustrations included; not just an inverted palette.

## Page patterns

1. **The brand mark is a living hero.**
   - On load: stars appear, connect, the facets fill in, then a label fades in.
   - The Arsenal / Sky Gem / Partnership toggle morphs the shape: it dissolves to dust and reassembles. Partnership shows both marks linked by a dotted line.
2. **One idea per section, each with one object** that proves it:
   - an accordion beside a live diagram,
   - a lesson path,
   - a four-gate fit check,
   - a tax comparison,
   - a year slider.
3. **Interactions with real feedback.**
   - Fit check: a ball walks through gates. They turn teal with a check, or red with an X. Finishing turns the ball into a gold sun. A "no" gets an honest message: "Probably not a fit. Spotting that early protects the client and your reputation."
   - Slider: past years are teal and future years grey, the headline number counts up live, and the assumptions sit right under the chart.
4. **One visual vocabulary everywhere.** The trailer, the in-page diagram and the lesson thumbnails all use the same images: gold particles for money, a teal "wrapper" pipe for the policy, a "You" avatar, a red TAX tag.
5. **Edges are designed, not forgotten.**
   - Booking: day chips, then time chips, then fields; the button stays disabled until it's valid.
   - "Video coming soon" cards are designed in their own right.
   - A certificate card is "the finish line".
   - A "demo version" banner says honestly what the page is.
   - Mobile gets a sticky bottom call to action.
   - The floating pill nav tightens on scroll.
6. **Plain-language copy** that speaks to the reader ("you"), with specific numbers, and disclaimers sitting next to the claims they qualify.

## The trailer (79s, 1920×1080)

- **One metaphor, start to finish:** money is gold liquid and particles.
  - The client's portfolio is a bowl of gold. A red TAX laser hits it every year, with a year counter.
  - A "legal way" ring then shields it.
  - Investments flow into a "life insurance policy" pipe and fill a cash-value cylinder, which sits beside a shrinking taxed account.
  - A wallet stands for policy loans, then the gold flows on to the heirs.
  - The letters "PPLI" assemble from the particles.
- **Structure:**
  - Problem in a dark scene.
  - "Here's how" turns the scene light.
  - The mechanism, step by step.
  - Who it's for, then "you" (advisor, agent, CPA and attorney merge into one "You" avatar).
  - Why it pays you: big cases, trusted clients.
  - Sky Gem does the work, shown as a checklist.
  - The 7-lesson course path, then a call to action with a cursor clicking it.
- **Text:** serif headlines at the top left, one italic accent word in colour, words revealed in time with the narration. A small legal footnote sits on each scene.
- **Sound:** slow, ambient music (about 66 BPM) under a calm narrator, about 190 words in 79s.

## Why this reads as crafted, not "vibe-coded"

1. A real design system: tokens, a type scale with roles, and consistent radii and shadows. Not one-off utility classes.
2. Colour carries meaning (teal = good or path, gold = money, red = tax or no). No purple-blue gradients.
3. Every section has one job and one object that demonstrates it, rather than grids of text cards.
4. The same metaphor and characters run through video, diagrams and UI, so the whole thing feels authored by one hand.
5. Motion explains and responds; nothing moves just to move.
6. The unglamorous states are finished: disabled, empty, coming soon, errors, dark mode, mobile, compliance notes.
7. The copy is short, concrete and honest, and every section points to one call to action.

## Weak spots noticed

- **Hidden content:** sections stay invisible until they're scrolled into view, so a page capture without scrolling (and possibly some link previews or crawlers) shows mostly blank space.
- **Hard-to-read small text:** some mono labels and footnotes are very small and low-contrast.
- **Unfinished lessons:** lessons 4–7 have no videos yet.
