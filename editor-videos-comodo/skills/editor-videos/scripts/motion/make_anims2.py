"""Renderiza cenas guiadas por palavras. jobs = [{"scene","cues":[s...],"dur":s,"out":pasta,"scale":1.5}]"""
import json, os, sys, shutil
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
chrome = next(iter([os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f == "chrome.exe"]), None)  # Chrome do puppeteer, se houver; senão o Chromium do Playwright
jobs = json.load(open(sys.argv[1], encoding="utf-8-sig"))
only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome or None, args=["--disable-gpu", "--allow-file-access-from-files"])
    scale = jobs[0].get("scale", 1.5)
    pg = br.new_page(viewport={"width": 900, "height": 330}, device_scale_factor=scale)
    pg.goto("file:///" + os.path.join(HERE, "scenes.html").replace("\\", "/"))
    pg.wait_for_timeout(700)
    for j in jobs:
        if only and j["scene"] not in only:
            continue
        out = j["out"] if os.path.isabs(j["out"]) else os.path.join(HERE, j["out"])
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out, exist_ok=True)
        n = max(2, int(round(j["dur"] * 30)))
        pg.evaluate("([s,c,d])=>setScene(s,c,d)", [j["scene"], j["cues"], j["dur"]])
        for i in range(n):
            pg.evaluate(f"render({i / 30.0})")
            pg.screenshot(path=os.path.join(out, "%04d.png" % (i + 1)), omit_background=True)
        print(j["scene"], n, "quadros", flush=True)
    br.close()

