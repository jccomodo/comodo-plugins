"""Renderiza as cenas de motion graphics (scenes.html) em sequências PNG com transparência.
uso: python make_anims.py anims.json     (anims.json = [{"scene":"etiqueta","dur":4.2,"out":"frames/etiqueta"} ...])"""
import json, os, sys, shutil
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
chrome = next(iter([os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f == "chrome.exe"]), None)  # Chrome do puppeteer, se houver; senão o Chromium do Playwright
jobs = json.load(open(sys.argv[1], encoding="utf-8-sig"))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome or None, args=["--disable-gpu", "--allow-file-access-from-files"])
    pg = br.new_page(viewport={"width": 900, "height": 420}, device_scale_factor=1)
    pg.goto("file:///" + os.path.join(HERE, "scenes.html").replace("\\", "/"))
    pg.wait_for_timeout(600)
    for j in jobs:
        out = os.path.join(HERE, j["out"]) if not os.path.isabs(j["out"]) else j["out"]
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out, exist_ok=True)
        n = max(2, int(round(j["dur"] * 30)))
        pg.evaluate(f"setScene('{j['scene']}')")
        for i in range(n):
            pg.evaluate(f"render({i / (n - 1)})")
            pg.screenshot(path=os.path.join(out, "%04d.png" % (i + 1)), omit_background=True)
        print(j["scene"], n, "quadros")
    br.close()

