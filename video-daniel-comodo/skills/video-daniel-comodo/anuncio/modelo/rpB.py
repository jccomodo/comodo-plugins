"""Renderiza o overlay (copy + cartões) quadro a quadro em PNG transparente: frames2_content (o que aparece) e frames2_mask (onde o vídeo fica desfocado).
Uso: python rpB.py frames content|mask INICIO FIM   |   python rpB.py test 1.0,2.5,...  (prévia v2_XX.png)
Com tmap.json, o quadro t da narração nova mostra o overlay no tempo antigo N(t)."""
import os,sys,subprocess
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tmap import N
H=os.path.dirname(os.path.abspath(__file__))
chrome=next(iter([os.path.join(r,f) for r,_,fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f=="chrome.exe"]),None)
def page(br,mask):
    pg=br.new_page(viewport={"width":1080,"height":1920});pg.on("pageerror",lambda e:print("err:",e));pg.on("console",lambda m:print("console:",m.text) if m.type=="error" else None)
    pg.goto("file:///"+os.path.join(H,"overlay.html").replace("\\","/")+("?mask=1" if mask else ""));pg.wait_for_function("window.READY===1",timeout=60000);return pg
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path=chrome or None,args=["--disable-gpu","--allow-file-access-from-files"])
    mode=sys.argv[1]
    if mode=="test":
        pg=page(br,False);pm=page(br,True)
        for i,t in enumerate([float(x) for x in sys.argv[2].split(",")]):
            pg.evaluate("t=>window.render(t)",t);pg.screenshot(path=os.path.join(H,"v2c_%02d.png"%i),omit_background=True)
            pm.evaluate("t=>window.render(t)",t);pm.screenshot(path=os.path.join(H,"v2m_%02d.png"%i),omit_background=True)
            subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.3f}","-i","src.mp4","-i","v2m_%02d.png"%i,"-i","v2c_%02d.png"%i,"-filter_complex","[0:v]split[a][b];[b]gblur=sigma=26:steps=2,eq=brightness=-0.05:saturation=1.08,format=rgba[bl];[1:v]format=rgba,alphaextract[mk];[bl][mk]alphamerge[pl];[a][pl]overlay[x];[x][2:v]overlay,scale=360:640","-frames:v","1","v2_%02d.png"%i],cwd=H)
    else:
        kind,a,b=sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
        pg=page(br,kind=="mask");out=os.path.join(H,"frames2_"+kind);os.makedirs(out,exist_ok=True)
        for i in range(a,b):
            pg.evaluate("t=>window.render(t)",N(i/30.0));pg.screenshot(path=os.path.join(out,"%05d.png"%(i+1)),omit_background=True)
    br.close()
print("ok")

