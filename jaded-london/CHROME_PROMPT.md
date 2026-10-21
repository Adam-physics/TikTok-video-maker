# Prompt for Claude in Chrome

**Before you run it:** open https://jadedldn.com/en-us in Chrome yourself, pass the
Cloudflare check, and set the country selector to **United States (USD)**. Then open
the Claude side panel and paste everything in the block below. If it stops partway
(context or length limits), say *"continue from where you stopped"*.

```
You are helping me document the website jadedldn.com (Jaded London, US store at
/en-us) for a redesign audit. I've already passed the site's security check in
this browser. Browse it like a normal shopper. Don't submit any forms, add to
cart, check out, sign up or log in. Work page by page and be thorough.

PART A: Raw catalog data (most important)
Open each of these URLs in a tab and SAVE THE FULL PAGE TEXT as a file
(Ctrl/Cmd+S, or copy all the text and give it to me as a downloadable file).
Keep the filenames shown:
  1. https://jadedldn.com/products.json?limit=250&page=1   -> products_p1.json
     Keep going with page=2, page=3 ... until the response is {"products":[]}
     -> products_p2.json, products_p3.json, ...
  2. https://jadedldn.com/collections.json?limit=250        -> collections.json
     (and page=2 if it returns 250 items)
  3. https://jadedldn.com/sitemap.xml                       -> sitemap.xml
     and open each child sitemap listed in it (products, collections, pages,
     blogs) -> sitemap_products.xml, sitemap_pages.xml, etc.
  4. https://jadedldn.com/robots.txt                         -> robots.txt
  5. https://jadedldn.com/en-us/products/<any-handle>.js for one product
                                                             -> product_sample.js.json
If any URL errors or is blocked, write that down and move on.

PART B: Page-by-page content inventory
Create ONE markdown file called jaded_inventory.md. For each page below, record:
- URL and page <title> / meta description (if visible)
- Announcement bar text (exact), header nav (every top-level item and every
  item in each mega-menu/dropdown, in order), utility icons (search, account,
  wishlist, bag, country/currency)
- Every section top to bottom: section type (hero, carousel, grid, video,
  text, UGC, etc.), exact headline/body/CTA copy, what the image/video shows,
  and the image/video URL (right-click > Copy image address; cdn.shopify.com
  links)
- Footer: every column and link, newsletter copy, social links, payment
  icons, legal text
- Any popups (newsletter, cookie, region), with exact copy and timing
- Notable UX: sticky header? filters? sort options? quick-add? swatches?
  size guide? reviews widget (which app)? Klarna/Afterpay? chat widget?
  "Shop the look"? recommended products? recently viewed?

Pages:
  1. Homepage /en-us (desktop, then repeat key notes for mobile width)
  2. Womens: New In, All Womens, plus 2 sub-categories (e.g. cargo pants,
     jeans)
  3. Mens: New In, All Mens, plus 2 sub-categories
  4. Swimwear (if present), Sale (if present), any "Essentials"/"Basics"
  5. Product pages: 1 Parachute Cargo Pant (womens), 1 mens jean, 1 dress or
     top, 1 swim item. Record title, price, compare-at price, colours, sizes,
     fit notes, full description, composition/care, delivery/returns copy,
     every image URL, badges, reviews, upsells
  6. /pages/the-parachute-pant-jaded-london, /pages/the-parachute-pants-womens,
     /pages/the-parachute-pants-mens
  7. Campaign/collab pages: /pages/rock-revival-collaboration,
     /pages/sleazenation, /pages/ldn-to-nyc, plus any other collab, campaign,
     lookbook or editorial page linked from nav or footer
  8. Stores: /pages/new-york-store-2026 and any London store page
  9. About / Our Story, Contact, FAQ, Shipping, Returns, Size Guide,
     Student discount, Affiliates/Ambassadors, Careers, Sustainability (if any)
 10. Search: search for "parachute" and record the results and UI behaviour
 11. Cart drawer: open it EMPTY only and record the copy and upsells

PART C: Screenshots
Take screenshots (full page where possible) and give them to me with these names:
  home_desktop.png, home_mobile.png (resize to ~390px wide or use the
  device toolbar), plp_womens.png, plp_mens.png, pdp_parachute.png,
  pdp_mobile.png, parachute_landing.png, collab_rock_revival.png,
  stores_nyc.png, menu_open_desktop.png, menu_open_mobile.png, footer.png

PART D: Quick technical notes (add to the end of jaded_inventory.md)
- Theme name if visible (view source, search for "theme" or
  Shopify.theme), apps you can identify from scripts (Klaviyo, Yotpo, Okendo,
  Rebuy, Nosto, Searchanise, Gorgias, Afterpay, Klarna, etc.)
- Rough load feel: how long until the hero shows, layout jumps, heavy
  autoplay video
- Accessibility: images without alt text, low-contrast text, keyboard focus
  visible?
- Anything broken, inconsistent or off-brand

PART E: Social presence (if you can view without logging in)
Visit Jaded London's Instagram and TikTok. Record handles, follower counts,
bio text, link-in-bio destination, and describe the 12 most recent posts:
format, vibe, colour, typography, recurring themes and creators/models.
This defines the brand's "is / is not".

When done, list every file you produced so I can download them all.
```

## After it finishes
Upload every file it produced into this repo at `jaded-london/scrape/` (or drag
them into the new Claude Code session), then follow step 4 of `HANDOFF.md`.
