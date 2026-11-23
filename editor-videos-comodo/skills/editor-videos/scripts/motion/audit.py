"""Auditoria de layout: mede a caixa de cada elemento em cada instante e aponta sobreposições.
uso: python audit.py anims2.json [cena,...]"""
import json, os, sys, itertools
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
chrome = next(iter([os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f == "chrome.exe"]), None)  # Chrome do puppeteer, se houver; senão o Chromium do Playwright
jobs = json.load(open(sys.argv[1], encoding="utf-8-sig"))
only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
JS = """()=>{const svg=document.getElementById('s');const kids=Array.from(svg.children);
 function tight(e){let U=null;const nodes=(e.children&&e.children.length)?Array.from(e.querySelectorAll('*')):[e];
   nodes.forEach(n=>{const tg=n.tagName.toLowerCase();if(['g','defs','lineargradient','radialgradient','stop','filter','fedropshadow'].includes(tg))return;
     let r=n.getBoundingClientRect();if(r.width<0.5&&r.height<0.5)return;let x=r.left,y=r.top,w=r.width,h=r.height;
     if(tg=='text'){y=r.top+0.24*r.height;h=0.62*r.height;if(!(n.textContent||'').trim())return}
     const o=(function(el){let v=1;while(el&&el!==svg){const a=el.getAttribute&&el.getAttribute('opacity');if(a!==null&&a!==undefined)v*=parseFloat(a);el=el.parentNode}return v})(n);
     if(o<0.05)return;
     if(!U)U={x1:x,y1:y,x2:x+w,y2:y+h};else{U.x1=Math.min(U.x1,x);U.y1=Math.min(U.y1,y);U.x2=Math.max(U.x2,x+w);U.y2=Math.max(U.y2,y+h)}});
   return U}
 const out=[];kids.forEach((e,i)=>{if(i<2)return;const U=tight(e);if(!U)return;
   let o=e.getAttribute('opacity');o=o===null?1:parseFloat(o);
   out.push({i,tag:e.tagName,tx:(e.textContent||'').trim().slice(0,16),x:U.x1,y:U.y1,w:U.x2-U.x1,h:U.y2-U.y1,o})});
 const T=tight(kids[1])||{x1:0,y1:0,x2:1,y2:1};return {title:{x:T.x1,y:T.y1,w:T.x2-T.x1,h:T.y2-T.y1},items:out}}"""
def contains(o, i):
    return i["x"] >= o["x"] - 2 and i["y"] >= o["y"] - 2 and i["x"] + i["w"] <= o["x"] + o["w"] + 2 and i["y"] + i["h"] <= o["y"] + o["h"] + 2
def inter(a, b):
    if contains(a, b) or contains(b, a): return None
    w = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]); h = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return (w, h) if w > 3 and h > 3 else None
bad_total = 0
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome or None, args=["--disable-gpu", "--allow-file-access-from-files"])
    pg = br.new_page(viewport={"width": 900, "height": 330})
    pg.goto("file:///" + os.path.join(HERE, "scenes.html").replace("\\", "/")); pg.wait_for_timeout(500)
    for j in jobs:
        if only and j["scene"] not in only: continue
        pg.evaluate("([s,c,d])=>setScene(s,c,d)", [j["scene"], j["cues"], j["dur"]])
        seen = {}
        t = 0.0
        while t <= j["dur"]:
            pg.evaluate(f"render({t})"); d = pg.evaluate(JS)
            vis = [it for it in d["items"] if it["o"] > 0.5 and it["w"] > 6 and it["h"] > 6]
            for it in vis:      # fora do cartão
                if it["x"] < 6 or it["x"] + it["w"] > 894 or it["y"] + it["h"] > 326:
                    seen.setdefault(("BORDA", it["tx"] or it["tag"], ""), t)
                ti = inter(it, d["title"]) if it["w"] < 880 else None
                if ti: seen.setdefault(("TITULO", it["tx"] or it["tag"], ""), t)
            for a_, b_ in itertools.combinations(vis, 2):
                r = inter(a_, b_)
                if r: seen.setdefault(("SOBREPOE", a_["tx"] or a_["tag"] + str(a_["i"]), b_["tx"] or b_["tag"] + str(b_["i"])), t)
            t = round(t + 0.1, 3)
        print("== %s (%.1fs): %d conflitos" % (j["scene"], j["dur"], len(seen)))
        for k, v in seen.items():
            print("   %-9s %-18s %-18s a partir de %.1fs" % (k[0], k[1], k[2], v))
        bad_total += len(seen)
    br.close()
print("TOTAL de conflitos:", bad_total)

