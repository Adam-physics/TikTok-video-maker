import json,glob,collections,re,statistics,sys
d=sys.argv[1]
P=[]; [P.extend(json.load(open(f))['products']) for f in sorted(glob.glob(d+'/products_p*.json'))]
C=[]; [C.extend(json.load(open(f))['collections']) for f in sorted(glob.glob(d+'/collections_p*.json'))]
G=[]; [G.extend(json.load(open(f))['pages']) for f in sorted(glob.glob(d+'/pages_p*.json'))]
print('products',len(P),'collections',len(C),'pages',len(G))
cnt=collections.Counter
print('vendor',cnt(p['vendor'] for p in P).most_common())
print('types',cnt(p['product_type'] for p in P).most_common(40))
prices=[float(v['price']) for p in P for v in p['variants']]
pmin=[min(float(v['price']) for v in p['variants']) for p in P]
print('price min/median/max', min(pmin), statistics.median(pmin), max(pmin))
sale=[p for p in P if any(v.get('compare_at_price') and float(v['compare_at_price'])>float(v['price']) for v in p['variants'])]
print('on sale',len(sale))
avail=[p for p in P if any(v['available'] for v in p['variants'])]
print('in stock (any variant)',len(avail))
imgs=[i for p in P for i in p['images']]
print('images',len(imgs),'per product median',statistics.median(len(p['images']) for p in P))
print('img widths',statistics.median(i['width'] for i in imgs if i.get('width')), max(i['width'] for i in imgs if i.get('width')))
noalt=0
print('variants',sum(len(p['variants']) for p in P))
print('options',cnt(o['name'] for p in P for o in p['options']).most_common(10))
sizes=cnt(v for p in P for o in p['options'] if o['name'].lower()=='size' for v in o['values'])
print('sizes',sizes.most_common(30))
by_type=collections.defaultdict(list)
for p in P: by_type[p['product_type']].append(min(float(v['price']) for v in p['variants']))
for t,l in sorted(by_type.items(),key=lambda x:-len(x[1]))[:25]: print(f'  {t}: n={len(l)} £{min(l):.0f}-£{max(l):.0f} med £{statistics.median(l):.0f}')
pub=cnt(p['published_at'][:4] for p in P); print('published yr',sorted(pub.items()))
print('created yr',sorted(cnt(p['created_at'][:4] for p in P).items()))
tags=cnt(t for p in P for t in p['tags'])
print('tags uniq',len(tags)); print([t for t,_ in tags.most_common(80)])
para=[p for p in P if 'parachute' in p['title'].lower()]
print('parachute',len(para),[ (p['title'],p['variants'][0]['price']) for p in para[:40]])
dup=cnt(p['title'] for p in P); print('dup titles',sum(1 for t,c in dup.items() if c>1), [t for t,c in dup.most_common(8)])
# collections
print('coll with images',sum(1 for c in C if c.get('image')))
print('coll products_count stats: empty',sum(1 for c in C if c.get('products_count',1)==0))
print('coll handles sample',[c['handle'] for c in C[:60]])
# body html quality
bh=[len(re.sub('<[^>]+>','',p['body_html'] or '')) for p in P]; print('desc chars median',statistics.median(bh),'empty',sum(1 for b in bh if b<20))
inline=sum(1 for p in P if 'style=' in (p['body_html'] or '')); print('desc with inline styles',inline)
sc=sum(1 for p in P if 'Style code' in (p['body_html'] or '')); print('style code in desc',sc)
model=sum(1 for p in P if re.search('Model is',p['body_html'] or '')); print('model info',model)
# pages
print('pages empty',sum(1 for g in G if len(g.get('body_html') or '')<50))
apps=cnt()
for g in G:
  h=g.get('body_html') or ''
  for k in ['klaviyo','typeform','youtube','vimeo','instagram','tiktok','script','iframe','mp4','gif','google','hubspot','mailchimp','attentive','postscript','yotpo','okendo','gorgias','zendesk','tolstoy','foursixty','dash hudson','later','flowbox','swiper','slick','jquery']:
    if k in h.lower(): apps[k]+=1
print('page embeds',apps.most_common())
test=[g['handle'] for g in G if re.search(r'test|copy|draft',g['handle'])]; print('test/copy pages',len(test),test)
signup=[g['handle'] for g in G if 'sign' in g['handle']]; print('signup pages',len(signup))
camp=[g['handle'] for g in G if 'campaign' in g['handle'] or 'lookbook' in g['handle']]; print('campaign pages',len(camp))
print('page yrs',sorted(cnt(g['updated_at'][:4] for g in G).items()))
print('ALL PAGES:'); print(' '.join(g['handle'] for g in G))
