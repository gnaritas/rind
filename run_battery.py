#!/usr/bin/env python3
"""Vision battery for RIND by Block Island Charcuterie new-site sign-off (t_387b338d).
Fork of deannas-wine-bar/run_battery.py (itself shibuya lineage) — OpenRouter
gemini-2.5-flash, threaded, forced VERDICT line. Shots are dsf-1 native widths
(1280 desktop / 390 mobile) — no resample."""
import base64, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')

env = {}
for line in open(os.path.expanduser('~/.hermes/.env')):
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1); env[k.strip()] = v.strip().strip('"\'')
KEY = env.get('OPENROUTER_API_KEY') or env.get('OPENROUTER_KEY')
if not KEY:
    print('NO OPENROUTER KEY'); sys.exit(2)

Q = ("This is a full-page {kind} screenshot of a business website (charcuterie-shop design: "
     "deep roast-brown hero band and footer, warm bone-paper body, white board-style panels each "
     "capped by a colored wax stripe across their top edge (paprika orange / sage green / gold — "
     "intentional), a colored gradient strip across the very top of the page (orange→gold→green, "
     "intentional), a giant letter-spaced serif wordmark 'RIND' on the dark hero, monospace "
     "small-caps labels, a flat vector illustration of a grazing board (cheese wheel with orange "
     "rind ring, salami coins, crackers, olives, grapes — intentional art, not a photo), rounded "
     "paprika-orange CTA buttons, numbered build-your-own steps with gold right-borders). "
     "List every visual or layout defect: misaligned columns/grids, text overflowing or clipped, "
     "uneven margins/spacing, overlapping elements, stretched/cropped images or iframes, broken "
     "nav/footer, inconsistent widths, garbled characters or stray glyphs, unreadable contrast. "
     "Do NOT flag: map tiles that are blank/grey or loading (sweep artifact), the flat vector "
     "grazing-board illustration (intentional art), the colored gradient top strip (intentional), "
     "the colored wax stripes on panel top edges (intentional), rounded corners on panels (boards, "
     "intentional), the giant letter-spaced RIND wordmark (intentional), responsive single-column "
     "stacking on mobile, textarea resize handles, normal line-wrapping in header nav or footer, "
     "the © year, wide letter-spacing on small-caps labels (intentional style), buttons that fit "
     "their text tightly, the numbered-steps list styling. Answer with ONE line only: "
     "'VERDICT: CLEAN' or 'VERDICT: MAP-BLANK' or 'VERDICT: DEFECTS - <list>'.")

def ask(name, path, kind):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    body = {
        'model': 'google/gemini-2.5-flash',
        'temperature': 0.2,
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': Q.format(kind=kind)},
            {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + data}},
        ]}],
        'max_tokens': 400,
    }
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
                                 data=json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + KEY,
                                          'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.load(r)
            txt = j['choices'][0]['message']['content'].strip()
            return name, txt
        except Exception as e:
            if attempt == 2:
                return name, 'ERROR ' + repr(e)[:120]

jobs = []
for f in sorted(os.listdir(SHOTS)):
    if f.endswith('_mobile.png'):
        jobs.append((f, os.path.join(SHOTS, f), 'mobile (390px wide)'))
    elif f.endswith('_desktop.png'):
        jobs.append((f, os.path.join(SHOTS, f), 'desktop (1280px wide)'))
jobs.append(('og.png', os.path.join(HERE, 'public', 'og.png'),
             'desktop 1200x630 social share card — judge text fit inside the brown frame with orange top bar, no clipping, readable contrast'))

results = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    for name, txt in ex.map(lambda a: ask(*a), jobs):
        results[name] = txt
        print('%-36s %s' % (name, (txt or '')[:220]))
open(os.path.join(SHOTS, 'vision-results.json'), 'w').write(json.dumps(results, indent=1))
print('wrote vision-results.json (%d shots)' % len(results))
