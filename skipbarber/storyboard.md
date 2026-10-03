# Storyboard: Skip Barber demo video

Status: **Step 3 checkpoint, waiting for approval.** All timings are provisional and assume 124 BPM. They will snap to the real beat map once the music file is supplied. Every scene length is set in beats in `video/src/timeline.ts`.

Brand values from the scrape (`scrape/inventory.md`):
- Colors: red `#FF0000`, black `#000000`, header ink `#111111`, white.
- Fonts on the site: Helvetica BLK Italic for section heads, Source Sans Pro for hero text, Inter for body. Helvetica BLK Italic is self-hosted by the site and not licensed to us, so Inter Tight 900 italic stands in for it. Source Sans 3 and Inter are used as on the site. Instrument Serif italic is the accent word font.

## Fact changes after the scrape (the site wins)

| Draft line | What the site says | Change in the video |
|---|---|---|
| "the school that trained..." | Alumni include Sergio Perez (F1), Colton Herta (IndyCar), Jordan Taylor (IMSA), Ross Chastain (NASCAR) | "What if you learned where *champions* learned?" and "From our *classroom* to" + the four series |
| "400,000+ drivers" | "Over 400,000 Alumni" (home page) | "400,000+ Skip Barber alumni" |
| "Champions in F1. IndyCar. IMSA. NASCAR." | Named alumni across the four series. No single "champions in" sentence | "From our *classroom* to FORMULA 1. INDYCAR. IMSA. NASCAR." |
| Three Day is the "signature" program | "our most popular program" | "Most popular" tag on the Three Day card |
| "Earn your license" (club, pro or international) | "places drivers on the path towards receiving a racing license with SCCA or USAC" | "On the path to your *license*." Badge: SCCA & USAC Licensed Racing School |
| Day 1 / Day 2 / Day 3 curriculum, incl. downshifting, threshold braking, flags, restarts, defending | No day-by-day split on the site. Found: braking marks, turn-in points, apex; instructors analyze lines, brake and throttle application; passing exercises, practice race starts, open lapping | Steps 01, 02, 03 without day labels, using only the found items |
| Mustang GT School Car, F4 with aero and slicks | "Skip Barber GT" (from a road-going Ford Mustang); Mygale FIA F4 "to 60 mph in under 4 seconds" | Car names as on the site. F4 aero/slicks dropped |
| GTX with "GMS Track Experience", new in 2026, oval | Partner is "GMS Race Cars". "our newest offering". "700 horsepower" Ilmor V8. "Our fastest, loudest, most thrilling program" | GTX card says "Stock car. 700 hp Ilmor V8". No partner or year on screen |
| "Perfect for someone new to racing" | Not found | Not used |

## Version A (public): 1920x1080, 61.9s

| # | Time | On screen | Visual | Assets | Source |
|---|---|---|---|---|---|
| 1 | 0:00.0 to 0:03.9 | "Anyone can drive fast." then hard cut: "RACING / IS HARD." | Black. Thin red speed line sweeps. Light Source Sans words blur in, then "RACING" tracks in and "IS HARD." slams in red. Engine rev under it | sfx engine-rev-1, whoosh-3 | |
| 2 | 0:03.9 to 0:06.8 | "What if you learned where *champions* learned?" | Mustang GT panning shot with speed streaks, slow push-in, words blur in | mustang-gt-track-03.jpg | /Race-Series, /testimonials |
| 3 | 0:06.8 to 0:10.2 | 400,000+ / Skip Barber alumni | Tachometer ring: ticks light up, sweeps into the redline as the number rolls | | Home page: "Over 400,000 Alumni" |
| 4 | 0:10.2 to 0:13.1 | Logo. "Since *1975*." | Logo glow reveal on black on the drop, with a red flash cut | skipbarber-logo.png, whoosh-1 | Home page: "In 1975, racing legend Skip Barber founded a school..." |
| 5 | 0:13.1 to 0:16.9 | "From our *classroom* to" then FORMULA 1. INDYCAR. IMSA. NASCAR. one per beat, then all four in a row | Red gradient intro, then each series slams over a darkened photo flash | f4-pack-limerock-01.jpg, f4-side-by-side-sebring.jpg, mustang-gt-pack-01.png, gtx-stock-car-01.png | /Race-Series, /testimonials |
| 6 | 0:16.9 to 0:22.7 | "Pick your *car*." Cards: Skip Barber GT (Built from a road-going Ford Mustang), Skip Barber Formula (Mygale FIA F4. 60 mph in under 4 seconds), Skip Barber GTX (Stock car. 700 hp Ilmor V8) | White scene, three floating cards with photos. Cursor clicks Formula, "Selected" tag | mustang-gt-track-05.jpg, f4-track-02.png, gtx-stock-car-01.png, click | /gt-car, /formula-car, /gtx |
| 7 | 0:22.7 to 0:28.5 | "Pick your *path*." One Day: Classroom, then lead-follow laps on track. Three Day [Most popular]: The path toward an SCCA or USAC racing license. Two Day Advanced: For Three Day graduates and experienced drivers. | Red gradient. A white progression line draws left to right and climbs, like Outrank's chart; cards land on each node | | /programs |
| 8 | 0:28.5 to 0:36.3 | 01 "*Learn* the line." Braking marks / Turn-in points / The apex. 02 "*Find* your limit." Your lines / Brake application / Throttle application. 03 "*Race*." Passing exercises / Practice race starts / Open lapping | Full-bleed photo per step. A 3D tilted white card flies in from depth and leaves left, Outrank calendar style | classroom-01.jpg, mustang-gt-braking-01.png, f4-side-by-side-sebring.jpg, whoosh-2 | /programs (quotes in code comments) |
| 9 | 0:36.3 to 0:40.6 | "On the path to your *license*." Badge: SCCA & USAC / Licensed Racing School / The Three Day puts you on the path to an SCCA or USAC racing license. | Red gradient, floating badge card, shield stamps in | | Home page, /programs |
| 10 | 0:40.6 to 0:46.0 | "The finest tracks in *America*." Chips: VIRginia International Raceway, Sonoma Raceway, Sebring, Lime Rock Park, Circuit of the Americas, Laguna Seca, NJMP. Eyebrow: "2027 programs on sale now at VIR and Sonoma" | Full-bleed track photos cycling (VIR, Sonoma, COTA), chips pop in one by one | mustang-gt-vir-01.jpg, track-sonoma-startline.png, track-cota-pitlane.jpg | Home page, track pages |
| 11 | 0:46.0 to 0:51.8 | "A bucket-list *gift*." then "Or the start of a *career*." | Split screen with a glowing red divider that slides from the student to the driver in race gear | smiling-student-helmet.png, driver-race-gear-trophy.png | Home page |
| 12 | 0:51.8 to 0:56.1 | "Get on *track*." Pill button: "Lock in your spot" | Darkened fleet photo, cursor clicks the pill, it fills red and glows | fleet-shop-overhead.png, click | Site button copy "LOCK IN YOUR SPOT!" |
| 13 | 0:56.1 to 1:01.9 | Logo. "The world's largest *racing school*." skipbarber.com | End card on black, fades out | skipbarber-logo.png | /VIR: "the world's largest racing school" |

## Version B (internal pitch, "Concept"): 1920x1080, 86.6s

Same as A, with these inserted after scene 9. Every inserted scene has a "Concept preview" tag in the top right corner.

| # | Beats | On screen | Visual |
|---|---|---|---|
| B1 | 13 | "Not sure where to *start*?" AI Program Finder: experience (None yet / Some track days / I have raced), car (GT / Formula / GTX), goal (A gift / A license / A career). Result: THREE DAY RACING SCHOOL / FORMULA | White chat card, chips tapped one by one, dark result card |
| B2 | 12 | "50 years of coaching. Now *always on*." Skip Barber Coach, digital twin built from the Skip Barber curriculum. Q: "Where should I brake into Turn 1 at VIR?" Generic typed answer | Dark card, avatar placeholder, live voice waveform |
| B3 | 11 | "Your laps, *analyzed*." Best lap by session chart, labeled "Illustrative data". Notes: Carry more speed to the apex / Pick up the throttle earlier / Hit the same brake marker every lap | White dashboard card, line draws and climbs |
| B4 | 9 | "Your path, *personalized*." | Scene 7's path with a pulsing "You are here" on One Day and "Suggested next" on Three Day |
| P | 6 (before scene 12) | [PARTNER OFFER] placeholder | Dashed dark card, no partner named |

End card adds "AI by Arsenal Digital Holdings" under skipbarber.com.

"50 years" follows the site's "50 years of building champions" (/formula-car).

## Version A vertical (social): 1080x1920, 40.6s

| # | Time | Scene |
|---|---|---|
| 1 | 0:00.0 to 0:03.4 | Hook |
| 3 | 0:03.4 to 0:06.3 | 400,000+ counter |
| 4 | 0:06.3 to 0:08.7 | Logo, Since 1975 |
| 5 | 0:08.7 to 0:12.1 | Classroom to F1, IndyCar, IMSA, NASCAR |
| 6 | 0:12.1 to 0:16.9 | Pick your car (cards stacked vertically) |
| 8 | 0:16.9 to 0:23.7 | Learn / Find / Race |
| 10 | 0:23.7 to 0:28.1 | Tracks |
| 11 | 0:28.1 to 0:32.9 | Gift / career (top and bottom split) |
| 12 | 0:32.9 to 0:36.3 | CTA |
| 13 | 0:36.3 to 0:40.6 | End card |

## Music and pacing plan

- Track: "Sports Action Version 3 - Natural Emotions" by BombinSound (Pixabay, 1:07, about 124 BPM, energy jump about 10s in, not Content ID registered). Pending download.
- The logo (scene 4) is placed at 10.2s to land on the jump. The cut list will be re-snapped to the measured beat grid.
- A hard cut lands on a beat at every scene boundary. Slams in scene 5 land one per beat.
