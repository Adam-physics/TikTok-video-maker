# Jaded London: content inventory

Source: public Shopify JSON endpoints on `jaded-london.myshopify.com` (`/products.json`, `/collections.json`, `/pages.json`, `/meta.json`), fetched 21 Oct 2026. The storefront `jadedldn.com` returns a Cloudflare challenge to automated browsers, so theme HTML, navigation menus, scripts and screenshots of the live site are **not** in this inventory; see "Gaps" at the end.

## Store

| Field | Value |
|---|---|
| Name | Jaded London (London, GB) |
| Base currency | GBP, money format `£{{amount_no_decimals}}` |
| Ships to | 190 countries |
| Shop Pay installments | off |
| Meta description | "Discover global inspired street style and cutting edge trends. Designed in London, delivered worldwide. Free UK Delivery over £80. Free international delivery varies." |
| Published products | 2058 |
| Published collections | 532 |
| Content pages | 390 |

## Products

| Brand line (vendor) | Products |
|---|---|
| Jaded London | 1180 |
| Jaded Man | 628 |
| Jaded Swim | 250 |

- Variants: **12,939**; images: **17,820** (median 8 per product, median width 2048 px, 99.6% JPEG)
- Price (lowest variant): £6 to £300, median £48
- On markdown (compare-at above price): **909** (44%); in stock in at least one size: 1655
- Titles used by more than one product: **355** (mostly the same unisex style listed once under Jaded London and once under Jaded Man)
- Published year: 2023: 79, 2024: 238, 2025: 632, 2026: 1109
- Unique tags: 1265 (mix of merchandising, sale-event, region and internal ops tags)

| Product type | Count | Price range | Median |
|---|---|---|---|
| Tops | 342 | £11–£140 | £39 |
| Baggy Jeans | 184 | £33–£150 | £85 |
| Joggers | 155 | £20–£120 | £65 |
| Jackets | 151 | £33–£300 | £85 |
| Shorts | 146 | £13–£100 | £45 |
| Mini Dresses | 133 | £15–£300 | £60 |
| Bikini Bottoms | 119 | £7–£65 | £20 |
| Bikini Tops | 115 | £8–£65 | £25 |
| Pants | 107 | £14–£90 | £65 |
| Hoodies | 74 | £33–£120 | £70 |
| Skirts | 73 | £8–£95 | £36 |
| Maxi Dresses | 67 | £14–£200 | £60 |
| Jorts | 51 | £20–£110 | £55 |
| Bootcut Jeans | 43 | £28–£120 | £70 |
| Belts | 34 | £12–£70 | £38 |
| Flared Jeans | 26 | £38–£130 | £85 |
| Bags | 26 | £8–£137 | £65 |
| Footwear | 24 | £39–£205 | £160 |
| Shirts | 18 | £25–£60 | £32 |
| Hats | 17 | £14–£50 | £38 |
| Straight Jeans | 17 | £33–£150 | £85 |
| Basic Tops | 16 | £20–£50 | £40 |
| Cropped T-Shirt | 15 | £40–£58 | £45 |
| Knitwear | 15 | £20–£85 | £38 |
| Sunglasses | 14 | £70–£120 | £120 |
| Skinny Jeans | 9 | £45–£95 | £85 |
| Trousers | 8 | £35–£59 | £42 |
| Vests | 7 | £19–£50 | £28 |
| Capes | 7 | £20–£50 | £20 |
| Cargo Shorts | 6 | £42–£65 | £50 |
| Scarves | 5 | £18–£125 | £63 |
| Scarf | 5 | £25–£45 | £28 |
| Runner Shorts | 4 | £45–£45 | £45 |
| T-Shirts | 3 | £45–£45 | £45 |
| Gloves | 3 | £15–£35 | £35 |
| Necklace | 3 | £30–£38 | £38 |
| Accessories | 2 | £15–£38 | £26 |
| Bag | 2 | £25–£25 | £25 |
| Swimsuits | 2 | £80–£80 | £80 |
| Gift Card | 2 | £10–£10 | £10 |
| Low Rise | 1 | £95–£95 | £95 |
| Stickers | 1 | £6–£6 | £6 |
| T-shirts | 1 | £23–£23 | £23 |
| Keyring | 1 | £13–£13 | £13 |
| Dresses | 1 | £45–£45 | £45 |
| Bracelet | 1 | £9–£9 | £9 |
|  | 1 | £60–£60 | £60 |
| Jeans | 1 | £38–£38 | £38 |

**Parachute franchise:** 47 products with "Parachute" in the title, £35–£75; core Parachute Cargo Pants £65.

## Collections

| Kind (classified) | Count |
|---|---|
| merchandising | 397 |
| internal ops (dated drop/reshoot) | 54 |
| sale | 34 |
| app-only | 30 |
| seasonal promo | 7 |
| empty | 6 |
| creator edit | 4 |

- No collection has an image in the JSON; 299 of 532 have no description.
- Internal operations leak into public URLs: dated drop/reshoot collections such as `/collections/11-2-26-mw-ecom-drop-and-reshoots`, `/collections/27-10-25-reshoots`.

## Pages

| Kind (classified) | Count |
|---|---|
| campaign / editorial | 108 |
| drop waitlist | 51 |
| stores / IRL | 35 |
| collab | 34 |
| careers | 26 |
| help centre | 21 |
| landing duplicate of collection | 21 |
| student discount | 21 |
| empty body | 20 |
| junk | 17 |
| misc | 14 |
| size guide | 5 |
| account | 5 |
| policy | 4 |
| search | 4 |
| hero franchise | 4 |

- 156 pages load Shogun page-builder assets (`a.shgcdn2.com`, `cdn.getshogun.com`).
- Third-party hosts embedded in page bodies: Shogun, YouTube, Vimeo, parcelLab, Parcel Perform, Student Beans, Searchanise, Pogo Donate. Pages also reference Klaviyo (30), Gorgias, Dash Hudson, Later, TikTok, Instagram. Handles reveal Swym (wishlist), usizy (size advice), Klarna, Student Beans (19 country pages), a native app.
- The accessibility statement names **EqualWeb** (an overlay) as its accessibility partner.
- Index-page hygiene: `/pages/campaigns` links to a `-copy` page, to a broken `sleazenation-for-jaded%20` URL and to a raw Dropbox MP4; `/pages/stores` links to `lucia-campaign`.

## Stores and IRL (from /pages/stores)

- NYC Store, September 2025 (434 Broadway per press)
- ENG Pop-up, Hangzhou, December 2025
- ENG Pop-up, Chengdu, December 2025
- Nubian Pop-up, Tokyo, November 2025
- World Tour: Miami Pop-up, May 2025
- World Tour: LA Pop-up, April 2025
- Jaded London / Selfridges London, November 2024
- London Pop-up, December 2024
- NYC Pop-up, September 2024
- Japan Pop-up, October 2024
- Jaded London x 2000Archives, Seoul, April 2024
- Shanghai Pop-up, March 2024
- LA Pop-up, April 2024 and April 2023
- London Pop-up, September 2023

## Full page list

| Old URL | Class | Proposed URL | Action |
|---|---|---|---|
| `/pages/10-off-your-first-order` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/2kjaded` | collab | `/pages/collabs/2kjaded` | 301 |
| `/pages/411` | campaign / editorial | `/pages/campaigns/411` | 301 |
| `/pages/411-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/411-sign-up` | drop waitlist | `/pages/drops/411` | 301 |
| `/pages/411takesparis` | stores / IRL | `/pages/stores/411takesparis` | 301 |
| `/pages/5am` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/5am-campaign` | campaign / editorial | `/pages/campaigns/5am` | 301 |
| `/pages/accessibility-statement` | campaign / editorial | `/pages/campaigns/accessibility-statement` | 301 |
| `/pages/accordion-test` | junk | `(delete)` | delete+301 to parent |
| `/pages/alloy-campaign` | campaign / editorial | `/pages/campaigns/alloy` | 301 |
| `/pages/amara-sign-up` | drop waitlist | `/pages/drops/amara` | 301 |
| `/pages/aphotic` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/armour-campaign` | campaign / editorial | `/pages/campaigns/armour` | 301 |
| `/pages/away-fans` | campaign / editorial | `/pages/campaigns/away-fans` | 301 |
| `/pages/b2r` | campaign / editorial | `/pages/campaigns/b2r` | 301 |
| `/pages/babymorocco-for-jadedlondon` | collab | `/pages/collabs/babymorocco-for-jadedlondon` | 301 |
| `/pages/bf-test` | junk | `(delete)` | delete+301 to parent |
| `/pages/block-exe-app-sign-up-page` | drop waitlist | `/pages/drops/block-exe` | 301 |
| `/pages/block-exe-sign-up-page` | drop waitlist | `/pages/drops/block-exe` | 301 |
| `/pages/blueprint` | campaign / editorial | `/pages/campaigns/blueprint` | 301 |
| `/pages/blueprint-drop-2-sign-up` | drop waitlist | `/pages/drops/blueprint-drop-2` | 301 |
| `/pages/blueprint-sign-up` | drop waitlist | `/pages/drops/blueprint` | 301 |
| `/pages/brand-partnerships-manager` | careers | `/pages/careers#brand-partnerships-manager` | 301 |
| `/pages/brazil` | campaign / editorial | `/pages/campaigns/brazil` | 301 |
| `/pages/bronco` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/campaign` | campaign / editorial | `/pages/campaigns/` | 301 |
| `/pages/campaign-6am` | campaign / editorial | `/pages/campaigns/6am` | 301 |
| `/pages/campaign-allegra` | campaign / editorial | `/pages/campaigns/allegra` | 301 |
| `/pages/campaign-amara` | campaign / editorial | `/pages/campaigns/amara` | 301 |
| `/pages/campaign-amethyst` | campaign / editorial | `/pages/campaigns/amethyst` | 301 |
| `/pages/campaign-ballerina` | campaign / editorial | `/pages/campaigns/ballerina` | 301 |
| `/pages/campaign-ember` | campaign / editorial | `/pages/campaigns/ember` | 301 |
| `/pages/campaign-fade` | campaign / editorial | `/pages/campaigns/fade` | 301 |
| `/pages/campaign-fade-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/campaign-faithless` | campaign / editorial | `/pages/campaigns/faithless` | 301 |
| `/pages/campaign-haze` | campaign / editorial | `/pages/campaigns/haze` | 301 |
| `/pages/campaign-joint-la` | campaign / editorial | `/pages/campaigns/joint-la` | 301 |
| `/pages/campaign-karmen` | campaign / editorial | `/pages/campaigns/karmen` | 301 |
| `/pages/campaign-larry-clark` | campaign / editorial | `/pages/campaigns/larry-clark` | 301 |
| `/pages/campaign-loveaffair` | campaign / editorial | `/pages/campaigns/loveaffair` | 301 |
| `/pages/campaign-newrock-aw25` | campaign / editorial | `/pages/campaigns/newrock-aw25` | 301 |
| `/pages/campaign-reverb` | campaign / editorial | `/pages/campaigns/reverb` | 301 |
| `/pages/campaign-romie` | campaign / editorial | `/pages/campaigns/romie` | 301 |
| `/pages/campaigns` | campaign / editorial | `/pages/campaigns` | 301 |
| `/pages/canvas` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/capex` | campaign / editorial | `/pages/campaigns/capex` | 301 |
| `/pages/capex-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/careers-jadedlondon` | careers | `/pages/careers` | 301 |
| `/pages/careers-jadedlondon-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/careers-jadedlondon-copy-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/casa-loma-campaign` | campaign / editorial | `/pages/campaigns/casa-loma` | 301 |
| `/pages/castellomen` | misc | `/pages/castellomen` | keep |
| `/pages/castellomens` | misc | `/pages/castellomens` | keep |
| `/pages/casting-call-jaded` | misc | `/pages/casting-call-jaded` | keep |
| `/pages/centrepiece` | campaign / editorial | `/pages/campaigns/centrepiece` | 301 |
| `/pages/centrepiece-sign-up` | drop waitlist | `/pages/drops/centrepiece` | 301 |
| `/pages/chengdu-pop-up` | stores / IRL | `/pages/stores/chengdu-pop-up` | 301 |
| `/pages/chief-growth-officer` | careers | `/pages/careers#chief-growth-officer` | 301 |
| `/pages/ciao-campaign` | campaign / editorial | `/pages/campaigns/ciao` | 301 |
| `/pages/cold-f33t-sign-up` | drop waitlist | `/pages/drops/cold-f33t` | 301 |
| `/pages/cold-feet-for-jaded` | collab | `/pages/collabs/cold-feet-for-jaded` | 301 |
| `/pages/colossus-sign-up` | drop waitlist | `/pages/drops/colossus` | 301 |
| `/pages/community-rewards` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/contact-us` | help centre | `/pages/help/contact-us` | 301 |
| `/pages/cookies-policy` | policy | `/policies/privacy-policy#cookies` | 301 |
| `/pages/core` | campaign / editorial | `/pages/campaigns/core` | 301 |
| `/pages/core-sign-up` | drop waitlist | `/pages/drops/core` | 301 |
| `/pages/core-sign-up-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/corporate-social-responsibility` | campaign / editorial | `/pages/campaigns/corporate-social-responsibility` | 301 |
| `/pages/cowboys-of-habit-for-jaded` | collab | `/pages/collabs/cowboys-of-habit-for-jaded` | 301 |
| `/pages/cowboys-of-habit-for-jaded-sign-up` | drop waitlist | `/pages/drops/cowboys-of-habit-for-jaded` | 301 |
| `/pages/cowboysofhabit` | collab | `/pages/collabs/cowboysofhabit` | 301 |
| `/pages/crash` | campaign / editorial | `/pages/campaigns/crash` | 301 |
| `/pages/creative-content-coordinator` | careers | `/pages/careers#creative-content-coordinator` | 301 |
| `/pages/crm-manager` | careers | `/pages/careers#crm-manager` | 301 |
| `/pages/crush` | campaign / editorial | `/pages/campaigns/crush` | 301 |
| `/pages/crush-sign-up` | drop waitlist | `/pages/drops/crush` | 301 |
| `/pages/curated-by-creators` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/curly-fry-x-jaded-man` | collab | `/pages/collabs/curly-fry-x-jaded-man` | 301 |
| `/pages/custom-football-shirt` | misc | `/pages/custom-football-shirt` | keep |
| `/pages/customer-care-advisor` | careers | `/pages/careers#customer-care-advisor` | 301 |
| `/pages/customer-care-advisor-weekends` | careers | `/pages/careers#customer-care-advisor-weekends` | 301 |
| `/pages/customer-care-manager-jaded-london` | careers | `/pages/careers#customer-care-manager-jaded-london` | 301 |
| `/pages/dahna` | campaign / editorial | `/pages/campaigns/dahna` | 301 |
| `/pages/decade-sign-up` | drop waitlist | `/pages/drops/decade` | 301 |
| `/pages/delivery-draft` | junk | `(delete)` | delete+301 to parent |
| `/pages/delivery-info` | help centre | `/pages/help/delivery-info` | 301 |
| `/pages/devon` | campaign / editorial | `/pages/campaigns/devon` | 301 |
| `/pages/devon-app-sign-up` | drop waitlist | `/pages/drops/devon` | 301 |
| `/pages/devon-sign-up-page` | drop waitlist | `/pages/drops/devon` | 301 |
| `/pages/dirtyl00ks-campaign` | collab | `/pages/collabs/dirtyl00ks-campaign` | 301 |
| `/pages/dirtyl00ks-for-jaded` | collab | `/pages/collabs/dirtyl00ks-for-jaded` | 301 |
| `/pages/download-the-jaded-london-app` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/drift` | campaign / editorial | `/pages/campaigns/drift` | 301 |
| `/pages/dusk-affair` | campaign / editorial | `/pages/campaigns/dusk-affair` | 301 |
| `/pages/dusk-campaign` | campaign / editorial | `/pages/campaigns/dusk` | 301 |
| `/pages/dusk-sign-up` | drop waitlist | `/pages/drops/dusk` | 301 |
| `/pages/eclipse-campaign` | campaign / editorial | `/pages/campaigns/eclipse` | 301 |
| `/pages/eden` | misc | `/pages/eden` | keep |
| `/pages/editions` | collab | `/pages/collabs/editions` | 301 |
| `/pages/elysium` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/ensemble` | campaign / editorial | `/pages/campaigns/ensemble` | 301 |
| `/pages/eternal` | campaign / editorial | `/pages/campaigns/eternal` | 301 |
| `/pages/europa` | careers | `/pages/careers#europa` | 301 |
| `/pages/europa-collection-preview` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/europa-sign-up-page` | drop waitlist | `/pages/drops/europa` | 301 |
| `/pages/exchanges` | help centre | `/pages/help/exchanges` | 301 |
| `/pages/eyewear-ss25-campaign` | campaign / editorial | `/pages/campaigns/eyewear-ss25` | 301 |
| `/pages/fantasy-store-campaign` | stores / IRL | `/pages/stores/fantasy-store-campaign` | 301 |
| `/pages/faqs-delivery` | help centre | `/pages/help/delivery` | 301 |
| `/pages/faqs-orders` | help centre | `/pages/help/orders` | 301 |
| `/pages/faqs-payments` | help centre | `/pages/help/payments` | 301 |
| `/pages/faqs-product` | help centre | `/pages/help/product` | 301 |
| `/pages/faqs-returns` | help centre | `/pages/help/returns` | 301 |
| `/pages/faqs-technical` | help centre | `/pages/help/technical` | 301 |
| `/pages/fatale` | campaign / editorial | `/pages/campaigns/fatale` | 301 |
| `/pages/fatale-sign-up` | drop waitlist | `/pages/drops/fatale` | 301 |
| `/pages/fatale2` | misc | `/pages/fatale2` | keep |
| `/pages/fatalecampaign` | campaign / editorial | `/pages/campaigns/fatale` | 301 |
| `/pages/files-old` | junk | `(delete)` | delete+301 to parent |
| `/pages/finale` | campaign / editorial | `/pages/campaigns/finale` | 301 |
| `/pages/footwear-launch` | campaign / editorial | `/pages/campaigns/footwear-launch` | 301 |
| `/pages/fracture-jaded-takes-paris` | stores / IRL | `/pages/stores/fracture-jaded-takes-paris` | 301 |
| `/pages/fracture-sign-up` | drop waitlist | `/pages/drops/fracture` | 301 |
| `/pages/got-game-campaign` | campaign / editorial | `/pages/campaigns/got-game` | 301 |
| `/pages/graphic-designer` | careers | `/pages/careers#graphic-designer` | 301 |
| `/pages/hang-on-in-there-campaign` | campaign / editorial | `/pages/campaigns/hang-on-in-there` | 301 |
| `/pages/hangzhou-stores` | stores / IRL | `/pages/stores/hangzhou-stores` | 301 |
| `/pages/head-of-marketing` | campaign / editorial | `/pages/campaigns/head-of-marketing` | 301 |
| `/pages/hotline` | help centre | `/pages/help/hotline` | 301 |
| `/pages/hotline-sign-up` | drop waitlist | `/pages/drops/hotline` | 301 |
| `/pages/ibiza` | campaign / editorial | `/pages/campaigns/ibiza` | 301 |
| `/pages/ibiza-2026-jaded-london` | campaign / editorial | `/pages/campaigns/ibiza-2026-jaded-london` | 301 |
| `/pages/idol` | misc | `/pages/idol` | keep |
| `/pages/idol-campaign` | campaign / editorial | `/pages/campaigns/idol` | 301 |
| `/pages/influencer-outreach-pr-assistant` | careers | `/pages/careers#influencer-outreach-pr-assistant` | 301 |
| `/pages/instagram-shop` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/international` | help centre | `/pages/help/international` | 301 |
| `/pages/internetgf` | campaign / editorial | `/pages/campaigns/internetgf` | 301 |
| `/pages/jaded-ldn-paper` | campaign / editorial | `/pages/campaigns/jaded-ldn-paper` | 301 |
| `/pages/jaded-ldn-x-sydney-carlson` | collab | `/pages/collabs/jaded-ldn-x-sydney-carlson` | 301 |
| `/pages/jaded-london-2000-archives` | collab | `/pages/collabs/jaded-london-2000-archives` | 301 |
| `/pages/jaded-london-2000archives-store` | stores / IRL | `/pages/stores/jaded-london-2000archives-store` | 301 |
| `/pages/jaded-london-denim` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/jaded-london-denim-unisex` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/jaded-london-eng-store` | stores / IRL | `/pages/stores/jaded-london-eng-store` | 301 |
| `/pages/jaded-london-gentle-monster` | collab | `/pages/collabs/jaded-london-gentle-monster` | 301 |
| `/pages/jaded-london-neutrals` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/jaded-london-pop-up-party-terms-conditions` | stores / IRL | `/pages/stores/jaded-london-pop-up-party-terms-conditions` | 301 |
| `/pages/jaded-london-selfridges-london` | stores / IRL | `/pages/stores/jaded-london-selfridges-london` | 301 |
| `/pages/jaded-london-size-guide` | size guide | `/pages/help/size-and-fit` | 301 |
| `/pages/jaded-london-x-2000-archives` | collab | `/pages/collabs/jaded-london-x-2000-archives` | 301 |
| `/pages/jaded-man-neutrals` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/jaded-new-rock-sign-up` | drop waitlist | `/pages/drops/jaded-new-rock` | 301 |
| `/pages/jaded-x-nothing-nyc` | collab | `/pages/collabs/jaded-x-nothing-nyc` | 301 |
| `/pages/jaded-x-vfiles-nyc-pop-up` | stores / IRL | `/pages/stores/jaded-x-vfiles-nyc-pop-up` | 301 |
| `/pages/jaded-x-vfiles-nyc-pop-up-copy-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/jadedboots` | campaign / editorial | `/pages/campaigns/jadedboots` | 301 |
| `/pages/jadedxomightycampaign` | collab | `/pages/collabs/jadedxomightycampaign` | 301 |
| `/pages/jadedxomightylaunchparty` | collab | `/pages/collabs/jadedxomightylaunchparty` | 301 |
| `/pages/jude-jeans` | campaign / editorial | `/pages/campaigns/jude-jeans` | 301 |
| `/pages/junior-womenswear-designer` | careers | `/pages/careers#junior-womenswear-designer` | 301 |
| `/pages/kaia-campaign` | campaign / editorial | `/pages/campaigns/kaia` | 301 |
| `/pages/katyazelentsova` | misc | `/pages/katyazelentsova` | keep |
| `/pages/klarna` | help centre | `/pages/help/klarna` | 301 |
| `/pages/la-casting-call` | campaign / editorial | `/pages/campaigns/la-casting-call` | 301 |
| `/pages/la-maskarade` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/la-maskarade-sign-up` | drop waitlist | `/pages/drops/la-maskarade` | 301 |
| `/pages/la-pop-up` | stores / IRL | `/pages/stores/la-pop-up` | 301 |
| `/pages/la-pop-up-sign-up` | drop waitlist | `/pages/drops/la-pop-up` | 301 |
| `/pages/la-popup-2025-store` | stores / IRL | `/pages/stores/la-popup-2025-store` | 301 |
| `/pages/la-store-2026` | stores / IRL | `/pages/stores/la-store-2026` | 301 |
| `/pages/la23party` | campaign / editorial | `/pages/campaigns/la23party` | 301 |
| `/pages/lamaskaradextides` | campaign / editorial | `/pages/campaigns/lamaskaradextides` | 301 |
| `/pages/lanzarote` | campaign / editorial | `/pages/campaigns/lanzarote` | 301 |
| `/pages/lapopup23` | stores / IRL | `/pages/stores/lapopup23` | 301 |
| `/pages/lapopup24` | stores / IRL | `/pages/stores/lapopup24` | 301 |
| `/pages/larry-clark-campaign` | campaign / editorial | `/pages/campaigns/larry-clark` | 301 |
| `/pages/larry-clark-editions` | collab | `/pages/collabs/larry-clark-editions` | 301 |
| `/pages/launches-womens` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/ldn-to-nyc` | campaign / editorial | `/pages/campaigns/ldn-to-nyc` | 301 |
| `/pages/ldnpopup23` | stores / IRL | `/pages/stores/ldnpopup23` | 301 |
| `/pages/livia` | campaign / editorial | `/pages/campaigns/livia` | 301 |
| `/pages/livia-collection-sign-up-page` | drop waitlist | `/pages/drops/livia` | 301 |
| `/pages/local-celebrities` | campaign / editorial | `/pages/campaigns/local-celebrities` | 301 |
| `/pages/lola` | campaign / editorial | `/pages/campaigns/lola` | 301 |
| `/pages/lola-app-sign-up` | drop waitlist | `/pages/drops/lola` | 301 |
| `/pages/lola-collection-sign-up-page` | drop waitlist | `/pages/drops/lola` | 301 |
| `/pages/london-pop-up` | stores / IRL | `/pages/stores/london-pop-up` | 301 |
| `/pages/london-pop-up-2024` | stores / IRL | `/pages/stores/london-pop-up-2024` | 301 |
| `/pages/london-pop-up-24` | stores / IRL | `/pages/stores/london-pop-up-24` | 301 |
| `/pages/london-pop-up-guests` | stores / IRL | `/pages/stores/london-pop-up-guests` | 301 |
| `/pages/london-pop-up-test2` | junk | `(delete)` | delete+301 to parent |
| `/pages/lucia-campaign` | campaign / editorial | `/pages/campaigns/lucia` | 301 |
| `/pages/matrix` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/mens` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/mens-1` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/mens-denim-app` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/mens-denim-fit-guide` | size guide | `/pages/help/size-and-fit` | 301 |
| `/pages/mens-tokyo` | stores / IRL | `/pages/stores/mens-tokyo` | 301 |
| `/pages/miami-popup-2025-store` | stores / IRL | `/pages/stores/miami-popup-2025-store` | 301 |
| `/pages/mvp-campaign` | campaign / editorial | `/pages/campaigns/mvp` | 301 |
| `/pages/new-rock-2-campaign` | collab | `/pages/collabs/new-rock-2-campaign` | 301 |
| `/pages/new-rock-editions` | collab | `/pages/collabs/new-rock-editions` | 301 |
| `/pages/new-rock-for-jaded` | collab | `/pages/collabs/new-rock-for-jaded` | 301 |
| `/pages/new-rock-sign-up` | drop waitlist | `/pages/drops/new-rock` | 301 |
| `/pages/new-york-2025-store` | stores / IRL | `/pages/stores/new-york-2025-store` | 301 |
| `/pages/new-york-pop-up-2024` | stores / IRL | `/pages/stores/new-york-pop-up-2024` | 301 |
| `/pages/new-york-store-2026` | stores / IRL | `/pages/stores/new-york-store-2026` | 301 |
| `/pages/nolita-jaded-london` | campaign / editorial | `/pages/campaigns/nolita-jaded-london` | 301 |
| `/pages/nolita-save-the-date` | stores / IRL | `/pages/stores/nolita-save-the-date` | 301 |
| `/pages/nolita-sign-up-app` | drop waitlist | `/pages/drops/nolita-sign-up-app` | 301 |
| `/pages/ntrls-mens` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/ntrls-sign-up` | drop waitlist | `/pages/drops/ntrls` | 301 |
| `/pages/nubian-pop-up` | stores / IRL | `/pages/stores/nubian-pop-up` | 301 |
| `/pages/nyc-party-2024` | campaign / editorial | `/pages/campaigns/nyc-party-2024` | 301 |
| `/pages/nyc-party-2025` | campaign / editorial | `/pages/campaigns/nyc-party-2025` | 301 |
| `/pages/nyc-popup-2024-store` | stores / IRL | `/pages/stores/nyc-popup-2024-store` | 301 |
| `/pages/office-manager-pa` | careers | `/pages/careers#office-manager-pa` | 301 |
| `/pages/offside` | campaign / editorial | `/pages/campaigns/offside` | 301 |
| `/pages/offside-sign-up` | drop waitlist | `/pages/drops/offside` | 301 |
| `/pages/offsidebrazil` | campaign / editorial | `/pages/campaigns/offsidebrazil` | 301 |
| `/pages/omighty-x-jaded` | collab | `/pages/collabs/omighty-x-jaded` | 301 |
| `/pages/ophidian-campaign` | campaign / editorial | `/pages/campaigns/ophidian` | 301 |
| `/pages/order-tracking` | help centre | `/pages/help/order-tracking` | 301 |
| `/pages/outerwear-campaign` | campaign / editorial | `/pages/campaigns/outerwear` | 301 |
| `/pages/outlaw` | misc | `/pages/outlaw` | keep |
| `/pages/outlaw-first-access` | drop waitlist | `/pages/drops/outlaw` | 301 |
| `/pages/pagayo-sign-up` | drop waitlist | `/pages/drops/pagayo` | 301 |
| `/pages/paid-social-executive` | careers | `/pages/careers#paid-social-executive` | 301 |
| `/pages/paris` | stores / IRL | `/pages/stores/paris` | 301 |
| `/pages/party-guests` | misc | `/pages/party-guests` | keep |
| `/pages/paul-frank` | collab | `/pages/collabs/paul-frank` | 301 |
| `/pages/paul-frank-for-jaded-london` | collab | `/pages/collabs/paul-frank-for-jaded-london` | 301 |
| `/pages/pelo` | campaign / editorial | `/pages/campaigns/pelo` | 301 |
| `/pages/people-and-talent-manager` | careers | `/pages/careers#people-and-talent-manager` | 301 |
| `/pages/people-talent-assistant` | careers | `/pages/careers#people-talent-assistant` | 301 |
| `/pages/pfw23` | stores / IRL | `/pages/stores/pfw23` | 301 |
| `/pages/point-break` | campaign / editorial | `/pages/campaigns/point-break` | 301 |
| `/pages/pop-up-store` | stores / IRL | `/pages/stores/pop-up-store` | 301 |
| `/pages/poster-for-jaded` | collab | `/pages/collabs/poster-for-jaded` | 301 |
| `/pages/poster-sign-up` | drop waitlist | `/pages/drops/poster` | 301 |
| `/pages/pr-manager` | careers | `/pages/careers#pr-manager` | 301 |
| `/pages/prima-swim` | campaign / editorial | `/pages/campaigns/prima-swim` | 301 |
| `/pages/princess-plastik` | campaign / editorial | `/pages/campaigns/princess-plastik` | 301 |
| `/pages/print-designer-mens` | careers | `/pages/careers#print-designer-mens` | 301 |
| `/pages/privacy-policy` | policy | `/policies/privacy-policy` | 301 |
| `/pages/product-size-guide` | size guide | `/pages/help/size-and-fit` | 301 |
| `/pages/production-coordinator` | careers | `/pages/careers#production-coordinator` | 301 |
| `/pages/puravida` | campaign / editorial | `/pages/campaigns/puravida` | 301 |
| `/pages/purity-campaign` | campaign / editorial | `/pages/campaigns/purity` | 301 |
| `/pages/rapid-search-results` | search | `/search` | 301 |
| `/pages/refund-policy` | policy | `/policies/refund-policy` | 301 |
| `/pages/requiem` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/requiem-first-access` | drop waitlist | `/pages/drops/requiem` | 301 |
| `/pages/returns-ca-en` | help centre | `/pages/help/returns-ca-en` | 301 |
| `/pages/returns-draft` | junk | `(delete)` | delete+301 to parent |
| `/pages/returns-eu-en` | help centre | `/pages/help/returns-eu-en` | 301 |
| `/pages/returns-gb-en` | help centre | `/pages/help/returns-gb-en` | 301 |
| `/pages/returns-info` | help centre | `/pages/help/returns-info` | 301 |
| `/pages/reviews` | misc | `/pages/reviews` | keep |
| `/pages/rewards` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/rock-revival-2026` | campaign / editorial | `/pages/campaigns/rock-revival-2026` | 301 |
| `/pages/rock-revival-collaboration` | collab | `/pages/collabs/rock-revival-collaboration` | 301 |
| `/pages/rock-revival-for-jaded-london` | collab | `/pages/collabs/rock-revival-for-jaded-london` | 301 |
| `/pages/rock-revival-sign-up` | drop waitlist | `/pages/drops/rock-revival` | 301 |
| `/pages/rockrevivalxjaded` | collab | `/pages/collabs/rockrevivalxjaded` | 301 |
| `/pages/ruine-campaign` | campaign / editorial | `/pages/campaigns/ruine` | 301 |
| `/pages/sale-download-the-app` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/saphira` | misc | `/pages/saphira` | keep |
| `/pages/saphira-campaign` | campaign / editorial | `/pages/campaigns/saphira` | 301 |
| `/pages/saphira-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/schott-2025-editions` | collab | `/pages/collabs/schott-2025-editions` | 301 |
| `/pages/schott-for-jaded` | collab | `/pages/collabs/schott-for-jaded` | 301 |
| `/pages/schott-sign-up` | drop waitlist | `/pages/drops/schott` | 301 |
| `/pages/search-results` | search | `/search` | 301 |
| `/pages/search-results-1` | search | `/search` | 301 |
| `/pages/search-results-page` | search | `/search` | 301 |
| `/pages/senior-graphic-designer` | careers | `/pages/careers#senior-graphic-designer` | 301 |
| `/pages/shanghai-pop-up` | stores / IRL | `/pages/stores/shanghai-pop-up` | 301 |
| `/pages/share-cart` | account | `/account/wishlist` | 301 |
| `/pages/shared-wishlist` | account | `/account/wishlist` | 301 |
| `/pages/shearling-boots-download-app` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/shearling-boots-sign-up` | drop waitlist | `/pages/drops/shearling-boots` | 301 |
| `/pages/sign-up-to-newsletter` | drop waitlist | `/pages/club` | 301 |
| `/pages/siren-campaign` | campaign / editorial | `/pages/campaigns/siren` | 301 |
| `/pages/sitemap` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/size-guide` | size guide | `/pages/help/size-and-fit` | 301 |
| `/pages/sleaze` | collab | `/pages/collabs/sleaze` | 301 |
| `/pages/sleazenation` | collab | `/pages/collabs/sleazenation` | 301 |
| `/pages/sleazenation-for-jaded` | collab | `/pages/collabs/sleazenation-for-jaded` | 301 |
| `/pages/sleazenation-paid-social` | collab | `/pages/collabs/sleazenation-paid-social` | 301 |
| `/pages/solaris-campaign` | campaign / editorial | `/pages/campaigns/solaris` | 301 |
| `/pages/sombre-ete` | campaign / editorial | `/pages/campaigns/sombre-ete` | 301 |
| `/pages/sombre-ete-sign-up` | drop waitlist | `/pages/drops/sombre-ete` | 301 |
| `/pages/spacebrat-editions` | collab | `/pages/collabs/spacebrat-editions` | 301 |
| `/pages/spirit-campaign` | campaign / editorial | `/pages/campaigns/spirit` | 301 |
| `/pages/spring-campaign` | campaign / editorial | `/pages/campaigns/spring` | 301 |
| `/pages/ss22-tropi-cool-swim-campaign` | campaign / editorial | `/pages/campaigns/ss22-tropi-cool-swim` | 301 |
| `/pages/ss22-tropi-cool-swim-campaign-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/stardom-campaign` | campaign / editorial | `/pages/campaigns/stardom` | 301 |
| `/pages/stores` | stores / IRL | `/pages/stores/stores` | 301 |
| `/pages/stores-2026` | stores / IRL | `/pages/stores/stores-2026` | 301 |
| `/pages/student-beans` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-australia` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-austria` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-belgium` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-canada` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-denmark` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-finland` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-france` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-germany` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-hong-kong` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-ireland` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-japan` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-netherland` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-new-zealand` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-norway` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-poland` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-spain` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-sweden` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-switzerland` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/student-beans-usa` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/students-discount-global-links` | student discount | `/pages/student-discount` | 301 (country auto-detect) |
| `/pages/style-guide` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/sub-rosa-sign-up` | drop waitlist | `/pages/drops/sub-rosa` | 301 |
| `/pages/subrosa` | campaign / editorial | `/pages/campaigns/subrosa` | 301 |
| `/pages/summer` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/sunglasses` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/survey-2026` | misc | `/pages/survey-2026` | keep |
| `/pages/swim` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/switchboard-donation` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/swym-share-wishlist` | account | `/account/wishlist` | 301 |
| `/pages/swym-wishlist` | account | `/account/wishlist` | 301 |
| `/pages/talent-recruiter` | careers | `/pages/careers#talent-recruiter` | 301 |
| `/pages/taxes-duties` | help centre | `/pages/help/taxes-duties` | 301 |
| `/pages/taxi-activation` | campaign / editorial | `/pages/campaigns/taxi-activation` | 301 |
| `/pages/team-spirit-campaign` | campaign / editorial | `/pages/campaigns/team-spirit` | 301 |
| `/pages/teenagefiction` | campaign / editorial | `/pages/campaigns/teenagefiction` | 301 |
| `/pages/terms-of-use` | policy | `/policies/terms-of-service` | 301 |
| `/pages/test` | junk | `(delete)` | delete+301 to parent |
| `/pages/thalita-campaign` | campaign / editorial | `/pages/campaigns/thalita` | 301 |
| `/pages/thank-you-for-subscribing` | drop waitlist | `/pages/club` | 301 |
| `/pages/the-parachute-pant-jaded-london` | hero franchise | `/pages/parachute` | 301 (mens/womens become tabs) |
| `/pages/the-parachute-pant-jaded-london-copy` | junk | `(delete)` | delete+301 to parent |
| `/pages/the-parachute-pants` | hero franchise | `/pages/parachute` | 301 (mens/womens become tabs) |
| `/pages/the-parachute-pants-mens` | hero franchise | `/pages/parachute` | 301 (mens/womens become tabs) |
| `/pages/the-parachute-pants-womens` | hero franchise | `/pages/parachute` | 301 (mens/womens become tabs) |
| `/pages/the-situation-has-escalated` | campaign / editorial | `/pages/campaigns/the-situation-has-escalated` | 301 |
| `/pages/tiktok-social-media-assistant` | careers | `/pages/careers#tiktok-social-media-assistant` | 301 |
| `/pages/tokyo-popup-2024-store` | stores / IRL | `/pages/stores/tokyo-popup-2024-store` | 301 |
| `/pages/track-your-order` | help centre | `/pages/help/track-your-order` | 301 |
| `/pages/trespass` | campaign / editorial | `/pages/campaigns/trespass` | 301 |
| `/pages/trespass-sign-up-page` | drop waitlist | `/pages/drops/trespass` | 301 |
| `/pages/tropi-cool-first-access` | drop waitlist | `/pages/drops/tropi-cool` | 301 |
| `/pages/uk-mainland` | help centre | `/pages/help/uk-mainland` | 301 |
| `/pages/unisex` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/unisex-spring` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/upgraded` | campaign / editorial | `/pages/campaigns/upgraded` | 301 |
| `/pages/upgradedlinmick` | misc | `/pages/upgradedlinmick` | keep |
| `/pages/usizy_feed` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/valeria` | campaign / editorial | `/pages/campaigns/valeria` | 301 |
| `/pages/valeria-sign-up` | drop waitlist | `/pages/drops/valeria` | 301 |
| `/pages/vendetta` | campaign / editorial | `/pages/campaigns/vendetta` | 301 |
| `/pages/vertigo-pt2-sign-up` | drop waitlist | `/pages/drops/vertigo-pt2` | 301 |
| `/pages/vertigomens` | campaign / editorial | `/pages/campaigns/vertigomens` | 301 |
| `/pages/violet-app-page` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/violet-jaded-london` | campaign / editorial | `/pages/campaigns/violet-jaded-london` | 301 |
| `/pages/violet-sign-up-page` | drop waitlist | `/pages/drops/violet` | 301 |
| `/pages/violet-sign-up-page-jaded-app` | drop waitlist | `/pages/drops/violet` | 301 |
| `/pages/vol-1-jaded-london` | campaign / editorial | `/pages/campaigns/vol-1-jaded-london` | 301 |
| `/pages/vol-1-sign-up-page` | drop waitlist | `/pages/drops/vol-1` | 301 |
| `/pages/vol1-campaign` | campaign / editorial | `/pages/campaigns/vol1` | 301 |
| `/pages/vol1-sign-up` | drop waitlist | `/pages/drops/vol1` | 301 |
| `/pages/vol1-sign-up-page-jaded-app` | drop waitlist | `/pages/drops/vol1` | 301 |
| `/pages/volare` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/volare-swim` | empty body | `(review)` | theme-section page or empty: confirm in admin |
| `/pages/volare-swim-first-access` | drop waitlist | `/pages/drops/volare-swim` | 301 |
| `/pages/wasted-potential-campaign` | campaign / editorial | `/pages/campaigns/wasted-potential` | 301 |
| `/pages/where-is-my-order` | help centre | `/pages/help/where-is-my-order` | 301 |
| `/pages/wholesale-coordinator` | careers | `/pages/careers#wholesale-coordinator` | 301 |
| `/pages/wishlist` | account | `/account/wishlist` | 301 |
| `/pages/womens` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/womens-black-friday` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/womens-denim-app` | landing duplicate of collection | `(merge)` | 301 to matching collection / app deep link |
| `/pages/womens-denim-fit-guide` | size guide | `/pages/help/size-and-fit` | 301 |
| `/pages/womens-social-pr-manager` | careers | `/pages/careers#womens-social-pr-manager` | 301 |
| `/pages/womenswear-design-manager-mat-cover` | careers | `/pages/careers#womenswear-design-manager-mat-cover` | 301 |
| `/pages/womenswear-designer` | careers | `/pages/careers#womenswear-designer` | 301 |

The full map, including every collection and all 2,058 product URLs, is in `migration_map.csv`.

## Gaps (need the Claude in Chrome capture)

- Live navigation menus, header/footer links, homepage sections and theme templates (Shopify JSON does not expose them).
- USD prices for the `/en-us` market (catalogue is GBP; Markets price lists are applied only on `jadedldn.com`).
- Scripts, page weight, Core Web Vitals, structured data and screenshots of the current storefront.
- Content of the 20 pages whose body is empty (built in theme sections), including `/pages/new-york-store-2026`, `/pages/stores-2026`, `/pages/sleazenation`, `/pages/rock-revival-collaboration`.
