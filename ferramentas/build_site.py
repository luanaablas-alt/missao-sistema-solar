"""Gera a pasta site/ (o que a Vercel publica) a partir do jogo em jogo/index.html.

Uso, na raiz do repositório:  python3 ferramentas/build_site.py

- troca as fontes e a biblioteca 3D que vinham de outros sites por arquivos próprios (site/fonts, site/vendor);
- liga o app instalável (manifesto, ícones e o service worker que guarda o jogo para funcionar sem internet);
- gera a política de privacidade e os termos a partir dos textos em ferramentas/.
"""
import os,re,json,shutil,hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'jogo','index.html');OUT=os.path.join(ROOT,'site');TOOLS=os.path.join(ROOT,'ferramentas')
s=open(SRC,encoding='utf-8').read()
def rep(x,y,n=1):
    global s
    assert s.count(x)==n,(x[:90],s.count(x));s=s.replace(x,y)
rep('''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Fredoka:wght@500;600;700&display=swap" rel="stylesheet">''',
'''<meta name="description" content="Jogo educativo de espaço para crianças de 6 a 8 anos: planetas de verdade, leitura, números e um universo para construir.">
<meta name="theme-color" content="#060a1a">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<style>
@font-face{font-family:"Fredoka";font-weight:500;font-display:swap;src:url(/fonts/fredoka-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Fredoka";font-weight:600;font-display:swap;src:url(/fonts/fredoka-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Fredoka";font-weight:700;font-display:swap;src:url(/fonts/fredoka-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Atkinson Hyperlegible";font-weight:400;font-display:swap;src:url(/fonts/atkinson-hyperlegible-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Atkinson Hyperlegible";font-weight:700;font-display:swap;src:url(/fonts/atkinson-hyperlegible-latin-700-normal.woff2) format("woff2")}
</style>''')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="/vendor/three-r128.min.js"></script>')
rep('var LEGAL=null;','var LEGAL={priv:"/privacidade",termos:"/termos"};')
# conta da família e assinatura: endereço do Supabase, chave pública e link de compra da Kiwify (ferramentas/conta.json)
CONTA=json.load(open(os.path.join(TOOLS,'conta.json'),encoding='utf-8'))
rep('var CONTA=null;','var CONTA='+json.dumps(CONTA)+';')
vj=os.path.join(OUT,'vercel.json');v=open(vj,encoding='utf-8').read()
v=re.sub(r"connect-src 'self'[^;]*;","connect-src 'self' "+CONTA['url']+";",v)
open(vj,'w',encoding='utf-8').write(v)
s=s.replace('src="tex/','src="/tex/').replace("url(tex/","url(/tex/").replace('"tex/"+','"/tex/"+')
rep('</body>','''<script>
if("serviceWorker" in navigator&&location.protocol==="https:"){window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){});});}
</script>
</body>''')
for bad in ('googleapis','gstatic','cdnjs','jsdelivr','unpkg'):
    assert bad not in s,bad
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(s)
# imagens dos planetas
if os.path.isdir(os.path.join(OUT,'tex')):shutil.rmtree(os.path.join(OUT,'tex'))
shutil.copytree(os.path.join(ROOT,'jogo','tex'),os.path.join(OUT,'tex'))
# política de privacidade e termos de uso
base=open(os.path.join(TOOLS,'legal_base.html'),encoding='utf-8').read()
for name,title in [('privacidade','Política de privacidade'),('termos','Termos de uso')]:
    body=open(os.path.join(TOOLS,name+'.body.html'),encoding='utf-8').read()
    open(os.path.join(OUT,name+'.html'),'w',encoding='utf-8').write(base.replace('__TITLE__',title).replace('__BODY__',body))
# service worker: lista do que fica guardado no aparelho, com versão nova a cada mudança
files=['/','/index.html','/privacidade','/termos','/manifest.webmanifest','/vendor/three-r128.min.js']
for d in ['fonts','tex','icons']:
    for f in sorted(os.listdir(os.path.join(OUT,d))):
        if not f.endswith('.txt'):files.append('/'+d+'/'+f)
h=hashlib.sha1()
for f in files[1:]:
    p=os.path.join(OUT,(f.strip('/')+('.html' if f in ('/privacidade','/termos') else '')))
    h.update(open(p,'rb').read())
ver=h.hexdigest()[:10]
sw=open(os.path.join(TOOLS,'sw.template.js'),encoding='utf-8').read().replace('__VERSION__',ver).replace('__FILES__',json.dumps(files))
open(os.path.join(OUT,'sw.js'),'w',encoding='utf-8').write(sw)
print('site/ pronto · versão',ver,'·',len(files),'arquivos guardados para uso sem internet')
