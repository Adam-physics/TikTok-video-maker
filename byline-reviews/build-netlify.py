# Builds netlify-build/ and byline-reviews-netlify.zip from index-academy.html
import shutil, os, zipfile
h=open('index-academy.html').read().replace('<meta name="claude:viewport-fit-sides" content="cover">\n','').replace('<meta charset="utf-8">\n','',1)
i=h.index('</style>')+len('</style>')
fav="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%232D46F5'/%3E%3Ctext x='16' y='23' font-family='Arial' font-weight='800' font-size='20' fill='white' text-anchor='middle'%3EB%3C/text%3E%3C/svg%3E"
pre=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
 f'<link rel="icon" href="{fav}">\n<meta property="og:title" content="Byline">\n'
 '<meta property="og:description" content="Real Amazon reviews for your book, from real readers. Up to 1,500 reviews, count guaranteed.">\n'
 '<meta property="og:type" content="website">\n')
shutil.rmtree('netlify-build',ignore_errors=True); os.makedirs('netlify-build')
open('netlify-build/index.html','w').write(pre+h[:i]+'\n</head>\n<body>'+h[i:].rstrip()+'\n</body>\n</html>\n')
covers=['cover-terminal.webp','cover-reality.webp','cover-transcendent.webp','cover-trivia.webp']
for c in covers: shutil.copy(c,'netlify-build/'+c)
with zipfile.ZipFile('byline-reviews-netlify.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in ['index.html']+covers: z.write('netlify-build/'+f,f)
print('built')
