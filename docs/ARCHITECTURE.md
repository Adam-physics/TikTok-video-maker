# Trick Trivia — autonomous TikTok production system

**Input:** an objective. *"Sell the screen-free family value of Trick Trivia."*
**Output:** a finished 1080×1920 MP4, captioned, scored, upload-ready — plus the
caption, hashtags, and a record of what was sold and how.

Claude runs as director: strategist, creative director, writer, producer,
editor, and QA. This document is the design. Nothing in it assumes the
sandbox; it assumes a local machine with API keys and a budget.

---

## 0. The thesis

The tools are not the bottleneck. **Judgment is.** Video, image, voice, and
music generation are all good enough today to produce a finished piece from
text. What is *not* solved is taste: whether a hook stops a scrolling
parent, whether a beat is funny, whether a reveal lands. The system is
therefore built around three compensations for weak judgment:

1. **Structure over vibes.** Every decision — value proposition, concept,
   hook, shot, cut — is an explicit, inspectable artifact with a stated
   reason. Bad taste in a JSON file can be found and fixed; bad taste inside
   a single monolithic prompt cannot.
2. **Volume and selection.** Generate several concepts and keep one.
   Generate several takes of every AI shot and keep one. Post two finishes
   of the best concept, not one. Selection is where a vision model is
   genuinely strong (rejecting the bad) even where it is weak (predicting
   the great).
3. **A feedback loop with reality.** Every finished video is logged with
   what it sold, how, and later, how it performed. The director reads that
   ledger before choosing the next concept. Real posts are the only judge
   that matters; the system is designed to learn from them.

The second principle carried this whole session: every real defect in the
current pipeline was caught by rendering, extracting frames, and *looking*.
That loop is not an add-on. It is the core.

---

## 1. Pipeline

```
objective
   │
   ▼
[1] STRATEGY        pick the one parent value to sell in THIS video
   │                (reads brand bible + content ledger)
   ▼
[2] CONCEPTS        5–8 concepts, deliberately diverse on
   │                value × format × hook-type × emotional register
   ▼
[3] SELECTION       rubric-scored; top 1 (or 2 for A/B) advances
   │
   ▼
[4] SCRIPT          beats, lines, on-screen text, the reveal moment
   │
   ▼
[5] SHOT LIST       per shot: modality, prompt, duration, refs, audio needs
   │
   ▼
[6] ASSETS          fan-out to providers; N takes per shot; vision-select
   │
   ▼
[7] EDIT (EDL)      timeline: clips, VO, SFX, music, captions, graphics
   │
   ▼
[8] RENDER          Remotion composition → ffmpeg encode
   │
   ▼
[9] QA              frames + audio inspected against a written rubric
   │    └── fail → revise EDL / re-roll shots → [8]   (bounded, 3 passes)
   ▼
[10] DELIVER        MP4 + caption.txt + ledger entry
```

Each stage writes a file into `runs/<id>/`. A human can open any stage,
disagree, edit it, and resume from there. That is the intervention model:
not "tell Claude where to put text at second 3.2," but "the concept is
wrong, here is why" — once, in words, and the ledger remembers.

---

## 2. Persistent understanding: the brand bible

Lives in `brand/` and is loaded through `CLAUDE.md` so every session starts
already knowing the product. Nothing here is regenerated; it is maintained.

```
brand/
  product.md          facts: pages, count, categories, ages, price, ASIN, formats
  customer.md         who buys (parent, teacher, gift-giver), when, why, objections
  value-props.md      THE list — each with: the parent's moment, the desire,
                      how to DEMONSTRATE it (never state it), example hooks,
                      example reveal lines
  voice.md            brand voice; what it never says; how it jokes
  visual.md           palette, fonts, the illustration style described in
                      words precise enough to prompt an image model
  amazon-listing.md   the live listing text, verbatim
  reviews.md          verbatim reviews, each tagged with the value prop(s) it
                      proves — the single richest source of hook language,
                      because it is real parent phrasing
  assets/             pages, cover, character sheets, product photos
  formats.md          the format library (see §5)
  ledger.json         every video made: objective, value prop, format, hook
                      type, concept summary, run id, and later, performance
  learnings.md        what worked, what did not, in plain language
```

`reviews.md` deserves emphasis. "Kept them busy for two hours in the car"
is a better hook than anything a model invents, and it is true. The
strategy stage mines it.

---

## 3. The director's process, stage by stage

**Strategy.** Given the objective, choose exactly one value to sell. Read
`value-props.md` for the menu, `ledger.json` for what has been covered and
what performed, and `customer.md` for who is scrolling. Output
`strategy.json`: the value, the parent's moment, the desired subconscious
thought ("my kid would love doing this to me"), the reveal timing (early,
late, or never-until-end), and the emotional register (funny, warm,
competitive, sneaky-educational). Rule: if the strategy could be
paraphrased as "here is our book," reject it and try again.

**Concepts.** Produce 5–8. The prompt demands divergence along explicit
axes and reads the ledger to avoid repeats. Each concept states its hook
(visual + on-screen text, which must agree), its format from the library,
its demonstration mechanism (what the viewer *experiences*), its reveal,
and its production risk (which shots need AI humans, dialogue, continuity).

**Selection.** A rubric, scored 1–5 each, weights in brackets:
hook specificity and stakes [3]; demonstrates rather than states [3];
feels native to the feed, not like an ad [2]; the reveal earns itself [2];
novelty against the ledger [1]; production risk, inverted [2]. Top concept
advances; when scores are close, the top two are both produced. **Honest
limit:** a model is reliable at rejecting weak concepts and unreliable at
predicting the winner. Selection prunes; posting decides.

**Script.** Beats with timings, every spoken line, every on-screen line,
the moment the book appears and how. Written against `voice.md`. Kallaway's
ordering applies: visual hook, then text hook, then spoken — and all three
aligned in the first second.

**Shot list.** For each beat, one or more shots. Each shot declares a
*modality* (see §4), a generation prompt, duration, reference images for
character/style consistency, a fallback modality if generation fails, and
its audio needs (VO line, SFX cue, music mood).

**Assets.** Fan out. Every AI shot is generated 3× and a vision pass picks
the take with the fewest artifacts, correct framing, and continuity with
its neighbours; a shot with no acceptable take is regenerated with a
revised prompt, then falls back to its declared alternative. VO is
generated, then transcribed back with word timestamps for captions.

**Edit.** An edit decision list: clip in/out, transitions, caption events
with word timing, SFX placement, music with ducking under VO, overlays and
graphics, the safe-zone constraints. The EDL is data; the renderer is
dumb. That is what makes revision cheap.

**Render.** Remotion composes (React: typography, motion graphics, caption
animation, overlays are all first-class); ffmpeg encodes to H.264/AAC,
1080×1920, faststart.

**QA.** See §6.

---

## 4. Providers and modalities

Accessed through a thin adapter layer (`providers/`) so a model can be
swapped without touching the director. Use **fal.ai** (or Replicate) as the
gateway for video and image models: one key, one billing, many models,
and new ones appear there first.

| Need | Primary | Alternates | Notes |
|---|---|---|---|
| Director, vision QA | Claude (Fable / Opus) | — | Reads frames; writes every stage artifact |
| Text → video, people, dialogue | Google Veo 3.x | Sora 2, Kling 2.x/3, Runway Gen-4 | Veo and Sora generate speech + lip sync natively; strongest for skits |
| Image → video, motion, stylized | Kling | Veo, Runway, Seedance, Hailuo | Cheaper per second; good for animating illustrated stills |
| Character consistency | Reference-to-video (Veo "ingredients", Kling "elements", Runway references) | Character sheet + image-to-video | Seed one character sheet, reuse across every shot |
| Stills | Flux (Kontext for edits) | Imagen 4, GPT-image, Ideogram | GPT-image for legible text; Flux Kontext to keep a character across stills |
| Voice | ElevenLabs v3 | OpenAI TTS | Expressive; per-character voices; cheap fallback |
| SFX | ElevenLabs SFX (text → sound) | Freesound | "kid losing it laughing," "buzzer," "page flip" on demand |
| Music | ElevenLabs Music / Suno / Stable Audio | trending in-app | Always deliver a music-free mix too; adding trending audio in-app is often better for reach |
| Stock | Pexels (free) | Storyblocks | Road, car interior, dinner table B-roll |
| Captions / alignment | whisperX | ElevenLabs alignment | Word timestamps from the VO itself |
| Render | Remotion + ffmpeg | MoviePy | Remotion for anything typographic or animated |
| Loudness / audio checks | ffmpeg ebur128, loudnorm | — | Deterministic; no model needed |
| Performance data | TikTok analytics export | Research API (limited) | Fed back into the ledger by hand or script |

**The ledger is the most important "provider."** It is the only source of
truth about what actually sells.

### Two lanes for people on screen

The best concepts involve a kid and a parent. There are two ways to get
them, and this is a strategic choice, not a technical one:

**Lane A — illustrated characters in the book's own style.** A character
sheet for the kid and the dad, drawn in the comic style of the pages;
scenes generated as stills in that style and animated with image-to-video;
dialogue by TTS. Consistency is easier (one style, one sheet). No uncanny
valley. No synthetic child. On-brand to the point of being *the brand*: the
book came to life. Recommended as the primary lane.

**Lane B — photoreal AI people.** Veo/Sora skits with generated actors.
This is what "AI UGC" looks like and it can convert, because UGC is the
native grammar of #amazonfinds. Risks are real: viewers — parents above
all — are sharp at spotting synthetic humans, and a fake family selling a
children's product is a trust problem if it reads as fake. Synthetic
children specifically are restricted by some providers and are a policy
and ethics line to decide deliberately. TikTok requires AI-generated
content labels for realistic synthetic media, and Veo/Sora output carries
provenance metadata. Use Lane B for adult-only or hands-and-book shots,
test it honestly, and label it.

---

## 5. Variety: formats as grammars, not templates

`formats.md` is a library of production grammars. Each entry describes the
shape (beats, pacing, typical length), what it is good at selling, its
shot vocabulary, and its asset needs. It is guidance for the director, not
a fill-in-the-blanks. A starting library:

- **POV skit** — "POV: you found the thing your kid puts the iPad down
  for." Kid vs parent, escalating. Sells: screen-free, family bonding,
  kids outsmarting adults.
- **Viewer participation** — the viewer is quizzed, reasons, is surprised.
  "You just learned three things because a children's book tricked you."
  Sells: learning without homework, knowledge that sticks.
- **Situation → rescue** — "2 hours into a 7-hour drive." Sells: road trip,
  zero setup.
- **Mock interface** — a text thread, a group chat, a notes-app list.
  Sells: relatability, conversation.
- **Review montage** — real parent lines, typographic, fast. Sells: proof.
- **Animated explainer** — one fact, why it is true, in the book's style.
  Sells: curiosity.
- **Reaction / stitched-style** — a "reaction" to a claim card. Sells:
  debate, defending an answer.
- **Day-in-the-life fragment** — dinner table, restaurant wait, bedtime.
  Sells: the everyday moment.
- **Carousel** — the Photo Mode listicle already built. Sells: the game
  itself, saves and shares.
- **ASMR / tactile** — page flips, the physical object. Needs real
  product footage. Sells: it's real, it's tangible.

The ledger tracks format × value × hook-type. Concept generation is told
what has been done and asked to diverge. "Ten videos" means ten cells in
that matrix, not ten variations of one.

---

## 6. Self-inspection and revision

After every render the system produces and reads:

- **A contact sheet** (every 0.5s) and **full frames at each beat** —
  inspected by the vision model against a written rubric: hook legible in
  frame one; text inside safe zones (deterministic check too); no text
  overflow or orphaned words; captions match the VO; character continuity
  across adjacent AI shots; visible generation artifacts (hands, garbled
  text, morphing); the book is on screen when the script says it is.
- **Audio measurements** — integrated loudness and true peak (ffmpeg
  ebur128); VO intelligibility by re-transcribing the mix and diffing
  against the script; silence gaps; music ducked under VO.
- **Pacing measurements** — average shot length, longest static span,
  time to first cut, time to reveal.

Failures produce a revision to the EDL (retime, swap a take, shrink text,
move a caption) or a re-roll of a shot with a revised prompt, then a
re-render. Bounded to three passes; if still failing, the run stops and
says exactly what is wrong, with frames attached.

**What this catches reliably:** everything mechanical and most things
visual. **What it does not:** whether it is funny, whether the timing
*feels* right, whether a parent would stop. Those come from posting.

---

## 7. What stays human

- **Keys and budget.** You decide the ceiling; the system reports spend per
  run.
- **Brand truth.** Reviews, the cover, product photos. Ten minutes with a
  phone on the physical book — pages turning, the cover on a car seat, a
  hand holding it at a table — produces footage no generator matches and
  every format can reuse. This is the highest-value thing you can give it.
- **The taste gate, at first.** Watch each finished video; reply approve,
  or one sentence of why not. That sentence goes to `learnings.md` and the
  ledger. The gate shrinks as the ledger grows.
- **Policy lines.** Whether to use photoreal AI people; whether ever to use
  synthetic children (recommendation: no); AI labelling.
- **Posting and performance.** TikTok's posting API requires an approved
  app; assume manual or a scheduler. Export analytics periodically; a
  script folds them into the ledger.

Everything else — strategy, concept, script, assets, edit, render, QA,
caption, hashtags — is the system's job.

---

## 8. Realistic capability, today

| Format lane | Hands-off finish rate | Post-ready without touching |
|---|---|---|
| Typography / motion graphics / book assets / VO | ~95% | ~85% |
| Illustrated characters (Lane A) | ~90% | ~65% |
| Photoreal AI skits with dialogue (Lane B) | ~85% | ~35–50% |

"Finish rate" is: an MP4 comes out. "Post-ready" is: you would upload it
as is. The gap is mostly AI video reliability — a skit with six shots of
the same two people, lip-synced, with comedic timing, will get there on
some runs and need a re-roll on others. The system is designed to re-roll
on its own; the numbers above are per attempt, not per concept.

Cost, rough, per finished 30-second video: **$3–8** with no AI video;
**$15–45** with ~20 seconds of AI footage at three takes per shot. A batch
of ten across mixed formats: roughly $150–350 and one to three hours
wall-clock with generation in parallel.

These numbers move monthly, in the right direction.

---

## 9. Repository shape

```
CLAUDE.md               loads brand/ and the process
brand/                  §2
docs/ARCHITECTURE.md    this file
director/               the staged process: strategy, concepts, select,
                        script, shots, edl, qa — each a Claude-driven step
                        with a schema-validated output
providers/              adapters: fal (veo, kling, flux…), elevenlabs,
                        pexels, whisperx — one interface per modality
render/                 Remotion project + ffmpeg encode
formats/                the grammar library, one file each
runs/<id>/              every stage artifact, assets, renders, qa reports
trivia/                 the current page-crop / carousel tooling (kept as
                        a modality: "book assets")
.claude/skills/tiktok   the entry point: /tiktok "<objective>" [--count N]
```

---

## 10. Build order

1. Brand bible + ledger + the `/tiktok` skill with the staged process,
   producing every artifact through *script* with no rendering. Read them.
   Fix the judgment before spending on pixels.
2. Provider adapters and the Remotion renderer; first lane: typography,
   book assets, VO, captions, music. Everything from this session ports in.
3. Lane A: character sheets in the book's style; stills; image-to-video;
   the POV skit format end to end.
4. QA loop with bounded revision.
5. Batch mode, ledger-driven diversity, the ten-video run.
6. Lane B, tested and labelled, if the ledger says photoreal UGC is worth it.
