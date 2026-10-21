import json,glob,re,sys,csv,collections,html
d=sys.argv[1]; out=sys.argv[2]
def load(pat,key):
  L=[]; [L.extend(json.load(open(f))[key]) for f in sorted(glob.glob(d+pat))]; return L
P=load('/products_p*.json','products'); C=load('/collections_p*.json','collections'); G=load('/pages_p*.json','pages')
rows=[]
by={g['handle']:g for g in G}
CAMP=set(re.findall(r'/pages/([a-z0-9-]+)',by['campaigns']['body_html']))
DROP={'womens','mens','unisex','swim','summer','sunglasses','mens-1','womens-black-friday','sale-download-the-app','shearling-boots-download-app','download-the-jaded-london-app','violet-app-page','mens-denim-app','womens-denim-app','jaded-london-denim','jaded-london-denim-unisex','unisex-spring','jaded-london-neutrals','jaded-man-neutrals','instagram-shop','launches-womens'}
def add(kind,old,new,action,cat,note=''): rows.append(dict(type=kind,old_url=old,new_url=new,action=action,category=cat,note=note))
def txtlen(h): return len(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',h or ''))).strip())
POL={'privacy-policy':'/policies/privacy-policy','refund-policy':'/policies/refund-policy','terms-of-use':'/policies/terms-of-service','cookies-policy':'/policies/privacy-policy#cookies'}
STORE=re.compile(r'(pop-?up|store|selfridges|nubian|chengdu|hangzhou|shanghai|tokyo|paris|lapopup|ldnpopup|nolita-save|pfw23|takes-paris|takesparis)')
JOB=re.compile(r'(manager|designer|coordinator|assistant|advisor|executive|recruiter|officer|careers|office-manager|talent-|pa$)')
for g in G:
  h=g['handle']; o='/pages/'+h; n=txtlen(g.get('body_html'))
  if re.search(r'(^test$|-test|test\d|-copy|draft|accordion|^bf-test|files-old)',h): add('page',o,'(delete)','delete+301 to parent','junk','test/copy/draft page')
  elif h in POL: add('page',o,POL[h],'301','policy')
  elif 'sign-up' in h or h.endswith('signup') or 'first-access' in h or h in ('thank-you-for-subscribing','sign-up-to-newsletter'):
    base=re.sub(r'-?(app-)?(sign-up|first-access|collection-sign-up|sign-up-page)(-page)?(-jaded-app|-copy)?$','',h).strip('-') or 'newsletter'
    add('page',o,f'/pages/drops/{base}' if base not in ('newsletter','sign-up-to-newsletter','thank-you-for-subscribing') else '/pages/club','301','drop waitlist','merge into drop page waitlist module')
  elif h.startswith('student') : add('page',o,'/pages/student-discount','301 (country auto-detect)','student discount')
  elif JOB.search(h) and 'campaign' not in h: add('page',o,'/pages/careers' if 'careers' in h else f'/pages/careers#{h}','301','careers','move role to ATS/careers metaobject')
  elif h.startswith('faqs') or h in ('delivery-info','returns-info','exchanges','order-tracking','track-your-order','where-is-my-order','taxes-duties','international','uk-mainland','klarna','contact-us','hotline') or h.startswith('returns-'):
    add('page',o,'/pages/help/'+re.sub(r'^faqs-','',h),'301','help centre')
  elif 'size' in h or 'fit-guide' in h: add('page',o,'/pages/help/size-and-fit','301','size guide','also inline on PDP')
  elif h in ('search-results','search-results-1','search-results-page','rapid-search-results'): add('page',o,'/search','301','search')
  elif 'wishlist' in h or h=='share-cart': add('page',o,'/account/wishlist','301','account')
  elif STORE.search(h): add('page',o,'/pages/stores/'+h,'301','stores / IRL')
  elif h in ('the-parachute-pant-jaded-london','the-parachute-pants','the-parachute-pants-mens','the-parachute-pants-womens'): add('page',o,'/pages/parachute','301 (mens/womens become tabs)','hero franchise')
  elif re.search(r'(for-jaded|x-jaded|jaded-x|-x-|collab|editions|rockrevival|omighty|paul-frank|schott|sleaze|2000|2kjaded|gentle-monster|new-rock|cowboys|babymorocco|curly|dirtyl00ks|sydney|cold-feet|nothing)',h):
    add('page',o,'/pages/collabs/'+h,'301','collab')
  elif h in DROP: add('page',o,'(merge)','301 to matching collection / app deep link','landing duplicate of collection')
  elif h in CAMP or re.search(r'(campaign|^campaigns$|lookbook)',h) or n>1500: add('page',o,'/pages/campaigns/'+re.sub(r'-?campaign-?','',h).strip('-') if h!='campaigns' else '/pages/campaigns','301','campaign / editorial')
  elif n<50: add('page',o,'(review)','theme-section page or empty: confirm in admin','empty body','body_html empty; content probably lives in theme sections/Shogun')
  else: add('page',o,o,'keep','misc')
for c in C:
  h=c['handle']; o='/collections/'+h
  if re.match(r'^\d{1,2}-\d{1,2}-\d{2}|^\d+(st|nd|rd|th)-',h) or 'reshoot' in h: add('collection',o,'(unpublish)','hide from Online Store; 301 to /collections/new-in','internal ops (dated drop/reshoot)')
  elif 'sale' in h: add('collection',o,'/collections/sale'+('-men' if 'men' in h and 'women' not in h else ''),'301 unless current season','sale')
  elif h.endswith('-app') or '-app-' in h or h.startswith('app-'): add('collection',o,o,'keep, noindex','app-only')
  elif 'influencer' in h or 'rail-edit' in h: add('collection',o,'/collections/edit-'+re.sub(r'-?(rail-edit|influencer)-?','',h),'301','creator edit')
  elif 'black-friday' in h or 'bfcm' in h: add('collection',o,'/collections/sale','301','seasonal promo')
  elif (c.get('products_count') or 0)==0: add('collection',o,'(review)','empty: 301 to parent category','empty')
  else: add('collection',o,o,'keep (canonical)','merchandising')
for p in P:
  add('product','/products/'+p['handle'],'/products/'+p['handle'],'keep (URLs unchanged on OS 2.0)','product',p['vendor'])
with open(out,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
s=collections.Counter((r['type'],r['category']) for r in rows)
for k,v in sorted(s.items()): print(k,v)
