# Jaded London: website teardown and rebuild (handoff)

Paste the **"Prompt for the new session"** section below into a fresh Claude Code
session. Do the setup steps first.

---

## 1. Settings to turn on before starting the new session

### Cloud environment (claude.ai/code → environment menu in the title bar → Edit)

| Setting | Value | Why |
|---|---|---|
| **Network access** | **Full** | Needed to load the competitor sites (Balenciaga, Corteiz, Represent, etc.) and Shopify image CDNs. In the previous session "Full" did not apply mid-session, so **set it first, then start a NEW session.** |
| If you must use *Limited* instead | Add to Allowed domains: `jadedldn.com`, `challenges.cloudflare.com`, `cdn.shopify.com`, `balenciaga.com`, `www.balenciaga.com`, `corteiz.com`, `representclo.com`, `acnestudios.com`, `ssense.com`, `vetements.com`, `ottolinger.com`, `kidsuper.com`, `jaded-london.myshopify.com`. Keep **Allow package managers** ticked. | Minimum set for the job |
| Repository | `adam-physics/tiktok-video-maker`, branch `claude/gracious-gates-0kf5oe` | This handoff file plus the Chrome scrape output live in `jaded-london/` |

Docs: https://code.claude.com/docs/en/cloud-environments#network-access

### What will still block Claude (even on Full)
- **jadedldn.com sits behind a Cloudflare "Verify you are human" CAPTCHA** for automated browsers. Claude Code won't (and shouldn't) bypass it. **Use Claude in Chrome (see `CHROME_PROMPT.md`)**: it runs in *your* real browser, so the check passes normally.
- **web.archive.org** reset every connection from the cloud container. Don't rely on it.

### Claude in Chrome extension
- Install / sign in: Chrome Web Store → "Claude" (Claude in Chrome).
- Before running the prompt, open jadedldn.com yourself once and pass the Cloudflare check.
- Site permissions: allow it on `jadedldn.com` (and the competitor sites if you want it to screenshot those too).
- Set the region to **United States / USD** in the site's country selector so prices match the `/en-us` store.

---

## 2. Workflow

1. Change the environment settings above.
2. Run `CHROME_PROMPT.md` in Claude in Chrome. It produces:
   - `jaded_inventory.md` (all copy, nav, pages, collections, products, prices, image URLs)
   - the raw Shopify JSON files (`products_p1.json`, `products_p2.json`, …, `collections.json`)
   - screenshots (desktop and mobile) of the key templates
3. Put everything it produced into `jaded-london/scrape/` in this repo. Easiest ways:
   - drag the files into the new Claude Code session's chat, **or**
   - on GitHub: open the repo → branch `claude/gracious-gates-0kf5oe` → `jaded-london/` → *Add file → Upload files* → put them in `scrape/`.
4. Start a NEW Claude Code session (so the Full network setting applies) and paste the prompt below.

### Quick manual fallback (no extension, 2 minutes)
In your normal browser, open each of these and press **Ctrl/Cmd+S** (save as `.json`):
- `https://jadedldn.com/products.json?limit=250&page=1` (then `page=2`, `page=3`… until you get `{"products":[]}`)
- `https://jadedldn.com/collections.json?limit=250`
- `https://jadedldn.com/pages.json` (may 404; fine)

These hold **every product, price, variant, description and image URL** on the store.
Then **Save Page As → Webpage, Complete** on the homepage, one collection page,
one product page, the Parachute page and the Stores page.

---

## 3. What we already know (from the previous session's research)

- **Brand:** Jaded London, founded 2013 by siblings **Jade and Grant Goulden**. Womenswear, menswear, swimwear.
- **Identity:** Y2K, rave and club culture, "sexy, day-to-night", rhinestones, tribal graphics, Japanese streetwear and hip-hop references (Forbes, Sept 2025). The "Smoke Room" rave installation shows up in their NYC activations.
- **Hero product:** **Parachute Cargo Pants** (unisex cut, M-51/M-65 field pant reference). About **$130 US / £65 UK**. Dedicated landing pages exist:
  `/pages/the-parachute-pant-jaded-london`, `/pages/the-parachute-pants-womens`, `/pages/the-parachute-pants-mens`.
- **Other content pages seen:** `/pages/sleazenation` (Nov 2023 Sleazenation archive collab), `/pages/ldn-to-nyc` (NYFW / VFILES pop-up),
  `/pages/rock-revival-collaboration` (2026 denim collab, second one), `/pages/new-york-store-2026` (**NYC store, 434 Broadway**).
- **Collections seen:** `new-in-all`, `new-in-womens`, `new-in-mens`, `womens-cargo-pants`, `mens-cargo-pants`, `mens-all`, `mens-trousers`; filter facets like *Baggy Jeans*, *Bootcut Jeans*.
- **Campaigns:** AW26 ("raw, industrial, editorial", via Visie), SS26 sports campaign.
- **Stockists:** ASOS, Urban Outfitters, Flannels.
- **Platform:** Shopify (Markets, with `/en-us` locale), behind Cloudflare.
- **Criticism to design around:** commentators call it trend-chasing / "no art direction" / fast fashion (The Gryphon, Apartstyle). The rebuild should give the brand a **stronger art direction** without making it look "luxury beige".
- **Balenciaga:** there's no known collab. "Something like Balenciaga" almost certainly means the **website's design language**: the Demna-era balenciaga.com (stark, near-brutalist UI; huge product imagery; tiny utilitarian type; black/white; full-bleed video; product grids as the homepage; "drops" treated like art releases).

---

## 4. Prompt for the new session (copy everything in the block)

```
Read jaded-london/HANDOFF.md and everything in jaded-london/scrape/ in this repo
(branch claude/gracious-gates-0kf5oe). These are the scraped contents of
jadedldn.com (Shopify store, US market), gathered with Claude in Chrome because
the site has a Cloudflare CAPTCHA. Don't try to bypass that CAPTCHA. Use the
scrape files, and fetch images directly from cdn.shopify.com where needed.

Goal: analyse the Jaded London website against better-in-class fashion
e-commerce sites and produce a full rebuild plan that keeps ALL current
content (products, prices, copy, images, collections, campaign/collab pages,
stores, policies) but is a much better website. It must meet the highest
industry standard WITHOUT losing the brand's niche: Y2K / rave / club /
London streetwear, sexy day-to-night, a big social-media brand. The
client reportedly wants it to feel "like Balenciaga". Interpret that as
the Demna-era balenciaga.com design language and say how far to push it
before it stops feeling like Jaded.

Do this:
1. Inventory: from the scrape, build a structured content inventory
   (sitemap/IA, nav, collections, product count, price ranges, templates,
   campaign pages, image counts, apps/integrations you can spot).
2. Audit the current site: IA, navigation, homepage, PLP, PDP, cart,
   search, mobile, performance (image weights, scripts), accessibility,
   SEO (titles, structured data, duplicate URLs like /en-us vs root),
   brand expression, and conversion patterns. Back every point with
   evidence from the scrape or screenshots.
3. Benchmark live against: balenciaga.com, corteiz.com, representclo.com,
   acnestudios.com, vetements.com, ottolinger.com, ssense.com, kidsuper.com,
   plus one Gen-Z volume player (e.g. ihateblue / Minga / Motel Rocks if
   reachable). For each: what they do better, with screenshots where
   possible, and what Jaded should and shouldn't copy.
4. Brand definition: derive what Jaded "is / is not" from their site copy,
   campaigns (AW26 industrial editorial, SS26 sport, Smoke Room, Sleazenation,
   Rock Revival, NYC 434 Broadway) and social presence (TikTok/Instagram).
5. Rebuild plan: IA and sitemap, page-by-page wireframes (home, PLP, PDP,
   drop/campaign, collab, stores, account), design system (type, colour,
   grid, motion, imagery rules), "Balenciaga dial" (what to take vs. leave),
   tech stack (Shopify Hydrogen vs. Online Store 2.0 theme: recommend one),
   performance and accessibility targets, SEO and Markets plan, content
   migration map (old URL → new URL, every page and asset), social/UGC
   integration, drop mechanics (countdowns, waitlists), and a phased
   roadmap.
6. Build a clickable HTML prototype of the new homepage, one PLP and one
   PDP using the REAL products, copy and cdn.shopify.com images from the
   scrape, and publish the report and prototype as an Artifact I can share.

Save working files under jaded-london/, commit and push to
claude/gracious-gates-0kf5oe. Cite sources.
```
