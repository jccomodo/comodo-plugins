import os, shutil
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(H, "frames"); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
chrome = next(iter([os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser(r"~\.cache\puppeteer\chrome")) for f in fs if f == "chrome.exe"]), None)  # Chrome do puppeteer, se houver; senão o Chromium do Playwright
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=chrome or None, args=["--disable-gpu", "--allow-file-access-from-files"])
    pg = br.new_page(viewport={"width": 760, "height": 260}, device_scale_factor=1.5)
    pg.goto("file:///" + os.path.join(H, "anim.html").replace("\\", "/")); pg.wait_for_function("window.READY===1"); pg.wait_for_timeout(300)
    for i in range(108):
        pg.evaluate("t=>window.render(t)", i / 30.0); pg.screenshot(path=os.path.join(out, "%04d.png" % (i + 1)), omit_background=True)
    br.close()
print("ok")
