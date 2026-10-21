# Jaded London rebuild: competitor website benchmark

Captured 2026-10-21 using headless Playwright Chromium from a cloud container (desktop 1440x900 at DPR 1, mobile 390x844 at DPR 2, Chrome 141 user agents). The raw numbers are in `metrics.json`. Screenshots are in `shots/`, named `<site>-<page>-<device>[-full].jpg`.

**How to read the numbers**
- **Weight and requests:**
  - *Initial* is the load event plus 6 s, with no interaction.
  - *Total* is measured after dismissing the cookie banner and scrolling to the bottom of the page.
  - Byte counts are encoded transfer sizes.
- **LCP:** each figure is one cold lab run. Read them as indicative, not as field data.
- **Third-party script domains:** distinct registrable domains serving scripts that are not the site's own. Shopify's `shopify.com` and `shop.app` count as third-party.
- **Video:** this Chromium build cannot decode H.264. Autoplay video heroes therefore show up blank, grey or as a poster frame in the screenshots (Motel, Ottolinger, Acne). Video presence comes from the DOM `<video>` elements.
- **Jaded context:** `../scrape/meta.json` shows Jaded on Shopify with 2,058 published products and 532 published collections. That is far more SKUs than any brand-only site below, so filtering and search matter more for Jaded than for most of them.

**Access summary**

| Site | Live capture? | Notes |
|---|---|---|
| balenciaga.com | **No: blocked** | Returned HTTP 403 "Access Denied" to a real Chromium with a desktop UA (`shots/balenciaga-home-desktop-BLOCKED.jpg`). WebFetch was also refused. Not retried or bypassed. The section below is web-researched. |
| ssense.com | Yes | A default headless UA got a 403 "Just a moment..." challenge in a connectivity test. The normal desktop-Chrome-UA run loaded with no challenge, and nothing was solved or bypassed. |
| corteiz.com | Partly | Every URL, including `/collections/all`, redirects to `/password`. Only the gate page is visible. |
| vetements.com | Partly | Holding page only. Shop links go out to SSENSE. |
| ihateblue.com | **No: unreachable** | The egress proxy returned 502 on CONNECT for both `ihateblue.com` and `www.ihateblue.com`. |
| All others | Yes | Home, PLP and PDP captured on desktop and mobile. |

---

## 1. Balenciaga (balenciaga.com): NOT CAPTURED LIVE

The live site blocked the automated browser (`shots/balenciaga-home-desktop-BLOCKED.jpg`). Everything here comes from published sources. None of it was observed by me.

- **2017 redesign:** Bureau Borsche rebuilt the site in 2017 under Demna. The layout was "stripped back... to a basic grid system" with imagery "focused purely on the products", giving it a "uniform, catalogue-like" feel. Brand presence was minimal, with the logo "placed modestly in the top-left corner". The article quotes a stated aim of being "utterly brilliant in its simplicity and superbly user-friendly". Source: [It's Nice That](https://www.itsnicethat.com/news/bureau-borsche-balenciaga-website-redesign-010317), and the studio's project page [bureauborsche.com](https://bureauborsche.com/projects/balenciaga/visual-identity).
- **Brutalist label:** HubSpot France lists the site as an example of brutalism, built on geometric structures with simplified typography and a white background. Source: [blog.hubspot.fr](https://blog.hubspot.fr/marketing/web-design-inspiration). Note this is a marketing blog, not design criticism.
- **Collections launched as media events:**
  - The FW21 collection was presented in December 2020 as a browser video game, *Afterworld: The Age of Tomorrow*, playable on any device, with the lookbook hosted on the website. Source: [Hero](https://hero-magazine.com/article/180958/balenciagas-fw21-collection-comes-with-an-online-video-game-set-in-2031/), [Input](https://www.inputmag.com/style/balenciaga-afterworld-the-age-of-tomorrow-video-game-fw21-collection).
  - In July and September 2021 the brand wiped its Instagram, Facebook and Twitter feeds around launches. Source: [FashionUnited](https://fashionunited.uk/news/fashion/did-balenciaga-erase-its-instagram-again/2021091257647), [Grazia](https://graziamagazine.com/us/articles/balenciagas-deletes-instagram-feed/).
- **The Demna era is over:** Pierpaolo Piccioli became creative director on 10 July 2025, succeeding Demna. Source: [LaPresse](https://www.lapresse.it/spettacoli/moda/2025/05/19/pierpaolo-piccioli-e-il-nuovo-direttore-creativo-di-balenciaga/), [Tag Walk](https://www.tag-walk.com/it/news/pierpaolo-piccioli-appointed-creative-director-of-balenciaga). I found no coverage of a Piccioli-era site redesign, so the current site's look is unverified.
- **No live metrics.** Weight, LCP, JSON-LD and so on were not measured.

**What they do better (per sources)**
- A strictly product-only, catalogue-style grid.
- The logo is demoted.
- Launches are treated as cultural events: a game, social feed wipes.

**Jaded should copy**
- The idea of a launch as a media event, such as a microsite or interactive drop.
- A consistent catalogue grid on PLPs.

**Jaded should not copy**
- The near-absence of brand signalling. It works for a heritage house that everyone already knows, not for a brand that needs to say "rave" in one second. See the "Balenciaga dial" section at the end.

---

## 2. Corteiz (www.corteiz.com)

**Shots:** `corteiz-home-desktop.jpg`, `corteiz-home-mobile.jpg`. Nothing else is reachable: every path redirects to `/password`.

**Measured**

| Measure | Value |
|---|---|
| Weight (desktop) | 164 requests / 1.44 MB initial; 197 / 1.53 MB total |
| Third-party script domains | 7 (Shopify, shop.app, Klaviyo, minmaxify, Heroku-hosted app, chimpstatic, Cloudflare) |
| LCP | 1.8 s desktop, 1.7 s mobile (the logo `div`) |
| Title | "CRTZRTW" |
| Meta description | None |
| JSON-LD | None |
| h1 | 1 (empty) |
| `lang` | `en` |

**Observed design**
- A black full-screen gate with the white Alcatraz logo.
- An EMAIL field with a yellow SUBMIT button, plus a padlock "PASSWORD" link.
- Type is Courier New throughout: 12 px body, 25 px h1. Colours are `#000` background and `rgb(255,213,0)` yellow.
- No nav, no products and no social links on the page.

**Drop mechanics (cited):**
- The site is password-protected and is "the only place to buy new product on drop days". Fans must "hunt down that password".
- Drops are "sporadic, highly-limited" and "typically sell out in minutes".
- The Instagram account is private.

Source: [Love Creative](https://lovecreative.com/blog/3x-ways-corteiz-is-breaking-all-the-rules). Another source says the password is shared on social media and sometimes chosen by fans: [Opumo](https://www.opumo.com/magazine/corteiz-meet-the-label-behind-streetwears-second-coming).

**What they do better**
- The site is the drop. It is the lightest page in this set (1.5 MB) and has a single action: give an email or enter the password.
- The scarcity mechanic is the brand.

**Jaded should copy**
- A Shopify password/gate template for *specific* drops, for example a "rave capsule" with a password released on TikTok live.
- Email and SMS capture as the only action on the gate.
- A tiny page weight on that gate.

**Jaded should not copy**
- Locking the *whole* store. Jaded sells 2,058 products continuously, and a site-wide gate would kill organic traffic.
- No SEO metadata at all.
- Hiding social links. Jaded's growth channel is TikTok.

---

## 3. Represent (representclo.com, served as the US store)

**Shots:**
- Home: `representclo-home-desktop.jpg`, `-full.jpg`, `representclo-home-mobile.jpg`, `-full.jpg`
- PLP: `representclo-plp-desktop.jpg`, `-full.jpg`, `representclo-plp-mobile.jpg` (/collections/mens-new-arrivals-all)
- PDP: `representclo-pdp-desktop.jpg`, `representclo-pdp-mobile.jpg` (Owners Club Hoodie)
- Gated sale: `representclo-vault-desktop.jpg`, `representclo-vault-mobile.jpg` (/collections/vault)

**Measured**

| Measure | Value |
|---|---|
| Home weight (desktop) | 462 requests / 7.6 MB initial; 531 / 8.1 MB total |
| Home JS | About 4.0 MB of the home page is JavaScript (resource breakdown) |
| Third-party script domains | **41 on home, the most in this set.** Includes Klaviyo, Attentive, Yotpo, LoyaltyLion, Wisepops, Ometria, Upfluence, Social Snowball, Trustpilot, Signifyd, Datadog, StackAdapt, Webgains, DoubleClick and TikTok. |
| LCP | Home 3.1 s desktop / 1.5 s mobile. PDP 1.7 s / 1.4 s. |
| JSON-LD (home) | Organization, WebSite/SearchAction, BreadcrumbList |
| JSON-LD (PLP) | CollectionPage and ItemList |
| JSON-LD (PDP) | Product, Offer, MerchantReturnPolicy, OfferShippingDetails, Brand, BreadcrumbList. The cap PDP also has AggregateRating. |
| h1 | Home h1 is the SEO title string at 12 px |
| Images without `alt` | 8 of 48 on home |

**Observed design**
- **Nav:** Represent / 247 / Outlet on the left, the wordmark in the centre, and Retail / The Vault / Prestige / US-USD / notifications bell / search / account / cart on the right.
- **Home:** a split two-tile hero, one tile per sub-brand ("Represent" and "247 Activewear"), each with two CTAs including "247 FW26 DROP 2". The page then goes almost straight to the footer: home height is 1,263 px.
- **Type and colour:** STKBureau throughout, on white with black text.
- **PLP:**
  - A "Featured Collections" card row sits above the grid.
  - There is a grid-density toggle and a **"Model" toggle** that switches between on-model and packshot images.
  - Filters sit in a "Filter & Sort" drawer.
  - 245 products with a load-more control.
  - Visually 4 columns on desktop and 2 on mobile. The DOM heuristic said 10 because of the collection carousel.
- **PDP:**
  - Image carousel with a "1/10" counter and model height and size info.
  - Colour swatches as product thumbnails, with "More Colors".
  - Size buttons, a "Size Chart" link and a **"Find your perfect size"** fit tool.
  - Black ADD TO CART button.
  - **A delivery date estimate keyed to a ZIP code** ("Fastest Delivery Thu, Oct 22 to Fri, Oct 23 to 94104").
  - Prestige loyalty points ("Earn 200 Prestige Points") and Afterpay instalments.
  - Accordions for details, FAQs and returns. "You may also like" cross-sell.
  - ATC stays visible after scrolling on mobile.
- **Drop mechanics:**
  - "The Vault" is a gated sale. Its title reads "THE VAULT - IS CLOSED | SIGN UP FOR SALE DETAILS" and the page is an email sign-up.
  - Drops are numbered ("FW26 DROP 2").
  - A notifications bell sits in the header.
- **Social:** Instagram, TikTok, YouTube, X and Facebook links. Upfluence and Social Snowball scripts point to creator and affiliate programmes.

**What they do better**
- The most complete PDP in the set: a fit finder, a dated delivery promise, loyalty points, BNPL and the richest Product schema.
- A sub-brand split on the homepage.
- A gated "Vault" sale that turns discounting into an event.

**Jaded should copy**
- The ZIP- or postcode-based delivery date on the PDP.
- The model/packshot toggle on the PLP.
- A size-finder link next to the size buttons.
- Numbered drops ("DROP 2").
- A gated sale page that collects sign-ups when closed.
- Rich Product schema, including MerchantReturnPolicy and OfferShippingDetails, which help Google Shopping listings.

**Jaded should not copy**
- 41 third-party script domains and about 4 MB of JS on the home page.
- A homepage that is just two tiles and a footer, which leaves no product discovery on the home.
- The SEO title used as a 12 px h1.

---

## 4. Acne Studios (acnestudios.com, Salesforce Commerce Cloud; US locale served)

**Shots:**
- Home: `acnestudios-home-desktop.jpg`, `-full.jpg`, `acnestudios-home-mobile.jpg`, `-full.jpg`
- PLP: `acnestudios-plp-desktop.jpg`, `-full.jpg`, `acnestudios-plp-mobile.jpg` (/us/en/woman/new-arrivals/)
- PDP: `acnestudios-pdp-desktop.jpg`, `acnestudios-pdp-mobile.jpg` (Patchwork Denim Shirt)

**Measured**

| Measure | Value |
|---|---|
| Home weight (desktop) | 94 requests / 2.5 MB initial; 141 / 5.3 MB total |
| Third-party script domains | 12 (OneTrust, reCAPTCHA, Bloomreach, Riskified, Meta, TikTok, GTM and others) |
| LCP | Home 6.0 s desktop (a 1.17 MP video poster JPG) / 3.0 s mobile. PLP 1.6 s / 0.9 s. PDP 2.8 s / 4.9 s. |
| JSON-LD | Organization on home. PDP has ProductGroup, Product, Offer and BreadcrumbList. |
| Images without `alt` | 0 everywhere |
| Skip links | Present ("Skip to navigation / main content / footer") |
| PDP meta description | None |

**Observed design**
- **Nav:** WOMAN, MAN, DENIM, BAGS, SCARVES, then SEARCH / HELP / ACCOUNT / bag count "00".
- **Home:**
  - A **full-bleed autoplay muted video**: 1440x810 on desktop, 390x585 on mobile.
  - The title lockup "Acne Studios / Hussein Chalayan" over the video.
  - Below it, an editorial collaboration block, then category tiles, a "Discover more" product row and a news section.
- **Type:** Helvetica Now Text at 12 px for body and h1, with Helvetica Monospaced Pro as a secondary face. Black on white.
- **PLP:**
  - A sub-category text row.
  - "99 items" count and a single FILTER button that opens a drawer.
  - 4 columns on desktop, 2 on mobile, on a light-grey image background.
  - Colour swatches on hover with "10 Colours" counts.
  - An editorial tile inserted into the grid.
  - Load-more.
- **PDP:**
  - Large image stack on the left (vertical scroll); swipe carousel on mobile.
  - Size grid with **struck-through out-of-stock sizes** and "Out of stock? Get notified".
  - Blue full-width ADD TO BAG plus a wishlist heart. The ATC container is `position: sticky`.
  - "Free delivery & returns" with a postal-code delivery estimate, complimentary gift wrapping and "Pick up in store".
  - Size guide, accordions and a "Recommended" cross-sell.
- **Social:** Instagram, YouTube, X/Twitter, Facebook, Pinterest and Weibo links. No TikTok link was found, though the TikTok pixel loads.

**What they do better**
- The cleanest accessibility basics in the set: 0 missing `alt`, skip links and one h1 per page.
- The PDP pattern for out-of-stock sizes (strike-through plus "Get notified").
- Fast PLP LCP (0.9 to 1.6 s).
- Grid tiles that mix editorial content with product.

**Jaded should copy**
- Strike-through sold-out sizes with an inline notify-me link.
- Skip links and full `alt` coverage.
- Editorial tiles inserted into the PLP grid. For Jaded these could be TikTok clips or rave photos.
- A sticky ATC.
- Separate desktop and mobile video posters (`poster-d.jpg` and `poster-m.jpg`).

**Jaded should not copy**
- A 12 px base type size with h1 also at 12 px. It reads as "quiet luxury", not club.
- The 6 s desktop LCP from a heavy video poster.
- Missing meta descriptions on PDPs.

---

## 5. Vetements (vetements.com)

**Shots:** `vetements-home-desktop.jpg`, `vetements-home-desktop-full.jpg`, `vetements-home-mobile.jpg`

**Measured**

| Measure | Value |
|---|---|
| Weight | 130 requests / 1.18 MB |
| Third-party script domains | 2 (Wix `parastorage.com`, Sentry) |
| LCP | 1.7 s desktop / 1.2 s mobile |
| Title | "VETEMENTS Official Website of the Fashion Brand" |
| JSON-LD | WebSite only |
| h1 | 0 |

**Observed design**
- A white page with "NEW VETEMENTS WEBSITE COMING VERY SOON" in condensed bold caps, centred, plus Instagram and YouTube icons.
- The full page adds "SHOP WOMENSWEAR / SHOP MENSWEAR" links that point to **ssense.com**, along with SHOWS (vogue.com) and INSTAGRAM.
- Built on Wix. The text sample says "under creative direction of Guram Gvasalia".
- No PLP or PDP of its own exists.

**What they do better**
- Nothing to benchmark for e-commerce. It shows that a cult brand can outsource retail to a stockist and keep its own domain as a statement.

**Jaded should copy**
- At most, a deliberately blunt holding page during a relaunch, if one is needed.

**Jaded should not copy**
- Sending shoppers to a third-party retailer. Jaded's margin and data depend on its own Shopify checkout.

---

## 6. Ottolinger (ottolinger.com, Shopify backend with a Nuxt front end)

**Shots:**
- Home: `ottolinger-home-desktop.jpg`, `-full.jpg`, `ottolinger-home-mobile.jpg`, `-full.jpg`
- PLP: `ottolinger-plp-desktop.jpg`, `-full.jpg`, `ottolinger-plp-mobile.jpg` (/shop/all)
- PDP: `ottolinger-pdp-desktop.jpg`, `ottolinger-pdp-mobile.jpg` (4D Sneaker Heel)

**Measured**

| Measure | Value |
|---|---|
| Home weight | 109 requests / 1.9 MB initial; 171 / 3.9 MB total |
| PDP weight | 94 requests / 1.6 MB |
| Third-party script domains | **5** (Google, iubenda, gstatic, Pinterest, Meta) |
| LCP | Home 5.7 s desktop / 4.5 s mobile. PLP 3.7 s. PDP 3.3 s. |
| JSON-LD | WebSite, WebPage and Organization; Product and Offer on PDP. No BreadcrumbList. |
| h1 | **0 on every page** |
| Images without `alt` | **79 of 79 on home, 71 of 71 on PLP, 8 of 8 on PDP** |

**Observed design**
- **Nav:** a single text row of All, New Arrivals, Tops, Bottoms, Dresses, Outerwear, Accessories, Collections and Sale, with Search and Cart. A centred bold wordmark sits underneath. A black announcement bar reads "AUTUMN / WINTER 26 COLLECTION AVAILABLE NOW".
- **Home:**
  - **Product-grid-as-homepage.** A long 14,000 px scroll alternates cut-out product shots on white (3 to 4 across) with full-width campaign images and video bands. One campaign block is labelled "OTTONYMOUS".
  - There is a 1440x150 video strip at the top, which renders grey in the screenshot because of the codec.
- **Type:** Unica at **11 px** body on desktop (16 px on mobile). Black on white.
- **PLP:**
  - The label "All" with a single "Filters" toggle.
  - 4 columns on desktop, 2 on mobile, with cut-out images on white.
  - 69 products in one page.
- **PDP:**
  - A single centred product image on desktop, with more images further down.
  - Tiny text in the right column: name, price, fit note ("Fits large. Order one full size down"), and "Custom-made in our studio, each pair is one of a kind".
  - A size `<select>` dropdown and an outline "Add to cart" button.
  - Text links for Details / Payments / Shipping & returns / Contacts, and a "Similar items" cross-sell.
  - On mobile, the size select and Add to cart sit in a bar at the bottom of the viewport (`ottolinger-pdp-mobile.jpg`).
- **Social:** Instagram and TikTok links in the footer.

**What they do better**
- Very few third-party scripts and a light PDP.
- The homepage *is* the shop. Product is never more than one scroll away.
- Product copy is honest about fit.

**Jaded should copy**
- Interleaving campaign or video bands into a product grid on the homepage.
- A fit note directly under the price.
- A lean script budget.

**Jaded should not copy**
- Zero h1s and zero `alt` attributes. That is an accessibility failure and an SEO loss.
- 11 px body type.
- A size `<select>` dropdown instead of buttons.
- Outline-only ATC buttons with weak contrast.

---

## 7. SSENSE (ssense.com/en-gb)

**Shots:**
- Home: `ssense-home-desktop.jpg`, `-full.jpg`, `ssense-home-mobile.jpg`, `-full.jpg`
- PLP: `ssense-plp-desktop.jpg`, `-full.jpg`, `ssense-plp-mobile.jpg` (/en-gb/men/sale)
- PDP: `ssense-pdp-desktop.jpg`, `ssense-pdp-mobile.jpg` (Rick Owens cargo pants)

**Measured**

| Measure | Value |
|---|---|
| Home weight (desktop) | 52 requests / **13.6 MB initial; 71 / 19.7 MB total**. A single **11.8 MB animated GIF** (Cloudinary, `w_2048`) is the desktop LCP element, at 5.3 s. |
| Home weight (mobile) | 3.1 MB / 4.9 MB, LCP 1.5 s |
| PLP weight | 2.7 MB, LCP 1.2 s |
| PDP weight | 2.7 MB, **LCP 0.9 s** desktop |
| Third-party script domains | 5 on home (OneTrust, Cloudflare Insights, Datadog, Zendesk, Riskified); 11 on PLP and PDP |
| JSON-LD | Home has WebSite/SearchAction and Organization. PLP and PDP have Product, Brand and Offer. No BreadcrumbList. |
| h1 | 2 on PDP (duplicated); 0 on PLP |
| Home meta description | None |
| Images without `alt` | 0 (most carry `alt=""`) |
| `lang` | `en-gb` |

**Observed design**
- **Nav:** MENSWEAR, WOMENSWEAR, EVERYTHING ELSE, SALE and SEARCH on the left; centred "SSENSE" wordmark; ENGLISH / LOGIN / WISHLIST / BAG (0) on the right. A grey promo bar ("Get 20% off... code FALL26") sits above.
- **Home:**
  - An animated text banner ("SHOP A WORLD OF... WILLY CHAVARRIA... EMERGING DESIGNERS").
  - Giant "SHOP MENSWEAR / SHOP WOMENSWEAR" type links.
  - Editorial cards: the h1 is an article, "Looksmaxxing and the Quantification of Culture". A card titled "WHAT'S CRACKING" and a DJ photo from the Smerz live set at their PFW pop-up also appear.
- **Type:** "Favorit SSENSE Inter" grotesque at 11 px body, a 95 px display h1, and JHA Times Now serif for editorial. This matches the third-party extraction at [shadcn.io](https://www.shadcn.io/design/ssense/raw). Black on white.
- **PLP:**
  - A **left sidebar** with category links, then a long designer list with a "Search Designers" box.
  - A right column with SORT options and a COLORS list.
  - 4 columns on desktop. On mobile, 2 columns with REFINE and SORT buttons.
  - 120 products per page on white with no card chrome.
- **PDP:**
  - Three columns: description and composition on the left, a vertical image stack in the centre, and a "SELECT A SIZE" dropdown with ADD TO BAG and "Add to wishlist" on the right.
  - "Model is 6'1" and wears size 48. SIZE GUIDE".
  - Klarna messaging on mobile and "You may also like".
  - Sticky ATC on desktop.
- **Social:** Instagram, TikTok, X and Facebook links on desktop.

**Cited critique:** the filters are limited to designer, colour and size for a huge catalogue, and there is no scroll cue on the PDP images. Source: [Pratt IXD critique](https://ixd.prattsi.org/2023/09/design-critique-ssense/).

**What they do better**
- Editorial and commerce on one domain.
- Huge type used as navigation.
- PDP LCP under 1 s.
- Very few third-party scripts on home.

**Jaded should copy**
- Large display type as category links on the homepage.
- An editorial or "zine" block, which could be club-night recaps or DJ features.
- A tight script budget.
- A model height and size line on the PDP.

**Jaded should not copy**
- An 11.8 MB GIF hero. Use MP4/WebM or animated WebP/AVIF instead.
- A size dropdown.
- A duplicated h1.
- The thin filters noted in the critique. Jaded's 2,000+ SKUs need real facets.

---

## 8. KidSuper (kidsuper.com, Shopify)

**Shots:**
- Home: `kidsuper-home-desktop.jpg`, `kidsuper-home-mobile.jpg`, `kidsuper-home-mobile-full.jpg`. The desktop page scrolls inside a container, so there is no desktop full-page shot.
- PLP: `kidsuper-plp-desktop.jpg`, `kidsuper-plp-mobile.jpg` (/collections/all)
- PDP: `kidsuper-pdp-desktop.jpg`, `kidsuper-pdp-mobile.jpg` (Fur & Herringbone Coat)

**Measured**

| Measure | Value |
|---|---|
| Home weight (desktop) | 331 requests / 6.8 MB initial |
| PLP weight (desktop) | 390 requests / 8.6 MB |
| PDP weight | 4.5 MB |
| Third-party script domains | 9 on home (Square, Dub, Klaviyo, GTM, Meta, CloudFront and others) |
| LCP | Home 2.2 s desktop (a 1 MP PNG) / 3.4 s mobile. PLP 8.9 s desktop / 1.1 s mobile. PDP 1.4 s. |
| JSON-LD | Organization; PDP adds ProductGroup, Product and Offer. No BreadcrumbList. |
| Images without `alt` | 4 of 240 on home |
| Meta description | "a real company built on unreal ideas." |

**Observed design**
- **Header:** a periwinkle announcement bar reading "Oct 24th 2026 Birthday Bash Tickets Now On Sale!", so **event ticketing is promoted on the store**.
- **Nav:** a script-style logo, then ALL, AW26, SS26, CATEGORIES, COLLABS, MORE, CONTACT, USD, search, account and cart.
- **Home:**
  - A 5-slide artwork slideshow, including a painted football pitch for the Havaianas collab, with "Shop All KidSuper".
  - "AW26 Out Now" product rail and a 2x2 tile grid (KidSuper Faces / Shop AW26 / SuperSuits / AW Best Sellers).
  - Collab sections (BÉIS x KidSuper, Havaianas x KidSuper) and an embedded video player.
- **Type and colour:** Inter at 12 px body, with a "New York" serif h1 at 40 px. White background.
- **PLP:**
  - A horizontal filter bar (Price, Size, Availability, Category) with Sort and a grid-density toggle.
  - "1002 items".
  - **5 columns on desktop**, 2 on mobile.
  - Size availability is printed under each card (S M L XL XXL), with SOLD OUT badges.
- **PDP:**
  - A carousel with a vertical thumbnail column.
  - A **"Low stock"** indicator, size buttons and a black "Add to cart".
  - an Afterpay monthly-instalment line, a bullet-point spec list and a size chart accordion.
  - A **mobile bottom bar** with thumbnail, sizes and cart icon (`kidsuper-pdp-mobile.jpg`).
- **Social:** Instagram, TikTok, YouTube, X and Facebook links.

**What they do better**
- The brand's art and world is the merchandising.
- Events (birthday bash tickets) are sold alongside product.
- Size availability on PLP cards and low-stock urgency on the PDP.

**Jaded should copy**
- Selling or promoting **rave and club-night tickets** through the store bar. Jaded's club identity fits this.
- Size availability under PLP cards.
- Low-stock badges.
- A mobile sticky size and cart bar.
- Collab landing sections.

**Jaded should not copy**
- A heavy PNG hero (1 MP PNG as the LCP).
- The 8.9 s desktop PLP LCP.
- A homepage that scrolls inside a container, which breaks native scroll and full-page capture.

---

## 9. Motel Rocks (motelrocks.com, served as the US store, Shopify)

**Shots:**
- Home: `motelrocks-home-desktop.jpg` (the hero is a video, which renders blank here), `-full.jpg`, `motelrocks-home-mobile.jpg`, `-full.jpg`
- PLP: `motelrocks-plp-desktop.jpg`, `-full.jpg`, `motelrocks-plp-mobile.jpg` (/collections/new-in)
- PDP: `motelrocks-pdp-desktop.jpg`, `motelrocks-pdp-mobile.jpg` (Letiria Mini Dress)

**Measured**

| Measure | Value |
|---|---|
| Home weight | **476 requests / 24.1 MB initial; 624 / 25.8 MB total desktop. Mobile total is 29.0 MB.** |
| PDP weight | **23.7 MB** |
| Third-party script domains | **31 on home, 33 on PDP.** Includes Attentive, Klaviyo, Candid, Hotjar, Microsoft Clarity, UserWay, Convert, Venn Apps, DigitalGenius, Trustpilot, Datadog, The Trade Desk, Snapchat, TikTok and Meta. |
| LCP | Home 5.4 s desktop / 9.5 s mobile. PLP 4.9 s. PDP 1.4 s desktop / 3.2 s mobile. |
| JSON-LD | Organization, BreadcrumbList and WebSite/SearchAction; PDP adds Product and Offer |
| h1 | **0 on home** |
| Title | Ends in the internal store handle "– motelrocks-com-us" |

**Why it is so heavy:** a resource breakdown shows about 19.7 MB of images on home and 20.2 MB on PDP. Most of it is **full-size Instagram CDN images** (0.8 to 1.6 MB each from `cdninstagram.com`) loaded by the "Shop our Instagram" UGC widget (`getcandid.com`), plus a 3.8 MB 1080p hero video.

**Observed design**
- **Nav:** hamburger, NEW IN, SHOP, JEANS, TOPS, DRESSES, a centred "motel" serif wordmark, then search / account / wishlist / cart. A scrolling ticker reads "Free USA shipping over $95 / Up to 50% off dresses / Students get 10% off".
- **Home:**
  - A full-bleed video hero ("Meet me at midnight", "SHOP HALLOWEEN").
  - A "Motel Denim + You" image banner and 4 category tiles (New In, Knitwear, Tops, Out Out).
  - "Shop our Instagram" UGC and an email "Join our community" block.
- **Type:** DM Sans at 14 px with Instrument Serif Italic accents. Near-black `rgb(14,14,14)` on white.
- **PLP:**
  - A sub-category text row and horizontal dropdown filters (Product Type, Color, Size, Price) with a Relevance sort.
  - Mobile uses "Filter & Sort" and a 1- or 2-column toggle.
  - 4 columns on desktop, 2 on mobile.
  - Wishlist heart and badges on each card ("NEW IN", "RECYCLED MATERIALS"). Load-more.
- **PDP:**
  - A 2-column image grid.
  - Size buttons with the unavailable size greyed out.
  - Shop Pay and Afterpay instalment lines and a "Size Guide" link.
  - Black ADD TO BAG, **"NOTIFY ME WHEN IN STOCK"**, add to wishlist.
  - Accordions (Product info / Fabric & care / Shipping & returns) and "Complete the look".
  - ATC stays visible after scrolling on desktop and mobile.
- **Mobile overlays:** a mobile app download banner ("15% off your first order") and a bottom "Download our app" bar. A UserWay accessibility widget and a chat bubble are also present.
- **Social:** Instagram, TikTok, YouTube, X, Facebook, Pinterest and Snapchat links.

**What they do better**
- The most "Jaded-adjacent" merchandising: a party-wear category ("OUT OUT") and seasonal hooks (Halloween).
- Strong PDP conversion furniture: notify-me, BNPL, complete the look, wishlist.
- A student discount and an app.

**Jaded should copy**
- An "Out Out" or "Rave" occasion category as a top-level tile.
- PDP notify-me for unavailable sizes.
- Wishlist hearts on the PLP.
- Category text chips above the PLP.
- Shoppable UGC as a concept, but done right (see below).

**Jaded should not copy**
- **Raw Instagram images loaded at full size.** Proxy UGC through Shopify or an image CDN at around 400 px, and lazy-load it.
- 31+ third-party script domains.
- Stacked app and promo overlays on mobile.
- No h1 on the homepage.
- The store handle in titles.

---

## 10. Minga London (mingalondon.com, served as the US store, Shopify with Global-e)

The closest aesthetic competitor: the meta description reads "inspired by Y2K, underground music and internet culture".

**Shots:**
- Home: `mingalondon-home-desktop.jpg`, `-full.jpg`, `mingalondon-home-mobile.jpg`, `-full.jpg`
- PLP: `mingalondon-plp-desktop.jpg`, `-full.jpg`, `mingalondon-plp-mobile.jpg` (/collections/new-in)
- PDP: `mingalondon-pdp-desktop.jpg`, `mingalondon-pdp-mobile.jpg` (Rumor Buckle Cropped Fur Jacket)

**Measured**

| Measure | Value |
|---|---|
| Home weight (desktop) | 328 requests / 10.9 MB initial; 405 / 12.5 MB total |
| PLP weight | 16.9 to 18.1 MB, with 12.4 MB of images |
| PDP weight | 8.5 MB |
| Third-party script domains | **25.** Includes Klaviyo, Afterpay, LoyaltyLion, Rebuy, Global-e, Forter, Elevar, CookieYes, DoubleClick, Pinterest, TikTok, Snapchat and Meta. |
| LCP | Home 2.7 s desktop / 1.4 s mobile. PLP 9.8 s desktop. **The mobile PLP LCP of 20.3 s was the newsletter-popup image** (`soundestlink.com`). PDP 4.9 s / 5.5 s. |
| JSON-LD | **None on home.** PLP has CollectionPage. PDP has Product and Offer. No Organization or BreadcrumbList anywhere. |
| h1 | Home h1 is "Minga London - All weirdos r welcome!" |
| Images without `alt` | 7 of 65 on home, 10 of 109 on PDP |
| Meta descriptions | Good and keyword-led on every page |

**Observed design**
- **Header:** a "mingamembersclub JOIN NOW" bar on top, then a black "FREE & FAST SHIPPING OVER $200" bar, then a black header with hamburger, the chrome "minga" wordmark, NEW, WOMEN, MEN, SALE (in red) and MINGA CLUB, plus search / account / wishlist / cart icons.
- **Home:**
  - A full-bleed campaign photo hero ("BLING RING", "SHOP NOW").
  - A strip of product cut-outs, then category image tiles (Hoodies / Bottoms / Jackets / Accessories) and a second campaign image.
  - A black footer with the "THE GOOD STUFF, STRAIGHT TO U" email capture ("10% off + early access to new drops and restocks", segmented Women / Men / Both).
  - After scrolling, a centred **"STAY IN THE LOOP" 10%-off popup** appears (`mingalondon-home-desktop-full.jpg`).
- **Type:** Makro XM (medium and bold) plus Shapiro extended faces: 14 px body, 22 px h1, wide caps. Black and white with red for SALE.
- **PLP:**
  - Category pill chips (Denim, Bags, Hoodies/Sweatshirts, Tops/T-shirts, Jackets/Outerwear, Joggers).
  - A horizontal dropdown filter bar (Product Type, Size, Color, Price) with SORT.
  - 4 columns on desktop, 2 on mobile, 60 per page. Wishlist heart on cards.
- **PDP:**
  - A thumbnail column, a main image and the name and price in wide caps.
  - Size buttons, "SIZE GUIDE" and a colour swatch.
  - Black ADD TO BAG, then three USP tiles (30 days return policy / free shipping over $200 / express shipping).
  - A description accordion, Afterpay, reviews and "You may also like".
  - On mobile, a dot-paginated carousel. **No sticky ATC on either device.**
- **Drop mechanics:** a members club ("Minga Club"), early access to drops and restocks for subscribers, and the word "drop" in the copy.
- **Social:** Instagram, TikTok, YouTube and Pinterest links. The Snapchat and TikTok pixels load.

**What they do better**
- The tone of voice ("All weirdos r welcome!", "straight to u") and a membership club.
- Chrome-logo Y2K branding executed cleanly on a conventional, usable Shopify layout.
- Good meta descriptions.
- USP tiles under the ATC.

**Jaded should copy**
- A members club with early access to drops.
- Segmented email capture (Women / Men / Both).
- USP tiles under the ATC.
- Category pill chips on the PLP.
- A brand voice in the h1 and microcopy.

**Jaded should not copy**
- 17 to 18 MB PLPs.
- A popup that becomes the LCP element.
- No sticky ATC.
- Missing Organization and Breadcrumb schema.
- 25 third-party script domains.

---

## Cross-site summary

Home and PDP weights are initial desktop values (load plus 6 s). LCP is the desktop / mobile home page in ms. "3P" is the number of third-party script domains on the home page.

| Site | Platform | Home MB | Home req | 3P | Home LCP D/M | PDP MB | Hero | PLP cols D/M | Filter UX | PDP gallery | Sticky ATC (D/M) | Drop / waitlist mechanic | PDP Product LD | Missing alt (home) | h1 issues |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Balenciaga | n/a (not captured) | n/a | n/a | n/a | n/a | n/a | per sources: product grid | n/a | n/a | n/a | n/a | launches as media events (cited) | n/a | n/a | n/a |
| Corteiz | Shopify | 1.44 | 164 | 7 | 1796 / 1680 | n/a | password gate | n/a | n/a | n/a | n/a | **whole-store password + email capture** | n/a | 0/1 | empty h1 |
| Represent | Shopify | 7.63 | 462 | **41** | 3068 / 1496 | 9.7 | split 2-tile image | 4 / 2 (visual) | Filter & Sort drawer, model/packshot toggle | carousel 1/10 | no / yes | numbered drops, gated "Vault" sale sign-up, notification bell | yes (+ return and shipping policy) | 8/48 | h1 = title |
| Acne Studios | SFCC | 2.46 | 94 | 12 | 6032 / 2960 | 2.1 | full-bleed video | 4 / 2 | single FILTER drawer | vertical stack / swipe | yes / sticky (not in view after scroll) | "Out of stock? Get notified" | yes | **0/24** | ok |
| Vetements | Wix | 1.18 | 130 | 2 | 1688 / 1156 | n/a | text holding page | n/a (sells via SSENSE) | n/a | n/a | n/a | "coming very soon" | n/a | 0/4 | no h1 |
| Ottolinger | Shopify + Nuxt | 1.91 | 109 | **5** | 5664 / 4464 | 1.6 | **product grid + video bands** | 4 / 2 | single "Filters" toggle | single image + stack | sticky CSS but not in view after scroll / bottom bar on load | none observed | yes | **79/79** | **no h1** |
| SSENSE | custom | **13.6** (11.8 MB GIF) | 52 | 5 | 5308 / 1516 | 2.7 | type banner + editorial | 4 / 2 | left sidebar (categories, designers), Refine/Sort on mobile | 3-col, centre stack | yes / no | none observed | yes | 0/34 | 2 h1 on PDP |
| KidSuper | Shopify | 6.82 | 331 | 9 | 2208 / 3368 | 4.5 | art slideshow | **5** / 2 | horizontal facet bar + density toggle | carousel + thumbs | yes / bottom bar | low stock, sold-out badges, **event tickets** | yes | 4/240 | ok |
| Motel Rocks | Shopify | **24.1** | 476 | 31 | 5376 / 9472 | **23.7** | full-bleed video | 4 / 2 | horizontal dropdowns; mobile drawer and column toggle | 2-col grid | yes / yes | notify me when in stock | yes | 0/25 | **no h1 on home** |
| Minga London | Shopify + Global-e | 10.9 | 328 | 25 | 2696 / 1404 | 8.5 | full-bleed photo | 4 / 2 | pill chips + dropdown bar | thumbs + main / dots | no / no | members club, early access to drops | yes (no Org or Breadcrumb) | 7/65 | ok |

**Patterns across the set**
- **4 columns on desktop and 2 on mobile is universal.** Only KidSuper uses 5.
- **Size UX:** size buttons are the norm (Acne, KidSuper, Motel, Minga, Represent). Dropdowns appear only at SSENSE and Ottolinger, which are the two most "austere" sites.
- **Weight is driven by imagery and UGC, not by the platform.**
  - The two lightest storefront PDPs are Ottolinger (Shopify, 1.6 MB) and SSENSE (custom, 2.7 MB).
  - The heaviest are Motel (Shopify, 24 MB, from raw Instagram images) and Minga (Shopify, 17 to 18 MB PLP).
- **Third-party scripts scale with "growth stack" ambition.** Represent has 41, Motel 31 and Minga 25, against 5 to 12 for the fashion-house sites.
- **Nobody runs on-site countdown timers.** No countdown text was detected on any captured page. Drop mechanics are delivered through gates (Corteiz, Represent Vault), clubs and early access (Minga), notify-me (Acne, Motel) and social channels.
- **Social integration is mostly footer links plus tracking pixels.** Only Motel had an on-site shoppable Instagram feed (Candid). KidSuper embeds video. None embedded TikTok content on the pages captured.

---

## The "Balenciaga dial": what a Y2K rave brand should take from Demna-era balenciaga.com

The live site was not captured. The trait descriptions below combine cited sources ([It's Nice That](https://www.itsnicethat.com/news/bureau-borsche-balenciaga-website-redesign-010317), [HubSpot FR](https://blog.hubspot.fr/marketing/web-design-inspiration), [Hero](https://hero-magazine.com/article/180958/balenciagas-fw21-collection-comes-with-an-online-video-game-set-in-2031/), [FashionUnited](https://fashionunited.uk/news/fashion/did-balenciaga-erase-its-instagram-again/2021091257647)) with live analogues measured in this benchmark (Ottolinger, SSENSE, Acne).

| Trait | Turn it up for Jaded? | Why |
|---|---|---|
| **Product-grid-as-homepage** | **Yes (dial at 7/10)** | Ottolinger shows the live version: product is never more than one scroll away, and the page weighs only 1.9 MB. For a 2,058-SKU, TikTok-driven store, landing visitors on a shoppable grid fits the "saw it on TikTok, buy it now" flow better than Represent's two-tile, no-product homepage. Interleave TikTok/UGC video bands and rave campaign shots into the grid, as Ottolinger does with campaign bands. |
| **Full-bleed video** | **Yes, with a budget** | It suits a club brand (strobe, crowd, motion), and Acne and Motel both use it. Requirements: a separate mobile poster (Acne's `poster-m.jpg` pattern), MP4/WebM under about 2 to 4 MB, `muted playsinline`, and no GIFs. SSENSE's 11.8 MB GIF and Acne's 6 s desktop LCP show the cost of skipping this. |
| **Drops as art releases** | **Yes (dial at 8/10)** | This is the most transferable trait. Copy the media-event idea (Afterworld, feed wipes) with Jaded-scale tools: a password-gated capsule page in Shopify's password template (Corteiz), a gated sale "Vault" with sign-up when closed (Represent), numbered drops, members' early access (Minga), and **club-night tickets sold on-site** (KidSuper). |
| **Black / white palette** | **Partial (4/10)** | Use black and white as the *UI chrome* so product colour and Y2K graphics pop. Minga does exactly this: a black header and white grid, with personality from the chrome logo and red SALE. Don't make the *brand* monochrome. Jaded's identity is colour, holographic and neon, so keep those as accent tokens (badges, drop banners, hover states). |
| **Brutalist UI** | **Light touch (3/10)** | Raw grids, hard edges and visible structure read as "underground" and suit rave flyers. Avoid the usability costs seen live: 0 h1s and 0 `alt` attributes at Ottolinger, and thin filters at SSENSE ([Pratt critique](https://ixd.prattsi.org/2023/09/design-critique-ssense/)). Brutalism should live in the art direction, not in removing affordances. |
| **Tiny utilitarian type** | **No (1/10)** | Ottolinger uses 11 px, SSENSE 11 px and Acne 12 px with a 12 px h1. That signals quiet luxury and makes product names hard to scan on a phone, which is where TikTok traffic lands. Jaded should use a loud display face for headings and drop names, with a body size of at least 14 to 16 px. Minga's 14 px with extended caps is the right register. |
| **Logo-minimal, near-anonymous branding** | **No** | It works for a heritage house that everyone knows. For Jaded it would erase the personality that TikTok viewers recognise. Keep a strong logo, voice-led copy (as with Minga's "All weirdos r welcome!") and scene signals such as event tickets and DJ content. |

**Bottom line**
- **Take:** the grid-first homepage, video (done efficiently) and drops as events. These raise conversion and hype, and the live data shows they can be cheap.
- **Leave:** tiny type, monochrome branding, anonymity and austere accessibility. These would make Jaded look like a luxury stockist and drain the Y2K/rave personality that is its edge.
