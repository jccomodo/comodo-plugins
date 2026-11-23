# Validador automático das animações HTML da Cômodo (estilo D / qualquer HTML com window.render(t) e window.READY=1).
# Varre o vídeo no tempo e mede no DOM renderizado:
#   OCULTO    texto/ícone coberto por outro elemento (linha/borda passando por cima de ícone, pílula atrás de contorno...)
#   TACHADO   risco que não passa no meio das letras
#   APERTADO  texto encostando na borda do card/pílula que o contém (ou vazando)
#   MARGEM    conteúdo fora da zona segura (orgânico x90-990 | ads Reels x64-1016,y300-1162 e faixa até 1265 só com x<=923)
#   BORDA     elemento cortado pela borda da tela (zoom/pan)
#   MASCARA   texto/ícone meio escondido pela máscara do título ou da legenda
#   LEGENDA   conteúdo encostando/cobrindo a legenda
#   LOOP      primeiro quadro diferente do último (só orgânico)
# Ignora de propósito: cursor, elementos com data-val-ignore, fundos de tela cheia, contornos vazados (só a borda conta).
# Uso: python valida_html.py <arquivo.html> [--modo organico|ads] [--passo 0.2] [--saida <pasta>] [--loop auto|sim|nao] [--dur s]
import os,sys,json,argparse,re,math
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageChops,ImageFont

ap=argparse.ArgumentParser()
ap.add_argument('html');ap.add_argument('--modo',default='organico',choices=['organico','ads'])
ap.add_argument('--passo',type=float,default=0.2);ap.add_argument('--saida',default=None)
ap.add_argument('--loop',default='auto',choices=['auto','sim','nao']);ap.add_argument('--dur',type=float,default=None)
A=ap.parse_args()
HTML=os.path.abspath(A.html);PASTA=os.path.dirname(HTML)
OUT=A.saida or os.path.join(PASTA,'val');os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT):
    if f.startswith(('ev_','folha_')):os.remove(os.path.join(OUT,f))
src=open(HTML,encoding='utf-8').read()
m=re.search(r'const NF=(\d+)',src)
DUR=A.dur or ((int(m.group(1))-1)/30 if m else None)
if DUR is None: sys.exit('sem NF no html: passe --dur')
chrome = next(iter([os.path.join(r,f) for r,_,fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f=="chrome.exe"]), None)  # Chrome do puppeteer, se houver; senão o Chromium do Playwright
ZONA={'organico':dict(x0=90,x1=990),'ads':dict(x0=64,x1=1016,y0=300,y1=1162,y2=1265,x2=923)}[A.modo]

JS=r"""
(Z)=>{
const ROOT=document.getElementById('p')||document.body;const W=1080,H=1920;const TR='rgba(0, 0, 0, 0)';
const SH=new Set(['path','circle','rect','ellipse','polygon','polyline','line','text']);
function opac(e){let o=1;for(let n=e;n&&n!==document.documentElement;n=n.parentElement){const cs=getComputedStyle(n);if(cs.display==='none'||cs.visibility==='hidden')return 0;o*=parseFloat(cs.opacity)}return o}
function ign(e){return !!(e.closest&&e.closest('[data-val-ignore]'))||isCursor(e)}
function isCursor(e){const s=e.closest&&e.closest('svg');if(!s)return false;const r=s.getBoundingClientRect();if(r.width>90||r.height>90)return false;const p=s.querySelector('path');return !!(p&&/^M0 0 L0 46/.test(p.getAttribute('d')||''))}
function ownText(e){for(const c of e.childNodes)if(c.nodeType===3&&c.textContent.trim())return true;return false}
function bgOf(cs){return (cs.backgroundColor&&cs.backgroundColor!==TR)||(cs.backgroundImage&&cs.backgroundImage!=='none')}
function borderOnly(e){if(e.namespaceURI==='http://www.w3.org/2000/svg')return false;const cs=getComputedStyle(e);return !bgOf(cs)&&parseFloat(cs.borderTopWidth)>0&&!ownText(e)}
function paints(e){const tg=e.tagName.toLowerCase();if(tg==='img'||tg==='canvas')return true;if(SH.has(tg)){const cs=getComputedStyle(e);return cs.fill!=='none'||cs.stroke!=='none'}
 if(tg==='svg')return false;if(e.namespaceURI==='http://www.w3.org/2000/svg')return false;const cs=getComputedStyle(e);
 if(bgOf(cs))return true;if(parseFloat(cs.borderTopWidth)>0&&cs.borderTopColor!==TR)return true;return ownText(e)}
function textRects(e){const rs=[];for(const c of e.childNodes)if(c.nodeType===3&&c.textContent.trim()){const r=document.createRange();r.selectNodeContents(c);for(const q of r.getClientRects())if(q.width>1&&q.height>1)rs.push(q)}return rs}
function U(rs){let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;for(const r of rs){x0=Math.min(x0,r.left);y0=Math.min(y0,r.top);x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom)}return {left:x0,top:y0,right:x1,bottom:y1,width:x1-x0,height:y1-y0}}
function sig(e){const t=(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,40);if(t)return t;const tg=e.tagName.toLowerCase();if(tg==='img')return 'img:'+(e.getAttribute('src')||'');
 const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return tg+(bgOf(cs)?'['+cs.backgroundColor+']':'')+'@'+Math.round(r.left/40)*40+','+Math.round(r.top/40)*40+' '+Math.round(r.width)+'x'+Math.round(r.height)}
const stage=ROOT.firstElementChild;
const masks=[...ROOT.querySelectorAll('.mask')].filter(m=>opac(m)>0.5).map(m=>m.getBoundingClientRect());
let winTop=0,winBot=H;for(const r of masks){if(r.top<5)winTop=Math.max(winTop,r.bottom*0.93);else winBot=Math.min(winBot,r.top+8)}
const overlays=[...ROOT.children].filter(e=>e!==stage&&!e.classList.contains('mask'));
let leg=null;for(const e of overlays){const rs=textRects(e);if(!rs.length||opac(e)<0.3)continue;const u=U(rs);if(!leg||u.top>leg.top)leg=Object.assign(u,{el:e})}
const out=[];const all=[...stage.querySelectorAll('*')];let KD='bloco';
// unidades verificadas: elementos com texto próprio, imagens, divs pintadas pequenas e SVGs (pela união dos traços)
for(const e of all){
 if(ign(e))continue;const tg=e.tagName.toLowerCase();const isSvg=tg==='svg';
 if(!isSvg&&!paints(e))continue;if(e.namespaceURI==='http://www.w3.org/2000/svg'&&!isSvg)continue;
 const o=opac(e);if(o<0.35)continue;
 let r;if(isSvg){const sh=[...e.querySelectorAll('path,circle,rect,ellipse,polygon,polyline,line,text')].map(s=>s.getBoundingClientRect()).filter(q=>q.width>0||q.height>0);if(!sh.length)continue;r=U(sh.map(q=>({left:q.left,top:q.top,right:q.right,bottom:q.bottom})))}
 else r=e.getBoundingClientRect();
 if(r.width<4||r.height<4)continue;if(r.right<0||r.left>W||r.bottom<0||r.top>H)continue;if(r.width>=1000&&r.height>=1500)continue;
 const tr=textRects(e);const isText=tr.length>0;const isIcon=!isText&&((tg==='img'||isSvg||!borderOnly(e))&&r.width<=220&&r.height<=220||tg==='img');KD=isText?'texto':(isIcon?'icone':'bloco');
 if(!isText&&!isIcon&&r.width>=700)continue;
 const b=isText?U(tr):r;   // caixa que importa: o texto em si
 const S=sig(e);
 const vy=Math.max(0,Math.min(b.bottom,winBot)-Math.max(b.top,winTop))/b.height;if(vy<0.05)continue;
 const vx=Math.max(0,Math.min(b.right,W)-Math.max(b.left,0))/b.width;
 if(vy<0.85&&vy>0.2&&vx>0.5&&(isText||isIcon))out.push({k:KD,tipo:'MASCARA',sig:S,box:[b.left,b.top,b.right,b.bottom],det:'visível '+Math.round(vy*100)+'%'+(isText?' (texto)':'')});
 if(vx<0.97&&vx>0.2&&vy>0.5)out.push({k:KD,tipo:'BORDA',sig:S,box:[b.left,b.top,b.right,b.bottom],det:'visível '+Math.round(vx*100)+'% na horizontal'});
 if(vx>=0.97&&vy>0.5){const bx0=b.left,bx1=b.right,by0=Math.max(b.top,winTop),by1=Math.min(b.bottom,winBot);const fora=[];
  if(bx0<Z.x0-2)fora.push('esq '+Math.round(bx0));if(bx1>Z.x1+2)fora.push('dir '+Math.round(bx1));
  if(Z.y0!=null){if(by0<Z.y0-2)fora.push('topo '+Math.round(by0));const lim=(bx1<=Z.x2+2)?Z.y2:Z.y1;if(by1>lim+2)fora.push('base '+Math.round(by1))}
  if(fora.length)out.push({k:KD,tipo:'MARGEM',sig:S,box:[b.left,b.top,b.right,b.bottom],det:fora.join(', ')})}
 // ---- oculto / tachado
 if((isText||isIcon)&&vy>0.6&&vx>0.9){const rs=isText?tr:[r];const pts=[];
  for(const q of rs){const cx=(q.left+q.right)/2,cy=(q.top+q.bottom)/2;pts.push([cx,cy],[q.left+q.width*.2,cy],[q.right-q.width*.2,cy],[cx,q.top+q.height*.3],[cx,q.bottom-q.height*.3])}
  const hits={};
  for(const [x,y] of pts){if(x<0||x>=W||y<0||y>=H)continue;
   for(const s of document.elementsFromPoint(x,y)){
    if(s===e||e.contains(s)||s.contains(e))break;if(s.classList&&s.classList.contains('mask'))break;
    if(!stage.contains(s))continue;if(ign(s))continue;if(!paints(s))continue;if(opac(s)<0.3)continue;
    const sr=s.getBoundingClientRect();if(sr.width>=1000&&sr.height>=1500)continue;
    if(borderOnly(s)){const bw=parseFloat(getComputedStyle(s).borderTopWidth)+3;if(!(x-sr.left<bw||sr.right-x<bw||y-sr.top<bw||sr.bottom-y<bw))continue}
    const k=sig(s);hits[k]=hits[k]||{n:0,s,sr};hits[k].n++;break}}
  for(const k in hits){const h=hits[k];const sr=h.sr;
   const strike=isText&&sr.height<=34&&sr.width>=b.width*0.5&&sr.top>b.top&&sr.bottom<b.bottom;
   if(strike){const cy=(sr.top+sr.bottom)/2;const mid=b.top+b.height*0.55;const off=(cy-mid)/b.height;
     if(Math.abs(off)>0.12)out.push({k:KD,tipo:'TACHADO',sig:S,box:[b.left,b.top,b.right,b.bottom],det:'risco '+(off>0?'abaixo':'acima')+' do meio das letras ('+Math.round(off*100)+'% da altura)'});continue}
   if(h.n>=2||!isText)out.push({k:KD,tipo:'OCULTO',sig:S,box:[b.left,b.top,b.right,b.bottom],det:'coberto por "'+k+'" ('+h.n+'/'+pts.length+' pontos)'})}}
 // ---- apertado / vazando
 if(isText&&vy>0.9&&vx>0.97){const u=b;const cs=getComputedStyle(e);let box=null,own=false;
  if(bgOf(cs)||parseFloat(cs.borderTopWidth)>0){box=e.getBoundingClientRect();own=true}
  else{let best=null;for(const c of all){if(c===e||c.contains(e)||e.contains(c)||ign(c))continue;if(c.namespaceURI==='http://www.w3.org/2000/svg')continue;const cc=getComputedStyle(c);if(!bgOf(cc))continue;if(opac(c)<0.5)continue;
    const q=c.getBoundingClientRect();if(q.width<u.width*0.9||q.height<u.height*0.9)continue;const mx=(u.left+u.right)/2,my=(u.top+u.bottom)/2;if(mx<q.left||mx>q.right||my<q.top||my>q.bottom)continue;if(q.width>=1000&&q.height>=1500)continue;
    if(!best||q.width*q.height<best.width*best.height)best=q}box=best}
  if(box){const gh=Math.min(u.left-box.left,box.right-u.right),gv=Math.min(u.top-box.top,box.bottom-u.bottom);const limH=own?14:18;const cs2=getComputedStyle(e);const circ=own&&parseFloat(cs2.borderTopLeftRadius)>=Math.min(box.width,box.height)*0.45;const limV=circ?-99:(own?5:12);
   if(gh<-1||gv<-1)out.push({k:KD,tipo:'APERTADO',sig:S,box:[u.left,u.top,u.right,u.bottom],det:'texto VAZANDO da caixa ('+Math.round(Math.min(gh,gv))+'px)'});
   else if(gh<limH||gv<limV)out.push({k:KD,tipo:'APERTADO',sig:S,box:[u.left,u.top,u.right,u.bottom],det:'folga '+Math.round(gh)+'px lateral / '+Math.round(gv)+'px vertical'})}}
 // ---- legenda
 if(leg&&(isText||isIcon)&&vy>0.5){const ix=Math.min(b.right,leg.right)-Math.max(b.left,leg.left),iy=Math.min(b.bottom,leg.bottom+8)-Math.max(b.top,leg.top-8);
  if(ix>0&&iy>0)out.push({k:KD,tipo:'LEGENDA',sig:S,box:[b.left,b.top,b.right,b.bottom],det:'encosta/cobre a legenda'})}
}
if(leg&&Z.y0!=null){const lim=(leg.right<=Z.x2+2)?Z.y2:Z.y1;if(leg.bottom>lim+2||leg.left<Z.x0||leg.right>Z.x1)out.push({k:KD,tipo:'MARGEM',sig:'legenda: '+leg.el.textContent.trim(),box:[leg.left,leg.top,leg.right,leg.bottom],det:'legenda fora da zona'})}
return out}
"""
MIN={'OCULTO':0.3,'TACHADO':0.2,'APERTADO':0.3,'MARGEM':0.4,'BORDA':0.8,'MASCARA':0.6,'LEGENDA':0.3,'LOOP':0}
SEV={'OCULTO':'GRAVE','TACHADO':'MÉDIO','APERTADO':'MÉDIO','MARGEM':'GRAVE' if A.modo=='ads' else 'MÉDIO','BORDA':'MÉDIO','MASCARA':'MÉDIO','LEGENDA':'GRAVE','LOOP':'MÉDIO'}

with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path=chrome or None,args=["--disable-gpu","--allow-file-access-from-files"])
    pg=br.new_page(viewport={"width":1080,"height":1920})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto("file:///"+HTML.replace("\\","/"));pg.wait_for_function("window.READY===1",timeout=60000)
    pg.add_style_tag(content="*{pointer-events:auto !important}")
    ts=[round(i*A.passo,3) for i in range(int(DUR/A.passo)+1)]
    raw={}
    for t in ts:
        pg.evaluate("t=>window.render(t)",t)
        for it in pg.evaluate(JS,ZONA):
            k=(it['tipo'],it['sig'],it['det'].split(' (')[0] if it['tipo'] in('OCULTO','TACHADO') else '')
            raw.setdefault(k,[]).append((t,it))
    grupos=[]
    for (tipo,s,_),lst in raw.items():
        cur=[lst[0]]
        for a,b in zip(lst,lst[1:]):
            if b[0]-a[0]<=A.passo*1.6:cur.append(b)
            else:grupos.append((tipo,s,cur));cur=[b]
        grupos.append((tipo,s,cur))
    res=[]
    for tipo,s,cur in grupos:
        d=cur[-1][0]-cur[0][0]+A.passo
        if d<MIN[tipo]-1e-6 or (tipo=='OCULTO' and len(cur)<2):continue
        mid=cur[len(cur)//2]
        sev=SEV[tipo]
        if tipo=='MASCARA' and '(texto)' not in mid[1]['det']:sev='LEVE'
        if tipo in('MARGEM','BORDA') and mid[1].get('k')=='bloco':sev='LEVE'
        res.append(dict(tipo=tipo,sev=sev,sig=s,t0=cur[0][0],t1=cur[-1][0],tmid=mid[0],box=mid[1]['box'],det=mid[1]['det']))
    ordem={'GRAVE':0,'MÉDIO':1,'LEVE':2}
    res.sort(key=lambda r:(ordem[r['sev']],r['t0']))
    loop=A.loop=='sim' or (A.loop=='auto' and A.modo=='organico' and 'PER(' in src)
    if loop:
        pg.evaluate("t=>window.render(t)",0);pg.screenshot(path=os.path.join(OUT,'_l0.png'))
        pg.evaluate("t=>window.render(t)",DUR);pg.screenshot(path=os.path.join(OUT,'_l1.png'))
        a=Image.open(os.path.join(OUT,'_l0.png')).convert('L');b=Image.open(os.path.join(OUT,'_l1.png')).convert('L')
        df=ImageChops.difference(a,b).point(lambda v:255 if v>40 else 0);n=int(sum(df.histogram()[255:]))
        if n>300:res.append(dict(tipo='LOOP',sev='MÉDIO',sig='primeiro x último quadro',t0=0,t1=DUR,tmid=DUR,box=list(df.getbbox() or (0,0,1080,1920)),det=f'{n} px diferentes'))
    try:fnt=ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","fonts","Poppins-Bold.ttf"),26)
    except Exception:fnt=ImageFont.load_default()
    for i,r in enumerate(res[:40]):
        pg.evaluate("t=>window.render(t)",r['tmid']);p=os.path.join(OUT,'ev_%02d.png'%i);pg.screenshot(path=p)
        im=Image.open(p).convert('RGB');dr=ImageDraw.Draw(im);x0,y0,x1,y1=[int(v) for v in r['box']]
        if A.modo=='ads':dr.rectangle((ZONA['x0'],ZONA['y0'],ZONA['x1'],ZONA['y1']),outline=(0,200,0),width=3);dr.rectangle((ZONA['x0'],ZONA['y1'],ZONA['x2'],ZONA['y2']),outline=(0,200,0),width=3)
        else:dr.line((ZONA['x0'],0,ZONA['x0'],1920),fill=(0,200,0),width=2);dr.line((ZONA['x1'],0,ZONA['x1'],1920),fill=(0,200,0),width=2)
        dr.rectangle((x0-5,y0-5,x1+5,y1+5),outline=(255,0,180),width=6)
        cx0,cy0=max(0,x0-280),max(0,y0-280);cx1,cy1=min(1080,x1+280),min(1920,y1+280)
        im=im.crop((cx0,cy0,cx1,cy1));sc=min(1,720/max(im.size));im=im.resize((int(im.size[0]*sc),int(im.size[1]*sc)))
        dr=ImageDraw.Draw(im);dr.rectangle((0,0,im.size[0],40),fill=(0,0,0));dr.text((10,6),f"#{i} {r['tipo']} {r['tmid']:.1f}s",fill=(255,255,255),font=fnt)
        im.save(p);r['evidencia']=p
    th=[];T=0.0
    while T<=DUR+1e-6:
        pg.evaluate("t=>window.render(t)",T);p=os.path.join(OUT,'_c.png');pg.screenshot(path=p)
        im=Image.open(p).convert('RGB').resize((270,480));d=ImageDraw.Draw(im);d.rectangle((0,0,86,32),fill=(0,0,0));d.text((6,3),f"{T:.0f}s",fill=(255,255,255),font=fnt)
        th.append(im);T+=2.0
    cols=8
    for k in range(0,len(th),cols*2):
        bloco=th[k:k+cols*2];sheet=Image.new('RGB',(270*cols,480*math.ceil(len(bloco)/cols)),(255,255,255))
        for j,im in enumerate(bloco):sheet.paste(im,((j%cols)*270,(j//cols)*480))
        sheet.save(os.path.join(OUT,'folha_%02d.jpg'%(k//(cols*2))),quality=78)
    br.close()

avisos=[]
wj=os.path.join(PASTA,'words.js')
if os.path.exists(wj):
    try:
        words=json.loads(open(wj,encoding='utf-8').read().split('=',1)[1].strip().rstrip(';'))
        for w in words:
            s=str(w[0])
            if re.search(r'\d',s):avisos.append(f'legenda com dígito "{s}" em {w[1]:.1f}s (está falado por extenso?)')
            if s.lower().startswith('comodo'):avisos.append(f'"Comodo" sem acento na legenda em {w[1]:.1f}s')
    except Exception as e:avisos.append(f'não li words.js: {e}')
json.dump(dict(html=HTML,modo=A.modo,dur=DUR,erros_js=errs,achados=res,avisos=avisos),open(os.path.join(OUT,'achados.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
L=[f'# Validação automática · {os.path.basename(HTML)} · modo {A.modo} · {DUR:.1f}s','']
if errs:L+=['## Erros de JavaScript']+[f'- {e}' for e in errs]+['']
L.append(f'## Achados ({len(res)})')
for i,r in enumerate(res):L.append(f"- **#{i} {r['sev']} · {r['tipo']}** {r['t0']:.1f}–{r['t1']:.1f}s · \"{r['sig']}\" · {r['det']}"+(f" · `{os.path.basename(r['evidencia'])}`" if r.get('evidencia') else ''))
if avisos:L+=['','## Avisos de legenda']+[f'- {a}' for a in avisos]
L+=['','Folhas de contato (1 quadro a cada 2 s): '+', '.join(sorted(f for f in os.listdir(OUT) if f.startswith('folha_')))]
open(os.path.join(OUT,'relatorio.md'),'w',encoding='utf-8').write('\n'.join(L))
print('\n'.join(L))
