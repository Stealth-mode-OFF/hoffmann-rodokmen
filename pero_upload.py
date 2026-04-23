#!/usr/bin/env python3
"""
PERO OCR bulk uploader — používá session cookies (remember_token).

USAGE:
  python3 pero_upload.py <folder>           # upload + layout + (manual OCR)
  python3 pero_upload.py <folder> --ocr     # auto-poll + trigger OCR

REQUIREMENTS:
  Přihlášený PERO účet, REMEMBER_TOKEN aktualizovaný (z F12 → Cookies).
"""
import os, re, sys, time, urllib.request, urllib.parse, urllib.error, http.cookiejar, uuid, io

BASE = "https://pero-ocr.fit.vutbr.cz"
REMEMBER_TOKEN = "3397|83dd3e8e7c1bb07510ad0998e9b45b58042146e1e9042109d39714612b53cde18b57a8ce7f2c795bd7238286d43f09c4a27a05d816d34cc6ab69f4653e284215"

# IDs (zjištěny inspekcí formulářů 23.4.2026)
LAYOUT_HANDWRITTEN = "d3152d9a-0662-4886-9998-423b2d8a1724"   # Handwritten layout
OCR_KURRENT = "e73416f7-61ad-4128-a966-8de09195e7d5"           # Kurrent (German, Czech)
OCR_BASELINE = "10876486-0566-43f3-9732-d58785d05d7e"          # baseline_id pro OCR krok (Handwritten)
LANG_GERMAN = "8b445087-f3e5-41dc-8143-4feeb967bf1e"           # German LM

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)
FOLDER = os.path.expanduser(sys.argv[1])
AUTO_OCR = "--ocr" in sys.argv[2:]
DOC_NAME = os.path.basename(FOLDER.rstrip("/"))
SOURCE = os.path.join(FOLDER, "small") if os.path.isdir(os.path.join(FOLDER, "small")) else FOLDER

# Auth
jar = http.cookiejar.CookieJar()
c = http.cookiejar.Cookie(0, "remember_token", REMEMBER_TOKEN, None, False,
    "pero-ocr.fit.vutbr.cz", True, False, "/", True, True, None, False, None, None, {}, False)
jar.set_cookie(c)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def multipart_post(path, fields, files=None):
    boundary = f"----PERO{uuid.uuid4().hex}"
    buf = io.BytesIO()
    for k, v in fields.items():
        buf.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    for name, filename, data in (files or []):
        buf.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode())
        buf.write(data); buf.write(b"\r\n")
    buf.write(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(f"{BASE}{path}", data=buf.getvalue(), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return opener.open(req, timeout=120)

def urlenc_post(path, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    return opener.open(req, timeout=30)

def get(path):
    return opener.open(f"{BASE}{path}", timeout=60)

def get_csrf():
    html = get("/document/new_document").read().decode()
    m = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', html)
    return m.group(1) if m else None

def create_doc(name):
    csrf = get_csrf()
    r = multipart_post("/document/new_document", {"csrf_token": csrf, "document_name": name})
    m = re.search(r"upload_images_to_document/([\w-]+)", r.geturl())
    if not m: raise RuntimeError(f"No doc_id in {r.geturl()}")
    return m.group(1)

def upload(doc_id, path):
    with open(path, "rb") as f: data = f.read()
    return multipart_post(f"/document/upload_image_to_document/{doc_id}",
        {}, [("file", os.path.basename(path), data)]).status

def start_layout(doc_id):
    get(f"/layout_analysis/select_layout/{doc_id}")
    return urlenc_post(f"/layout_analysis/start_layout/{doc_id}",
        {"layout_detector_id": LAYOUT_HANDWRITTEN}).status

def start_ocr(doc_id):
    # Inspect OCR form to get current field names
    html = get(f"/ocr/select_ocr/{doc_id}").read().decode()
    form_action = re.search(r'<form[^>]*action=["\']([^"\']+)["\']', html)
    action = form_action.group(1) if form_action else f"/ocr/start_ocr/{doc_id}"
    fields = {"baseline_id": OCR_BASELINE, "ocr_id": OCR_KURRENT, "language_model_id": LANG_GERMAN}
    return urlenc_post(action, fields).status

def doc_state(doc_id):
    html = get("/document/documents").read().decode()
    idx = html.find(doc_id)
    if idx < 0: return "?"
    snippet = html[idx:idx+2500]
    for state in ("OCR completed", "Running OCR", "Layout analysis completed", "Running layout", "New"):
        if state in snippet: return state
    return "?"

# === Main ===
print(f"PERO bulk: {FOLDER}")
jpgs = sorted(f for f in os.listdir(SOURCE) if f.startswith("page_") and f.endswith(".jpg"))
print(f"Images: {len(jpgs)} from {SOURCE}")

doc_id = create_doc(DOC_NAME)
print(f"Doc: {doc_id}\nURL: {BASE}/ocr/show_results/{doc_id}\n")

for i, jpg in enumerate(jpgs, 1):
    try:
        upload(doc_id, os.path.join(SOURCE, jpg))
        if i % 10 == 0 or i == len(jpgs):
            print(f"  [{i}/{len(jpgs)}] {jpg}")
    except Exception as e:
        print(f"  [{i}] ERR: {e}")

print(f"\nLayout: {start_layout(doc_id)}")

if not AUTO_OCR:
    print(f"\nDONE upload + layout. To trigger OCR after layout completes:")
    print(f"  curl/browse {BASE}/ocr/select_ocr/{doc_id}")
    sys.exit(0)

# Wait for layout
print("Waiting for layout completion...")
while True:
    time.sleep(30)
    s = doc_state(doc_id)
    print(f"  state: {s}")
    if s in ("Layout analysis completed", "Running OCR", "OCR completed"): break
    if s == "?": print("  (state unknown, retrying)")

if "OCR" not in doc_state(doc_id):
    print(f"\nOCR: {start_ocr(doc_id)}")
print(f"\nMonitor: {BASE}/document/documents")
