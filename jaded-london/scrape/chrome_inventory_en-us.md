# Jaded London (jadedldn.com/en-us): Content Inventory for Redesign Audit

Captured 21 Oct 2026, US store (USD), desktop Chrome \~1440px. Read-only browsing: nothing added to cart, no forms submitted, no login.

  

**URL shorthands used below**

  

  - ASSET/ = https://assets.jadedldn.com/image/upload/e\_sharpen:70,w\_1600,c\_limit/shopi/cdn/shop/files/ (Cloudinary-style proxy in front of Shopify files; banners use this)
  - CDN/ = https://jadedldn.com/cdn/shop/files/
  - PCDN/ = https://cdn.shopify.com/s/files/1/0022/9824/9267/files/ (product images)
  - VID/ = https://assets.jadedldn.com/video/upload/w\_2000,c\_limit,q\_auto,f\_auto:video,ac\_none/shopv/videos/c/o/v/
  - SHG/ = https://i.shgcdn.com/ (Shogun page-builder images)

  

-----

## 0\. Global elements (every page)

### Announcement bar (US variant: section announcement-USA)

Dark charcoal bar, single line, auto-rotating ticker (approx. every 3-4 s). Separate hidden variants exist for ROW, UK, AUS, EU.

  

1.  "THE SOUND ROOM NYC" → /en-us/pages/jaded-x-nothing-nyc
2.  "10% OFF YOUR FIRST ORDER" → /en-us/pages/10-off-your-first-order
3.  "FREE SHIPPING ON ORDERS OVER $150" → /en-us/pages/delivery-info

### Header

  - Left: "Jaded London" wordmark logo (CDN/test2\_180x@2x.png, white version CDN/testwhite2\_180x@2x.png, alt "Jaded London"; note "test" filenames in production).
  - Right utility icons: Search (opens full-width search overlay), Wishlist heart (/en-us/apps/wishlist, Swym), Bag (/en-us/cart), Hamburger.
  - **No visible top-level nav on desktop.** All navigation lives in a right-hand slide-out drawer opened by the hamburger, even at desktop width.
  - Header is sticky; becomes semi-transparent white over hero when scrolling. Announcement bar scrolls away.
  - Country/currency selector lives only inside the drawer ("UNITED STATES (USD $)" dropdown, Global-e).

### Navigation drawer (exact order)

**Women +**

  

  - Home (/pages/womens)
  - New Arrivals (/collections/new-in-womens)
  - Bestsellers (/collections/womens-bestsellers-jaded)
  - Shearling Boots NEW (/collections/shearling-boots)
  - Nolita NEW COLLECTION (/collections/nolita-collection)
  - Party Edit (/collections/autumn-party-edit)
  - Clothing +: View All, Dresses, Tops, Corsets, Knitwear, Jeans, Bottoms, Outerwear, Joggers & Sweatpants, Hoodies & Sweatshirts, Matching Sets & Co-Ords, Swimwear, Skirts, Unisex, Basics, Shorts & Jorts
  - Dresses +: All Dresses, Party Dresses, Maxi Dresses (/collections/evening-dresses), Backless Dresses, Day Dresses
  - Outerwear
  - Denim Fit Guide (/pages/womens-denim-fit-guide)
  - Jeans +: Slim/Straight, Bootcut, Baggy/Oversized, Statement, Jorts, Denim Fit Guide, All Denim
  - Shop By Edit +: Cleo Edit, Camo Edit, Bandage Edit, Lace Edit, Animal Print Edit
  - Swim (/pages/swim)
  - Launches +: Shearling Boots NEW, Nolita NEW, Violet, Devon, Lola
  - View All, Footwear, Back in Stock, Accessories, Sale

  

**Men +**

  

  - Home (/pages/mens), New Arrivals, Shearling boots NEW, block.exe NEW COLLECTION, View All, Bestsellers
  - Clothing: Tops, T-Shirts & Vests, Jeans, Bottoms, Trousers, Outerwear, Joggers & Sweatpants, Knitwear, Shirts, Hoodies & Sweatshirts, Tracksuit Sets, Basics, Shorts
  - Jeans: Bootcut, Baggy/Oversized, Slim/Straight, Jude Jeans, Jorts, Denim Fit Guide, All Denim
  - Outerwear
  - Launches: Shearling Boots NEW, block.exe NEW COLLECTION, VOL.1, Trespass, Europa, Rock Revival by Jaded London (/collections/mw-rock-revival-2026)
  - Denim Fit Guide, View All, Accessories, Jude Jeans, Back in Stock, Tailoring (/collections/tailoring-aw25), Footwear, Sale

  

**Swim +**: Home, Women's Swimwear, Bestsellers, Bikini Sets, Bikini Tops, Bikini Bottoms, Beach Cover Ups, Beach Dresses, Beach Co-ord Sets, Sale

  

**Unisex +**: Unisex Bestsellers, Unisex Tops, Unisex Bottoms, Unisex Coats & Jackets

  

**Denim Fit Guide +**: Women's Denim Fit Guide, Men's Denim Fit Guide

  

**Sale +**: Women's Sale, Men's Sale

  

**Stores +**: New York Store (/pages/new-york-store-2026), LA Store (/pages/la-store-2026)

  

**Login** · **UNITED STATES (USD $)** selector

  

Note: a second, legacy hidden sidebar-menu section is still in the DOM with old links (New In, Women's, Men's /pages/mens-1, Instagram Shop, Contact, Delivery, Returns, Size Guide, FAQ, app links, and both @jadedldn and @jaded\_man socials).

### Footer

Four columns on a white background, accordion style even on desktop:

  

1.  **Customer Service +**: Contact Us, Delivery, Returns, Size Guide, FAQ (https://faq.jadedldn.com/, external), Account Login
2.  **Brand +**: Stores (/pages/stores-2026), Campaigns, Editions, Pop-Up Stores (/pages/stores), Community Rewards, Gift Cards, Careers
3.  **Student Discount +**: Student Beans (/pages/students-discount-global-links), UNiDAYS (myunidays.com/partners/jadedlondon/micro)
4.  **Terms & Conditions +**: (same links as legal row)

<!-- end list -->

  - **Follow Us**: Instagram (@jadedldn), YouTube, TikTok (@jadedldn) icons. (No Jaded Man socials in footer.)
  - **Download App**: iOS (App Store id1539936585, GB store link), Android (Google Play).
  - **Newsletter**: heading "10% off your first order", body "Sign up to our newsletter for 10% off your first full price order as well as exclusive early access to new collection launches.", email field + "Submit".
  - **Legal row**: "© 2026 Jaded London |" Terms of Use · Privacy Policy · Cookies Policy · Accessibility Statement · Corporate Social Responsibility · EU Right to Withdrawal (EU link shown on US store).
  - **No payment icons** in footer.

### Floating widgets

  - Bottom-left: Gorgias chat bubble (round, black "…").
  - Bottom-right: EqualWeb accessibility overlay button (black circle, person icon).

### Popups

  - No newsletter, cookie or region popup appeared on load or after 10+ seconds on desktop in this session (the browser had previously visited and set the US region, so first-visit popups may have been suppressed). A popup section exists in the theme but was empty.

  

-----

## 1\. Homepage /en-us

  - **Title**: "Jaded London | Official Online Store"
  - **Meta**: "Discover global inspired street style and cutting edge trends. Designed in London, delivered worldwide. Free Delivery over $150."
  - **Sections (top to bottom)**: the entire homepage is one full-viewport hero, then the footer.
      
    1.  **Split hero** (home\_banner\_section\_us): campaign photo on a pale white/grey seamless studio backdrop of a young man (black military-frogging zip jacket, grey jeans, black ribbed shearling boots) and a young woman (shaggy grey shearling vest, grey skinny jeans, pink studded shearling boots), both sitting on the floor. Text links "Menswear" (left, → /en-us/pages/mens) and "Womenswear" (right, → /en-us/pages/womens) in grey sans-serif over the image. No headline, no CTA button, no product.
          
          - Desktop: ASSET/DESK\_SHEARLING\_SPLIT\_V3.jpg
          - Mobile: ASSET/MOB\_SHEARLING\_SPLIT\_V2.jpg
          - Both have empty alt text.
    2.  Footer.
  - Hidden sections for other markets (home\_banner\_section\_MPd3ag, \_au\_) present but empty for US.
  - **Mobile notes** (from markup; screenshot not possible, see Part C): separate mobile crop of the same hero; same two text links; same drawer nav.

  

-----

## 2\. Gender landing pages

### Womens /en-us/pages/womens

  - **Title**: "Womenswear | Jaded London"; **Meta**: "Shop the hottest pieces across swimwear and dresses, denim to skirts and more at Jaded London, making the perfect wardrobe additions."

<!-- end list -->

1.  Full-width banner, text "Shop New in" → /collections/new-in-womens. Desktop ASSET/Untitled-8\_copy.jpg, mobile ASSET/NEW\_IN\_MOB\_copy.jpg (note "Untitled" filename).
2.  4-tile category row: Dresses, Outerwear, Tops, Bottoms. Images: ASSET/image\_7a74a406-81b1-455b-bbfe-741b78164d61.png, ASSET/JWJK6048\_F4.jpg, ASSET/TOPS\_c5d683d4-….jpg, ASSET/BOTTOMS\_2fadf58b-….jpg.
3.  Banner "Shearling boots / Shop now" → shearling-boots. ASSET/WW\_CAMO\_SHEARING\_V1.jpg (mob), ASSET/WW\_CAMO\_DESK\_V1.jpg (desk). Camo shearling boot campaign.
4.  Banner "Shop Denim" → **womens-denim-fit-guide** (not the denim collection). ASSET/DENIM\_DESK\_copy.jpg, ASSET/DENIM\_MOB\_copy.jpg.

### Mens /en-us/pages/mens

  - **Title**: "Menswear | Jaded London"; **Meta**: "From denim jeans and jorts, to t-shirts, hoodies and more. Shop Jaded London's menswear here for statement pieces and wardrobe staples."

<!-- end list -->

1.  Banner "Shop Outerwear" → /collections/jaded-man-jackets. ASSET/OUTERWEAR\_BANNER\_20\_OCT\_DESKTOP\_2.jpg, ASSET/OUTERWEAR\_BANNER\_20\_OCT\_MOBILE.jpg.
2.  4-tile row: New In, Bottoms, Denim, Knitwear. ASSET/JMT7076\_F3\_….jpg, ASSET/JMCP6936\_F1\_….jpg, ASSET/WEB\_HEARTDENIM\_13.10.jpg, ASSET/JMKW6785\_F1\_….jpg.
3.  Banner "Shop block.exe" → /collections/block-exe. ASSET/DESKTOP\_TESTA\_1\_….jpg, ASSET/NEW\_IN\_MW\_13.10\_….jpg.

### Swim /en-us/pages/swim

  - **Title**: "Swim" (no brand suffix); **Meta**: empty.

<!-- end list -->

1.  Banner "Shop New In" → womens-swimwear. ASSET/DESK\_SWIM\_NEW\_IN.jpg, ASSET/MOB\_SWIM\_NEW\_IN.jpg.
2.  4 tiles: Bikinis, Beach Dresses, Bestsellers, Shop All. ASSET/JSBT6289\_F2\_0726\_….jpg, ASSET/JWD5586\_FLF2\_0226\_….jpg, ASSET/21APRWWECCOM33048\_….jpg, ASSET/JWS5583\_FLF1\_0226\_….jpg.

<!-- end list -->

  - Summer swim landing still prominent in late October.

  

-----

## 3\. Collection pages (PLPs)

**Shared PLP template (all collections)**: sections shogun-helper, shogun-above, main, recently-viewed-products, shogun-below.

  

  - **Layout**: edge-to-edge 4-column grid on desktop, no gutters, no collection title or intro text visible above the grid, tall 3:4-ish cards on pale grey studio backgrounds.
  - **Card**: two images (hover swaps to alternate view), wishlist heart top-right, "+" quick-add bottom-right that reveals a size row and "Add To Bag", product name, price, and "N Colours" line when the style has colourways (e.g. "2 Colours").
  - **Sticky bottom bar**: "Sort" (left) and "Filter" (right).
  - **Sort options**: Most relevant, Price low to high, Price high to low, Newest.
  - **Filters**: Size (mixes XXS-XXL, UK 3-16, "UK16" duplicate, W24-W38, ONE SIZE/One Size duplicates), Product type, Gender (dirty values: "Men", "Women", "women", "Womens"), Colour, In Stock / Out of stock. "See results" button.
  - **Pagination**: numbered pages, 48 products per page.
  - **Badges**: low-stock only ("4 left in stock"); no NEW or % OFF badges on cards.
  - **Sale cards** show sale price then original price (e.g. "$140 $195").
  - **Recently viewed** carousel below grid.
  - No swatches on cards (colour count text only).

  

|  |  |  |  |  |
| :-: | :-: | :-: | :-: | :-: |
| \*\*Collection\*\* | \*\*Title tag\*\* | \*\*Meta (abridged)\*\* | \*\*Pages\*\* | \*\*First products\*\* |
| New In Womens /collections/new-in-womens | New Arrivals Womenswear \| Jaded London | Shop the latest Jaded London Women's Collection… Free Delivery and Free Returns Available | 7 | Black Drummer Hoodie $180 (a Jaded Man style, JMH), Black Leather Drummer Shearling Boots $285, Aporial Funnel Buckle Knit Dress $170, Vivienne Lace Fringe Dress $170, Anve Crop PU Leather Jacket $270, Ardor Seamed Jeans in Washed Black $195, Field Khaki Jacket $245… |
| All Womens /collections/womens-all | Women's Streetwear & Clothing \| Y2K Fashion for Women | Discover Jaded London's full women's clothing collection, featuring bold contemporary pieces… | 14 (\\\~628 in stock, 299 OOS) | Ixia Chiffon Bandana Scarf Dress $190, Isen Knit Mini Dress in Green $155, Crush Stripe Backless Mini Dress $100, Alessia Jewelled Halter Mini Dress $180, Roswen Lace Corset Top in Green $155… Parachute Cargo Shorts $100 |
| Womens Denim /collections/all-womens-denim | Denim Outfits \| Women's Denim Outfits | …statement and oversized pieces… | 3 | Ardor Seamed Jeans $195, Rhiannon Extreme Low-rise Bootcut $195, Tori Distressed Lace Low Rise Straight $195, Leona Bootcut Cooper Jeans in Croc $155, Leni Low Rise Flare $170, Kelsey Low Rise Slim Bootcut $155… |
| Womens Bottoms /collections/womens-bottoms | Women's Bottoms \| Casual Trousers & Bottoms for Women | Complete your look… | 7 | Norien Slashed PU Leather Trousers $220, Idol Croc Effect Bandage Trousers $195, Rhiannon Bootcut $195, Alula Embellished Mini Shorts $100, Roswen Satin Lace Mini Skirt $155, Dollie Sequin Lace Mini Shorts $98, Cleo Slouchy Bootcut Jogger $145, Panel Mesh Vapor Joggers $180… |
| New In Mens /collections/new-in-mens | New Arrivals Menswear \| Jaded London | Shop the latest design and trends from Jaded London Menswear… | 7 | Heart XL Colossus Jeans $190, Tan Suede Drummer Shearling Boots $285, Heart T-Shirt $80, Stud Muse Straight Leg Jeans $195, Saken Purple Cropped T-Shirt $80, Boxer Colossus Jeans $195, Ornate Double Breasted Military Jacket $300, Parachute Pants in Grey Check $170… |
| All Mens /collections/mens-all | Men's Clothing \| Jaded Man \| Jaded London | Shop men's clothing… signature colossus fits with washed, distressed finishes. | 9 | Saken Purple Cropped T-Shirt $80, Heart XL Colossus Jeans $190, Parachute Pants in Grey Check $170, Boxer Colossus Jeans $195, Storm Knitted Hoodie $145, 1947 Black Hoodie $180, Long Sleeved Henley Knit Top $155… |
| Mens Denim /collections/all-mens-denim | Men's Denim Clothing & Outfits | …From baggy jorts to denim jeans and jackets… | 3 | Drummer Muse Low Rise Straight $190, Stud Muse $195, Indigo Baggy Twisted Seam $190, Boxer Colossus $195, The Blessed Endeavour XL Colossus $195, Bedrock Drift Bootcut $190, Stud Blue Jude Bootcut $195, Drain Jeans $170… |
| Mens Trousers /collections/mens-trousers | Men's Pants \| Men's Cargo Pants & Suit Pants | Shop Jaded London's men's pants \*\*& women's cargo pants\*\*… | 1 (27 items) | Black Pinstripe Stacked Straight Suit Pants $130, Goliath Black Suit Pants $115, Tattoo Pinstripe Goliath $135, Oxblood Faux Leather Pants $180, California Camo Ripstop Cargos $190, Washed Black XL Parachute Cargo Pants $170, Black Parachute Cargo Pants $130, Camo Carpenter Cargo $190, Brown Check Cadet Cargos $190 |
| Womens Swimwear /collections/womens-swimwear | Women's Swimwear \| Swimwear & Beachwear for Women | Find your summer fits… | 3 | Idol Metallic Bandage Bikini Top/Bottoms in Gold $100/$100, Clementina Wired Cup Bikini Top $100, Freda Check Triangle Bikini Top $78, Tessera Jewel Cut Out Swimsuit $180, Selka Metal Bead Crochet Bikini $125/$115, Sarong $190… |
| Womens Sale /collections/sale-womens | Women's Clothing Sale \| \*\*Women's Summer Sale 2026\*\* | Our women's summer clothing sale is here\\\!… | 8 | Serilda Sequin Chiffon Midi Dress $140 (was $195), Zelya Beaded Crochet Halter Top $45 ($145), Willow Terry Bikini $62 ($89), Briony Studded Satin Cargo Trousers $160 ($195), Rebel Military PU Leather Top $84 ($170)… |
| Mens Sale /collections/sale-mens | Men's Clothing Sale \| \*\*Menswear Summer Sale 2026\*\* | …limited time only… | 2 | Slate Shirt $62 ($125), Jinx Balloon Jorts $115 ($145), Rider Moto Jacket $115 ($190), Black Oil Wash Parachute Pants $93 ($155), Stud Denim Jacket $180 ($295)… |
| Womens Basics /collections/womens-basics | Women's Basics | (empty) | 3 | 13 Stripe Straight Jogger (4 colours) $170, Mist Racer Maxi Dress $135, Mist V Neck Top $71, Cleo Slouchy Bootcut Jogger $145, Los Angeles Distressed Raglan Top $80… |
| Mens Basics /collections/mens-basics | Men's Basics \| Basic Clothing for Men | Elevate your essentials… | 3 | Mist Hoodie $78, Haze Henley T-Shirt $80, Mist Vest $67, Ecru Waffle Henley Top $110, White Bite T-Shirt $115, Jude Bootcut Jeans $190… |

  

Card image example (womens-all first card): CDN/JWD5791\_1\_800x.jpg and hover CDN/JWD5791\_6\_800x.jpg, alt "Ixia Chiffon Bandana Scarf Dress – view 1/2". Product card alts are populated; banner alts are not.

  

-----

## 4\. Product pages (PDPs)

**Shared PDP template**

  

  - Layout: left half large image carousel with prev/next arrows (no thumbnails visible above the fold); right half: title, price, Size selector (text buttons; **first size pre-selected/underlined by default**), Color, optional fit line (e.g. "THIS STYLE HAS BEEN DESIGNED FOR UNISEX"), "ADD TO BAG" (black full-width), "ADD TO WISHLIST", then accordions: Description, Shipping, Returns.
  - Low-stock line "Only N items in stock\!" (shown even at 143 units).
  - Reviews: Judge.me widget ("No reviews" / "241 reviews"); some products show "borrowed" grouped reviews.
  - Klarna and Afterpay placements are in the markup but **no BNPL messaging was visible** next to price at the time of capture.
  - Size guide: full multi-tab size guide (Women / Men / Unisex; Denim, Tops & Hoodies, Dresses, Skirts, Trousers & Shorts, Coats, Knitwear, Swimwear, Footwear, Shearling Boots; CM/IN toggle; UK/US/EU/IT/AU conversion) embedded in every PDP as a modal.
  - "Styled With" shop-the-look block with mini quick-add on some PDPs.
  - "You May Also Like" (Shopify product recommendations) and "Recently Viewed" below.
  - Sticky "Add to bag - $X / Select Size" bar.

  

**Shipping accordion copy (US)**: "Standard shipping cost - $6.99 · Standard shipping timeframe (business days) - 4-7 · Express shipping cost - $15 · Express shipping timeframe (working days) - 1-3 · Free shipping over $150 · All taxes and duties are included. We guarantee no additional charges on delivery. For information on shipping please click here."

  

**Returns accordion copy**: "We are happy to refund any items within 30 days of receipt. if 30 days have gone by since your purchase, unfortunately we can't offer you a refund. To be eligible for a return, your item must be unworn with the original tags attached, in the original packaging and all swimwear must be returned with the hygiene sticker attached. if our customer care team feel any of these points are not met, it is at their discretion on whether the item is suitable for return. should a refund be refused your item will be returned to you. Items marked as non-refundable including but not limited to, beauty products, haircare or earrings can not be returned once packaging has been opened due to hygiene reasons. To see our full returns policy please click here." (lowercase sentence starts as on site)

### 4a. Washed Black XL Parachute Cargo Pants (womens) /en-us/products/washed-black-xl-parachute-cargo-pants-ww

  - Vendor Jaded London · Type Pants · **$170**, no compare-at · Sizes XXS-XXL, all in stock · Colour Black · "THIS STYLE HAS BEEN DESIGNED FOR UNISEX" · "Only 11 items in stock\!" · No reviews.
  - **Description**: "Washed Black XL Parachute Cargo Pants · New XL Parachute fit · Oversized fit · Heavy cotton ripstop fabric · 6-pocket styling · Metal zip fly front with bar tack detail and concealed button closure · Drawcord waistband · Mid-low rise · Antique silver stud detailing at pockets · Knee panelling for volume · Adjustable drawcord hem · Carli is 5 ft 10 and wears a size XS · Style code: JMCP7092"
  - **Composition/care**: 100% Cotton. Machine wash at 30 degrees, cool iron on reverse, wash inside out, lay flat to dry.
  - **Tags**: unisex, parachute, la-miami-pop-up, staff, "WW UX Sept 2026", COLLECTION:UnisexCampaign…
  - **Images (11)**: PCDN/JMCP7092\_3.jpg, \_1, \_4, \_2, \_5, \_6, \_9, \_7, JMCP7092\_F3\_aa218e30-….jpg, JMCP7092\_F4\_83f61e7c-….jpg, JMCP7092\_F2\_bcf8e151-….jpg. Lead image shows the model in a studded black puffer jacket and sunglasses (pants cropped out of the first frame).
  - A men's duplicate exists: /products/washed-black-xl-parachute-cargo-pants (the catalog duplicates many unisex styles with a -ww suffix).

### 4b. Heart XL Colossus Jeans (mens) /en-us/products/heart-xl-colossus-jeans

  - Vendor **Jaded Man** · Type Baggy Jeans · **$190** · W26-W38 (W26, W28 sold out) · Colour "Black" (tag says colour\_blue; product is dark indigo with pink stars/heart crotch print) · "Only 28 items in stock\!" · **241 reviews**.
  - **Description**: "LDN XL Colossus Heart Jeans · XL Colossus fit · A baggier fit to our original colossus jean · Heavy non-stretch slub indigo fabric · 5 pocket styling · \<3 crotch print · Model is 5 ft 9, and wears a size W30 for an oversized fit. · Style code: JMJE7108"
  - **Composition/care**: 100% Cotton. Cold hand wash separately, no biological detergents, wash darks separately, inside out, colour may transfer/fade, lay flat, do not rub stains, iron on reverse, do not pile whilst damp.
  - **Images (11)**: PCDN/JMJE7108\_F1.jpg, download\_d6ee195d-….jpg, JMJE7108\_F1\_f5a4cd0d-….jpg, JMJE7108\_F3\_7532445a-….jpg, JMJE7108\_B1.jpg, download\_2b817bb0-….jpg, download\_29047c6c-….jpg, JMJE7108\_F2.jpg, JMJE7108\_F2\_6634f4c1-….jpg, JMJE7108\_F3.jpg, JMJE7108\_F4.jpg ("download\_" filenames suggest UGC/downloaded imagery).
  - Tags: block.exe, nyc-store, COLOSSUS. Womens duplicate heart-xl-colossus-jeans-ww.

### 4c. Vivienne Lace Fringe Dress /en-us/products/vivienne-lace-fringe-dress

  - Vendor Jaded London · Type Mini Dresses · **$170, compare-at $170** (same value, data error) · UK 4-16 all in stock · Black · "Only 12 items in stock\!" · **11 reviews** (with review highlights/keywords blocks).
  - **Description**: "Dramatic asymmetric dress · Baroque woven fabric · Long tassels · One shoulder · Mini to midi length · Sheer · Black colourway · Shorts not included · Model is 5 ft 9 and wears a size S · Product Code: JWD4661"
  - **Composition/care**: 50% Cotton, 50% Polyamide; Fringe 100% Polyester. Hand wash separately, reshape whilst damp, avoid snagging, lay flat.
  - **Styled With**: Washed Black Drift Bootcut Jeans $170 (3 colours) with inline size select + Add To Bag.
  - **Images (8)**: PCDN/JWD4661\_3.jpg, \_6, \_5, \_1, \_4, \_8, \_7, \_2.
  - Tags reveal reuse since SS24 (ss24, blackfriday2024, XMAS WW 2025, Oct Party Edit 2026) yet still in "New in".

### 4d. Idol Metallic Bandage Bikini Top in Gold /en-us/products/idol-metallic-bandage-bikini-top-in-gold

  - Vendor **Jaded Swim** · Type Bikini Tops · **$100, compare-at $100** · XS-XL (M sold out) · Gold · "Only 143 items in stock\!" · **4 reviews**.
  - **Description**: "This striking metallic gold bikini top features stretch knitted bandage fabric with a high-shine foil finish. A bandage halterneck strap provides support, while a gold clasp fastening completes the look. Matching bikini bottoms available. Details: Stretch fabric, Metallic gold, Halter neck, Clasp fastening, 96% polyester, 4% elastane. Brittany is 5 ft 9 and wears a size S. Product Code: JSBT5601"
  - **Care**: Hand wash only, lay flat, rinse after use, avoid snagging, colour change with sun/chlorine, not for prolonged sea/chlorine use due to foil finish, possible foil loss.
  - **Styled With**: Idol Metallic Bandage Bikini Bottoms in Gold $100; Idol Metallic Bandage Corset Top in Gold $170.
  - **Images (8)**: PCDN/JSBB5602\_F3\_1125\_….jpg (lead image is the *bottoms* SKU), JSBT5601\_F2\_1125\_…, JSBT5601\_F4\_1125\_…, JSBB5602\_FLF2\_1125\_…, JSBB5602\_B1\_1125\_…, JSBT5601\_F1\_1125\_…, JSBT5601\_FLF2\_1125\_…, JSBT5601\_FLF1\_1125\_….

  

-----

## 5\. Parachute landing pages (Shogun-built, legacy)

### /en-us/pages/the-parachute-pant-jaded-london

  - **Title**: "Parachute | Jaded London"; **Meta** contains typos: "virtual cargo trend", "Kylier Jenner".
  - Centered serif-less heading "PARACHUTE", intro: "The new wardrobe staple. Covering every corner of 'cargo', our Parachute collection is the embodiment of the viral cargo trend. The unisex nature of the garment has united both of our brands, which has had a huge influence on the success of the collection. Our parachute pants have been worn by a roster of the Insta superstars: Kylie Jenner, Hailey Bieber and Kaia Gerber."
  - Italic grey note: "Please keep in mind when purchasing that although our parachute pants are a unisex product, the sizing is different across women's and men's. A women's size small is equivalent to a men's size xsmall."
  - Two columns "MENS" / "WOMENS" each with a campaign image (MENS: older man with dreadlocks in a cream knit, khaki parachute pants, rust wall; WOMENS: model with curly hair, khaki cargo corset, holding snowshoes/hiking gear on grey backdrop), product cards (Ecru Parachute Cargo Pants "Sold out", Brown $130; Khaki $130, Ecru $130), "SHOP MENS PARACHUTE PANTS" / "SHOP WOMENS PARACHUTE PANTS", long campaign copy (Herbie Mensah as face of Jaded Man campaign; inspiration M-51 & M-65 U.S. Army field pants; womenswear "explorer" campaign with y2k cargo skirts, matching corsets, umbra dress). Typos: "bought a strong sense", "huge arrange of hiking gear". "SHOP ALL" CTA.
  - Images: SHG/6f67d448-ba67-4df3-998c-5061ad3662de/, SHG/7e769e5d-c205-4535-ae42-d7de792e894d/, CDN/17\_JAN\_MW\_ECCOM0125\_2\_2048x.jpg, CDN/17\_JAN\_MW\_ECCOM0093\_2\_2048x.jpg, SHG/ab67b8f6-…/, SHG/e5f7a75f-…/, SHG/741395f9-…/.

### /en-us/pages/the-parachute-pants-womens and /the-parachute-pants-mens

  - Same structure: "PARACHUTE / WOMENS" (or MENS), intro, sizing note, campaign copy, product cards.
  - **Bug: prices render in GBP on the US store** ("£65.00", "£45.00", "Ecru Cargo Corset £48.00"), and the mens page shows three price-only cards with missing product names.

  

-----

## 6\. Campaign / collab pages

### Rock Revival /en-us/pages/rock-revival-collaboration

  - **Title**: "Rock Revival by Jaded Collaboration 2026"; **Meta**: "Introducing our second collaboration with Rock Revival by Jaded London. A collision of rebellious heritage and contemporary energy, the Rock Revival by Jaded London capsule redefines core denim."

<!-- end list -->

1.  Full-bleed autoplay video hero (grainy VHS-style footage, red pickup truck under trees in a California canyon). Desktop poster CDN/DESK\_POSTER\_d3d4ec67-3493-4bad-850d-679d56ca1ae8.jpg, video VID/a21282764fb1461299aed4372c8a0a4c.mp4; mobile poster CDN/MOB\_PPSTER.jpg, video VID/2b5e45a19a25455da27b71268f3c9d44.mp4.
2.  Text block: "Rock Revival by Jaded London" + body: "Introducing our second collaboration with Rock Revival by Jaded London. A collision of rebellious heritage and contemporary energy, the Rock Revival by Jaded London capsule redefines core denim. Statement pieces are cut with precision and finished with bold studs, heavy stitch detailing and a worn-in finish. Grounded by essential jersey staples, the collection balances grit and ease, a seamless fusion of two worlds." Then dates: "Store Exclusive Early Access Wednesday 8th April · NY Store: 434 Broadway, NY, 10013 · LA Store: 8483 Melrose Avenue, CA 90069 · App Exclusive Early Access Wednesday 15th April 8pm BST / 3pm EST / 12pm PST · Full Collection Available Online Thursday 16th April 8pm BST / 3pm EST / 12pm PST at jadedldn.com" (launch info is six months stale; no shop CTA).
3.  Image banner https://assets.jadedldn.com/image/upload/e\_sharpen:70,w\_1920,c\_limit/shopi///cdn/shop/files/desk\_rr.jpg (note triple slash).
4.  Newsletter: "Want to know more? Sign up to find out when to shop early access for all upcoming launches and collections." + Subscribe.

### Sleazenation /en-us/pages/sleazenation

  - **Title**: "Sleazenation"; Meta empty.

<!-- end list -->

1.  Shop-now image → /collections/sleazenation (ASSET/shop\_now\_mob.jpg, ASSET/shop\_now\_desktop.jpg).
2.  Text: "Jaded London has collaborated with Sleazenation Magazine to curate a collection of artworks from their archive, which captures British youth culture of the late 90s & early 00s. The curation has been used across a capsule collection which consists of photographic sublimation prints direct to ready-made garments, to screen printing of graphic artwork across jersey as well as all over prints to knit & accessories."
3.  "VIEW THE COLLECTION" grid of 15 product links (rave-tee, red-how-are-you-tee, ibiza-passion-tie-1, f-ckin-tune-hot-pants, ibiza-kiss-mesh-long-sleeve, undressed-mini-skirt, moto-girls-baby-tee, millennium-flame-tee, how-are-you-tote-bag, 2003-tee, kissing-club-tee-1, black-how-are-you-tee-2…) linking to **non-localised** https://jadedldn.com/products/... URLs. Images ASSET/WW26OCT8280.jpg, ASSET/19-10-mens6133.jpg, ASSET/Artboard\_3\_….jpg, ASSET/WW26OCT9070\_….jpg, ASSET/WW26OCT9019\_….jpg, ASSET/WW26OCT8991.jpg.
4.  Image pair → collection (ASSET/Artboard\_6\_….jpg, ASSET/Artboard\_1\_….jpg).
5.  Text: "Sleazenation was a British monthly fashion and lifestyle magazine printed by Swinstead Publishing in London between 1996 and 2003. The first of its kind, Sleazenation was one of the UK's most influential publications, inspiring the "new hipster" movement in London's East End in the late 1990s and compared by subsequent writers and critics with Dazed and Confused."

### LDN to NYC /en-us/pages/ldn-to-nyc (Shogun, blog-style editorial)

  - **Title**: "LDN TO NYC | Jaded London". Heading "LDN TO NYC", sub "DINNER / POP UP / PARTY", dated September 15th, 2022.
  - Sections: THE PARTY (NYFW activation, 3-day pop-up at VFILES, JADED X VFILES merch); video credit @satananthony; "POP UP | I ♥ LDN: The Mercer St Takeover." long copy (12 Mercer St, home & away football merch, screen printing by @bcconyc); "VFILES X JADED CAMPAIGN" credits (photographer @\_JOSHUO, models @monicamllonch @okfloki, team list); "DINNER | FANELLI'S NYC" copy with guest handles; "Written by Jaded Ldn"; "Other News": VERTIGO, AW22 BLUEPRINT. Large empty gap above content while media loads.

### Jaded x NOTHING / The Sound Room /en-us/pages/jaded-x-nothing-nyc (linked from announcement bar)

  - **Title**: "Jaded London x NOTHING"; **Meta**: "…Immersive listening experience at our New York City store, download the App for entry. Opening September 16th 2026."

<!-- end list -->

1.  Video hero: posters CDN/DESKTOP\_POSTER\_e9da3d9c-5ca8-448d-9d68-ab4e035d4085.jpg / CDN/MOBILE\_POSTER\_acfc5fc9-….jpg, videos VID/4ce5f628a6fb44a3a165b3f5fc32f076.mov / VID/9c5b51b156fe4b22853df39b84c3fa55.mov (.mov delivery).
2.  Image banner …/DESKTOP\_2\_32507a49-….jpg.
3.  Text: "Join us for an exclusive immersive listening experience at our New York City store, in collaboration with NOTHING. Now open at 434 Broadway, New York, NY 10013, DJs featured include: MANUKA HONEY @mariimals · THE TWINS @waitareyoutwins · JOAO LAGRIMA DE OURO @joao.lagrima.de.ouro · BOY PILLOW @boy\_\_\_pillow · OCEANE @oceane2u · Entry is exclusively available via the Jaded London app. Download the app to secure your invitation." (links to nothing.tech and DJ Instagrams)
4.  App Store / Google Play image buttons (CDN/apple.jpg, CDN/android.jpg, no alt).

### Campaigns index /en-us/pages/campaigns

  - Heading "CAMPAIGNS", intro "Get a closer look into the world of Jaded through our campaign archive and discover exclusive behind-the-scenes content."
  - Grid of \~130 campaign tiles, newest first: NOLITA, VOL. 1, JADED X NOTHING, VIOLET, LA CASTING CALL, IBIZA, TRESPASS, EYEWEAR, DEVON, AWAY FANS, EUROPA, LOLA, JUDE JEANS, LIVIA FOR SS26, ROCK REVIVAL BY JADED LONDON, LA STORE LAUNCH, ROMIE, KARMEN, HAZE, AMARA, FADE, SPRING, RUINÉ, MVP, SLEAZE, FINALE, ETERNAL, ENSEMBLE, IDOL, CRASH, NEW ROCK FOR JADED AW25, LARRY CLARK, EMBER, REVERB, 6AM, BALLERINA, NEW YORK 25' PARTY, AMETHYST, FAITHLESS, IBIZA, KAIA, BRAZIL, EYEWEAR SS25, SOLARIS, POINT BREAK, BABYMOROCCO FOR JADED LONDON, ALLEGRA, WASTED POTENTIAL, STARDOM, LOVE AFFAIR, ECLIPSE… back to PARACHUTE. Duplicates exist (IBIZA ×2, PURITY ×2, SWIM | OFFSIDE ×2, VOL. 1 and VOL1).

### Editions /en-us/pages/editions

  - Heading "EDITIONS", intro: "Editions is a platform for showcasing the talent and individuality of creatives. Editions acts as a catalyst for their craft, as well as allowing a new perspective on the collection it will be a part of, where in some cases, the project will sit as a standalone collection. Introducing exciting and aligned creatives to our ecosystem is a way of empowering their ideas, giving them a voice and creating a space that acts a spotlight for these designers/creators. Each Edition will have their own space on our site…"
  - Tiles: LARRY CLARK "KIDS" 1995, NEW ROCK FOR JADED '25, SCHOTT FOR JADED '25, JADED X OMIGHTY, KATYA ZELENTSOVA, SPACEBRAT, DIRTYL00KS, ROCK REVIVAL FOR JADED, 2000 ARCHIVES FOR JADED, PAUL FRANK FOR JADED, SLEAZENATION FOR JADED, SCHOTT FOR JADED, NEW ROCK FOR JADED, LA MASKARADE X TIDES, COWBOYS OF HABIT FOR JADED, JADED X PELO ROSSO, PRINCESS PLASTIK, LDN TO NYC - VFILES.

  

Other editorial pages found in the sitemap (not individually inventoried): \~80 \*-campaign pages, curly-fry-x-jaded-man, jaded-ldn-x-sydney-carlson, omighty-x-jaded, paul-frank-for-jaded-london, jaded-london-2000-archives, jaded-london-gentle-monster, babymorocco-for-jadedlondon, larry-clark-campaign, nyc-party-2024/2025, plus test/draft pages that are publicly indexed (london-pop-up-test2, delivery-draft, returns-draft, the-parachute-pant-jaded-london-copy, ss22-tropi-cool-swim-campaign-copy).

  

-----

## 7\. Stores

### Stores (US) /en-us/pages/stores-2026 (footer "Stores")

  - **Title**: "Jaded Retail Stores | LA & USA"; **Meta**: "Shop Jaded in store on Melrose Avenue in Los Angeles and Broadway, New York. Stores open 11am-7pm Monday-Saturday and 12pm-6pm Sunday."
  - Two carousels ("world tour" section): **New York Store**: Opening times Monday to Saturday 11am - 7pm, Sunday 12pm - 6pm, 434 Broadway NY, 10013 (one slide says Mon-Fri 11-7, Sat 11:30am-7:30pm: inconsistent hours). **LA Store**: Mon-Sat 11am-7pm, Sun 12pm-6pm, 8483 Melrose Avenue CA, 90069. Images CDN/TEST\_91eef4bf-….jpg, CDN/Artboard\_5\_….jpg, CDN/Artboard\_2\_….jpg, CDN/Artboard\_3\_….jpg, CDN/Artboard\_10\_….jpg, CDN/josh-cho-photography-jaded-london-los-angeles-1.jpg, -3.jpg.

### New York Store /en-us/pages/new-york-store-2026

  - **Title**: "Jaded London Stores | NYC Broadway"; **Meta**: "Explore our NYC store on Broadway, open 11am-7pm Monday to Saturday and Sunday 12pm-6pm. 434 Broadway, New York, NY, 10013."

<!-- end list -->

1.  Heading "New York Store", image carousel with arrows (**slides render blank on first paint until lazy-loaded**; see stores\_nyc\_carousel\_unloaded.png), then "Opening times: Monday to Saturday: 11am - 7pm, Sunday: 12pm - 6pm" and "Address: 434 Broadway, New York, NY, 10013". Images CDN/TEST\_8c5f49db-….jpg, CDN/Artboard\_5\_aface3da-….jpg, CDN/Artboard\_2\_7d91cb75-….jpg, CDN/Artboard\_3\_174caff7-….jpg. No map, no phone, no directions link.
2.  Video banner "Introducing: The Sound Room / In collaboration with NOTHING" → jaded-x-nothing-nyc (DJ in a mirrored booth, fisheye footage). Same poster/video as the NOTHING page; mobile poster CDN/MOBILEPOSTER.jpg.

### LA Store /en-us/pages/la-store-2026

  - **Title**: "Jaded London Stores | LA Melrose Avenue"; **Meta**: "Explore our LA store on Melrose Avenue, open 11am - 7pm." Same carousel template as NY.

### London

  - **No permanent London store page.** London presence is pop-ups only: "London Pop-up, December 24'", "Jaded London / Selfridges London, November 24'", "London Pop-up, September 23'" on /pages/stores; legacy pages london-pop-up, london-pop-up-24, london-pop-up-2024, jaded-london-selfridges-london.

### Pop-Up Stores /en-us/pages/stores

  - Intro "Jaded London physical stores, pop-up's and IRL experiences." Tiles with "Explore More": ENG Pop-up Chengdu (Dec 2025), Nubian Pop-up Tokyo (Nov 2025), World Tour: Miami Pop Up (May 25), London Pop-up (Dec 24'), Japan Pop-up (Oct 24'), Jaded London x 2000Archives Seoul (Apr 2024), Shanghai Pop-up (Mar 24'), LA Pop-up (Apr 23'), ENG Pop-up Hangzhou (Dec 2025), NYC Store (Sep 2025), World Tour: LA Pop-up (Apr 25), Selfridges London (Nov 24'), NYC Pop-up (Sep 2024), LA Pop-up (Apr 24'), London Pop-up (Sep 23'). Ordering is not chronological.

  

-----

## 8\. Info pages

|  |  |  |
| :-: | :-: | :-: |
| \*\*Page\*\* | \*\*Title\*\* | \*\*Key copy / notes\*\* |
| Contact /pages/contact-us | Contact Jaded London | Left sidebar of help links (Delivery, returns, contact us, Gift Cards, Student Discount, Jobs, Klarna, Terms, Privacy, Cookies, CSR, Refund policy, Size Guide, faqs; several point to non-localised or old URLs like /pages/jobs, /pages/klarna). Copy: "Got a question you can't find an answer too \\\[sic\\\] or need a little extra help with your order? Have you checked out our FAQs section… Please note, sending a second message before receiving a reply from us will result in longer response times. Our customer care team are here Monday - Friday 10am - 5pm (excluding bank holidays) and aim to respond to all enquiries within 48 hours. To help us answer you as quickly as possible, please always include your Order Number…" (UK hours, no US time zone stated). |
| Delivery /pages/delivery-info | Delivery-Information | "DELIVERY. Please track your order on our tracking page. We are also unable to deliver to freight forwarded or PO Box addresses. We kindly recommend selecting a secure, permanent delivery address… Temporary locations such as hotels or Airbnb accommodations can present access and timing challenges… delivery cannot be guaranteed…" Accordions: UK MAINLAND, USA, INTERNATIONAL, TAXES & DUTIES, WHERE IS MY ORDER? (UK listed first on US store). |
| Returns /pages/returns-info | Returns-info | 30-day refund policy (as PDP), plus "Gift cards are also not eligible for refunds. We do not accept combined returns… We no longer offer exchanges, any returned items will be refunded instead. Please note: Items purchased online cannot be returned in-store." Links for UK / EU / US returns; accordions UK RETURNS, USA RETURNS, EU RETURNS, CANADA RETURNS, INTERNATIONAL RETURNS, RECEIVED THE WRONG ITEM?, REFUNDS, LATE OR MISSING REFUNDS, CONCESSIONS AND THIRD PARTY RETAILERS. |
| FAQ | (external) | https://faq.jadedldn.com/ (separate help-centre subdomain, likely Gorgias Help Center). Legacy faqs-\\\* pages also exist. |
| Size Guide /pages/jaded-london-size-guide | Jaded London Size Guide | Same component as PDP modal: Women/Men/Unisex tabs, CM/IN, category tabs, UK→US/EU/IT/AU conversion, inside-leg Regular 85cm / Petite 79cm. "All womens clothing is in UK sizing" (US store still sells in UK sizes). |
| Student discount /pages/students-discount-global-links | Students Beans by Market \\\[sic\\\] | List of 20 markets (UK, USA, Germany, Australia, Ireland, Canada, Austria, Switzerland, Netherlands, Belgium, Spain, Finland, Denmark, Poland, Sweden, Norway, Japan, Hong Kong, New Zealand, France) linking to non-localised Student Beans pages. UNiDAYS in footer. |
| Community Rewards /pages/community-rewards | Community Rewards | LoyaltyLion programme: "Community Rewards. Get access to exclusive rewards and early product launches with our community rewards programme." LOGIN / SIGN UP; 1. SIGN UP 2. START SHOPPING 3. EARN REWARDS; perks: welcome discount, 5 points per £/$/€ spent, cash reward, secret promo codes, first access to collections and sale, free standard delivery, digital access to all parties, pop up shop queue jump; Tiers One 0-1249, Two 1,250-1,749, Three 1,750-2,499, Four 2500+; Refer a friend (friend gets 10% off, you get 100 points); +20 points each for joining, TikTok follow, Instagram follow, newsletter. GIF icons CDN/1.gif, CDN/Untitled-2.gif, CDN/3.gif. "REFER" button links to \\\#. |
| Careers /pages/careers-jadedlondon | Careers \| Jaded London | Meta: "We're always on the lookout for new talent…" Plain list of 17 roles (Logistics Coordinator, Creative and Social Co-ordinator - Jaded Man, Senior Womenswear Designer, Retail Operations Manager, Director of Retail, Senior Creative Producer, Production & Compliance Admin Assistant, Creative Content & Styling Coordinator, Wholesale Account Assistant, Sample & Showroom Coordinator, Head of Influencer Marketing, New Store Retail Operations Manager - Miami, Senior Menswear Designer, Sales Associate - New York, Freelance - Brand Activations & Pop-ups Project Manager, Paid Social Executive, Customer Care Assistant). |
| CSR /pages/corporate-social-responsibility | Corporate Social Responsibility \| Jaded London | Sections: People / Modeling for Jaded London (agency-only models, paid shoots), Social Media Collaborations (gifting tiers based on followers/engagement), Hiring (equal opportunities). Lowercase sentence starts. This is the closest thing to a sustainability page; none exists. |
| 10% off /pages/10-off-your-first-order | 10% Off Your First Order | "Sign up for 10% off your first order. Join our community for early access to new collections, exclusive offers, and curated content made just for you." + Subscribe; video hero CDN/DESK\\\_POSTER\\\_2.jpg, VID/64d24dcc889445c3abb9925408a7ce8a.mp4. |
| About / Our Story | n/a | \*\*No About page\*\* (/pages/about-us returns 404). |
| Affiliates / Ambassadors | n/a | \*\*No page\*\* (/pages/affiliates 404). Affiliate tracking runs through Awin (script present). |
| App | /pages/download-the-jaded-london-app | Linked from footer (non-localised). |

  

-----

## 9\. Search ("parachute")

  - Search icon opens a full-width overlay below the header with a single input ("Search…") and close X; page dims behind.
  - Typing shows instant results: "**1000 results**" with "View all" link, then a 4-up product grid with wishlist hearts (first: Black Parachute Cargo Pants $130, 8 colours; then khaki/camo, navy and olive parachute styles).
  - The result count looks capped/loose (catalog has \~30 parachute styles).
  - **Bug**: raw CSS and inline JavaScript (with developer comments written in Gujarati) render as text inside the results container's DOM (a.product-option-plus-button {…}, document.addEventListener('DOMContentLoaded'…). Visible to screen readers/text extraction; worth checking visually on slower loads.
  - No suggested queries, categories or recent searches shown.

## 10\. Cart (empty)

  - Clicking the bag icon with an empty bag does **not** open a drawer; it goes to /en-us/cart.
  - Page copy: "Your bag is empty" + black button "Shop our products". Below: "Recently viewed" carousel (showed Washed Black XL Parachute Cargo Pants $170). No upsells, no free-shipping progress bar, no trust copy in the empty state.

  

-----

## PART D: Technical notes

### Platform and theme

  - Shopify. Shopify.theme.name = "jaded-london/Shearing-Boots-Launch-jaded-london…" (theme published straight from a launch branch), schema\_name "Jaded London" v1.0.0 (custom theme). Class names (ProductItem\_\_Wrapper, Popover) indicate it was forked from Maestrooo's **Prestige** theme.
  - **Shogun** page builder used for PLP wrappers and all legacy editorial/landing pages (shogun-above/below, i.shgcdn.com images).
  - Images served via assets.jadedldn.com (Cloudinary-style transform proxy, e\_sharpen:70,w\_1600) and Shopify CDN.

### Apps / third parties identified (from script hosts and markup)

|  |  |
| :-: | :-: |
| \*\*Purpose\*\* | \*\*Vendor\*\* |
| Cross-border / currency / duties | Global-e |
| Reviews | Judge.me |
| BNPL | Klarna, Afterpay (placements present) |
| Wishlist | Swym (swymv3pro) |
| Loyalty | LoyaltyLion |
| Chat / helpdesk / FAQ | Gorgias (chat + help centre) |
| Email / CRM | Ometria |
| SMS | Attentive (cdn.attn.tv) |
| A/B and price testing | Intelligems |
| Size recommendation | uSizy |
| Accessibility overlay | EqualWeb |
| Fraud | Forter |
| Error/session monitoring | Noibu, Microsoft Clarity |
| Speed layer | RenderBetter (accel.renderbetter.com) |
| Mobile app | Venn Apps |
| Student | Student Beans, UNiDAYS |
| Affiliate | Awin (dwin1.com) |
| Merchandising / banners | Hextom |
| Page builder | Shogun |
| Ads/analytics | GTM, Google Ads, Meta pixel, TikTok pixel, Snapchat pixel, Shop app |
| Misc | jQuery from code.jquery.com, jsDelivr libraries, media/content.9gtb.com, lantern.roeyecdn.com, two first-party proxied hosts (dicsr., jnecc.jadedldn.com) |

  

Roughly 40 third-party script hosts on a PDP: a major performance and maintenance cost.

### Load feel

  - Homepage hero appears quickly (single image), but the announcement bar ticker and header shift slightly on load.
  - Shogun pages (Parachute, LDN to NYC) paint a large empty white area before content.
  - NYC store carousel renders blank until lazy-load fires.
  - Collab/NOTHING pages autoplay heavy videos (NOTHING served as .mov).
  - Every PDP ships the entire multi-category size guide markup inline.

### Accessibility

  - Banner, hero and campaign images consistently have **empty alt text**; product card images do have alts.
  - App badge images (apple.jpg, android.jpg) have no alt.
  - Hero text links ("Menswear"/"Womenswear") are mid-grey on a light photo: low contrast.
  - Footer legal links \~11px grey.
  - Icon-only header buttons: search, wishlist and bag have labels; hamburger button has no accessible name.
  - EqualWeb overlay used instead of native fixes.
  - Keyboard focus not formally tested (no keyboard-only pass done).

### Broken / inconsistent / off-brand

1.  GBP prices (£65) on US Parachute gender pages; mens page cards missing product names.
2.  Sale collection titles/metas say "Summer Sale 2026" in October.
3.  Rock Revival page still advertising April early-access dates with no shop CTA; Swim landing still summer-led.
4.  Compare-at price equals price on many products (Vivienne dress, Idol bikini) – risk of fake "sale" display.
5.  Colour data mismatch (Heart jeans "Black" vs tag colour\_blue); size filter duplicates (UK16 vs UK 16, ONE SIZE vs One Size); gender filter dirty values.
6.  Unisex styles duplicated as separate men's and women's products (-ww suffix), splitting reviews/stock and SEO.
7.  Men's styles appearing in Women's New In (Black Drummer Hoodie).
8.  Many links not localised to /en-us (Sleazenation products, contact sidebar, student links, app page), bouncing users to the default market.
9.  "Shop Denim" banner goes to a fit guide, not a collection.
10. Test/draft pages publicly in the sitemap; "test" and "Untitled" filenames in production assets; theme published from a branch-named theme.
11. Copy typos: "answer too", "Kylier Jenner", "virtual cargo trend", "bought a strong sense", "huge arrange", "Students Beans", "pop-up's".
12. Inconsistent NY store hours across carousel slides.
13. No About/Our Story, no Sustainability, no Affiliates page; no permanent London store page despite "London" being the brand name.
14. Footer EU Right to Withdrawal shown on US store; UK customer-care hours with no US time zone.
15. "Only 143 items in stock\!" scarcity message triggers at high stock.
16. Raw CSS/JS (Gujarati dev comments) inside search results markup.
17. Homepage has no product, no brand statement and no campaign storytelling: one image and two links.

  

-----

## PART E: Social presence

### Instagram @jadedldn (viewed logged-out; login modal dismissed)

  - Verified. **1.5M followers**, 1,261 following.
  - Bio: "JADED LONDON / @jaded\_swim / SHEARLING BOOTS - available now / jadedldn.com/collections/shearling-boots and 4 more".
  - Highlights: NOLITA, SHEARLING BOOT, PRESS.
  - Related accounts IG suggests: Rat & Boa, Jaded Swim, Archived Runway, Omighty, I.AM.GIA, Meshki, Peppermayo, Vivienne Westwood, Guizio, tourist souvenirs, Maison Margiela.
  - Most recent \~11 grid posts (all carousels): (1) pink-haired model in a pink lace-up corset and grey flares leaning on a hot-pink car with "MO…" branding (Nolita / NOTHING-adjacent nightlife look); (2) the shearling campaign duo on white (grey hoodie/coat with black backless lace dress and studded black boots); (3) model crouched against a white wall in a black corset with camo studded shearling boots; (4) close-up of pink studded shearling boots on pavement; (5) black ribbed and studded shearling boots, studio crop; (6) NYC street style: curly-haired model in big sunglasses, faux-fur collared leather bomber and blue jeans on a SoHo corner; (7) model in a zebra faux-fur coat and heels in an SUV with the Brooklyn Bridge/Manhattan skyline; (8) platinum-blonde model in oversized sunglasses and a tiger-stripe faux-fur coat; (9) model with an umbrella in a grey military-button mini coat-dress crossing a rainy street; (10-11) further fur/NYC street content.
  - **Vibe**: 2000s Y2K-meets-indie-sleaze, NYC street and paparazzi-style flash, studio on white seamless for product drops. Palette: black, greys, denim, fur browns, with hits of hot pink and camo. Typography almost absent on grid (image-led, no text overlays).

### TikTok @jadedldn (viewed while the browser was signed in to TikTok; nothing interacted with)

  - Verified. **423.4K followers**, 1,560 following, **5.6M likes**.
  - Bio: "SHEARLING BOOTS - now live"; links: jadedldn.com/collections/new-in-womens and the App Store app.
  - Latest videos (views): pinned pink studded boot UGC reply "what are these boots?\!" (28.4K), pinned NYC street walk (161K), pinned The Sound Room mirrored pod (91.4K), older-couple shearling content (12.9K), aerial/hammock stunt (7,640), camo studded boot close-up (56.8K), toddler in oversized knit and shearling boots (25.9K), "turning my grandma into me" styling transformation (13.8K), couple in a NYC alley (11.5K), zebra fur coat in a helicopter (11.7K) and stepping out of a helicopter (11.4K), purple joggers street walk (17.6K), "Rated R recruits only" military bomber (11.4K), studded leather chair shoot (11.4K), NYC crosswalk pose (43.8K), purple corset in rain (13.1K), sequin flower halter detail (12.4K), male models carrying women in a warehouse (13.1K).
  - **Recurring themes**: NYC (store, streets, helicopters), shearling boots launch, UGC-style replies, family/age-gap humour (grandma, toddler), nightlife, fur, studs, military detailing. Text overlays in TikTok's native font, lowercase, meme tone.

### Brand "is / is not" (from site + social)

  - **Is**: London-born but NYC-forward; Y2K/indie-sleaze; studs, fur, lace, camo, baggy denim; flash photography and street casting; collabs with subculture heritage (Sleazenation, Larry Clark, Rock Revival, New Rock, VFILES); IRL events, pop-ups and app-gated access; humour and UGC on TikTok.
  - **Is not**: minimal luxury, polished e-commerce storytelling (the site is far plainer than the socials), sustainability-led, or overtly British-heritage in the US experience.

  

-----

## Mobile notes (Part B/C)

The browser window could not be resized below desktop width from this session, and the site blocks being framed, so mobile screenshots were not captured. From markup: separate mobile crops exist for every banner (MOB\_\* assets), the same hamburger drawer is used, PLP filter/sort are a sticky bottom bar, and the PDP collapses to a single column with the same accordions.