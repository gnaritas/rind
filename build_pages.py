#!/usr/bin/env python3
"""RIND by Block Island Charcuterie — generator (single source for all pages).
websites lane, card t_387b338d. Built 2026-11-25. Demo host pinned from first byte.
Design: cheese-wax palette — roast-brown ink, bone paper, paprika/sage/gold wax accents;
"board" panels get a colored wax rind across the top edge; rounded corners (boards, not
labels). No photos, no third-party JS, no webfonts.
Facts ONLY from press-verified card sources: Newsday (rind-by-block-island-charcuterie-
northport-cxbsmqvv), Hoodline 2026-10, GreaterLongIsland.com 2026-10. Building address
24 Woodbine Ave corroborated: OpenStreetMap way 465988581 + Yelp + MapQuest +
thethompsonbuilding.com (Northport Historical Society). Unknown (phone, hours, prices,
exact opening day) = omitted, never guessed."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://rind-demo.up.railway.app"

BRAND = "RIND by Block Island Charcuterie"
BRAND_PLAIN = "RIND by Block Island Charcuterie"
ADDR = "The Thompson Building, 24 Woodbine Avenue, Northport, NY 11768"
GEO = (40.899668, -73.351223)  # building centroid, OpenStreetMap way 465988581 (ODbL)
MAP_Q = "https://www.google.com/maps?q=24%20Woodbine%20Avenue%2C%20Northport%2C%20NY%2011768&output=embed"
DIRS = "https://www.google.com/maps/dir/?api=1&destination=24%20Woodbine%20Avenue%2C%20Northport%2C%20NY%2011768"
EMAIL = "blockislandcharcuterie@gmail.com"

def head(title, desc, path, ld=None, utility=False, og_desc=None):
    u = ORIGIN + path
    d = desc.replace('"', "'")
    od = (og_desc or desc).replace('"', "'")
    parts = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
             '<meta name="robots" content="noindex, nofollow">',
             '<!-- BUILT-2026-11-25 -->',
             '<title>%s</title>' % title,
             '<meta name="description" content="%s">' % d,
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<link rel="canonical" href="%s">' % u,
             '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
             '<link rel="stylesheet" href="/style.css">']
    if not utility:
        t = title.replace('"', "'")
        od = (og_desc or desc).replace('"', "'")
        parts += [
            '<meta property="og:type" content="website">',
            '<meta property="og:title" content="%s">' % t,
            '<meta property="og:description" content="%s">' % od,
            '<meta property="og:image" content="%s/og.png">' % ORIGIN,
            '<meta property="og:url" content="%s">' % u,
            '<meta name="twitter:card" content="summary_large_image">']
    for blk in (ld or []):
        parts.append('<script type="application/ld+json">%s</script>' % json.dumps(blk, ensure_ascii=False))
    parts.append('</head>')
    return "\n".join(parts)

NAV_LINKS = [
    ("Story & concept", "/the-concept"),
    ("Build your own", "/build-your-own"),
    ("Boards & events", "/boards-for-events"),
    ("Visit", "/visit"),
]

def nav(active):
    items = []
    for label, href in NAV_LINKS:
        cur = ' aria-current="page"' if href == active else ""
        items.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    items.append('<a class="btn sm" href="/contact">Opening-day list</a>')
    return ('<body>\n<div class="topline" aria-hidden="true"></div>\n'
            '<a class="skip" href="#main">Skip to content</a>\n'
            '<header class="site">\n'
            '<p class="brand"><a href="/"><span class="wordmark">RIND</span> <em>by Block Island Charcuterie</em></a></p>\n'
            '<nav aria-label="Site"><p>%s</p></nav>\n'
            '</header>\n<main id="main">' % " ".join(items))

FOOTER = ('</main>\n<footer>\n'
          '<p class="footline">%s</p>\n'
          '<p class="footline">%s</p>\n'
          '<p class="footline fine">&copy; 2026 &middot; <a href="/the-concept">Story</a> &middot; <a href="/build-your-own">Build your own</a> &middot; <a href="/boards-for-events">Boards &amp; events</a> &middot; <a href="/visit">Visit</a> &middot; <a href="/contact">Contact</a> &middot; <a href="/privacy">Privacy</a></p>\n'
          '</footer>\n</body>\n</html>\n') % (BRAND_PLAIN, "Opening soon &middot; The Thompson Building, 24 Woodbine Avenue, entrance on Scudder Avenue &middot; Northport, NY 11768")

def store_node(path="/"):
    return {
        "@context": "https://schema.org",
        "@type": "FoodStore",
        "name": BRAND,
        "alternateName": "RIND",
        "url": ORIGIN + path,
        "image": ORIGIN + "/og.png",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "The Thompson Building, 24 Woodbine Avenue",
            "addressLocality": "Northport",
            "addressRegion": "NY",
            "postalCode": "11768",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": "https://www.google.com/maps?q=24%20Woodbine%20Avenue%2C%20Northport%2C%20NY%2011768",
    }

def breadcrumb(label, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": ORIGIN + path},
        ],
    }

def service_node(name, stype, desc, path):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": stype,
        "description": desc,
        "url": ORIGIN + path,
        "areaServed": [
            {"@type": "City", "name": "Northport", "containedInPlace": {"@type": "State", "name": "New York"}},
            {"@type": "Place", "name": "Long Island, New York"},
        ],
        "provider": {k: v for k, v in store_node(path).items() if k != "@context"},
    }

# Inline SVG grazing-board art for the hero (aria-hidden, decorative). Flat vector, no runtime.
BOARD_SVG = '''<svg class="board-art" viewBox="0 0 360 260" role="img" aria-hidden="true" focusable="false">
  <rect x="8" y="8" width="344" height="244" rx="26" fill="#3a2c1d"/>
  <rect x="20" y="20" width="320" height="220" rx="20" fill="#c9a26b"/>
  <circle cx="105" cy="105" r="46" fill="#f6f0e2"/>
  <path d="M105 59 a46 46 0 0 1 39 23 l-39 23 z" fill="#dfa443"/>
  <circle cx="105" cy="105" r="46" fill="none" stroke="#c05a2c" stroke-width="8"/>
  <path d="M59 105 a46 46 0 0 0 23 -39" fill="none" stroke="#c05a2c" stroke-width="8" stroke-linecap="round"/>
  <circle cx="215" cy="80" r="21" fill="#7c2f23"/>
  <circle cx="215" cy="80" r="21" fill="none" stroke="#5f2018" stroke-width="4"/>
  <circle cx="262" cy="96" r="21" fill="#8f3c18"/>
  <circle cx="262" cy="96" r="21" fill="none" stroke="#5f2018" stroke-width="4"/>
  <circle cx="238" cy="130" r="21" fill="#a34a22"/>
  <circle cx="238" cy="130" r="21" fill="none" stroke="#5f2018" stroke-width="4"/>
  <rect x="62" y="168" width="42" height="42" rx="8" fill="#e7d4ac" stroke="#b9993e" stroke-width="3" transform="rotate(-8 83 189)"/>
  <rect x="112" y="178" width="42" height="42" rx="8" fill="#eadfbe" stroke="#b9993e" stroke-width="3" transform="rotate(5 133 199)"/>
  <circle cx="205" cy="188" r="10" fill="#5d6b45"/>
  <circle cx="232" cy="198" r="10" fill="#50603c"/>
  <path d="M255 178 q26 -22 52 -6 q-20 20 -46 12 z" fill="#5d6b45"/>
  <circle cx="292" cy="150" r="9" fill="#6d4b8a"/>
  <circle cx="308" cy="164" r="9" fill="#5a3d74"/>
  <circle cx="298" cy="178" r="9" fill="#6d4b8a"/>
</svg>'''

pages = {}

# ---------------- HOME ----------------
home_ld = [store_node("/")]
pages["index.html"] = (
    head("RIND by Block Island Charcuterie — Build-Your-Own Charcuterie, Northport NY",
         "A build-your-own charcuterie shop from the founder of Block Island Charcuterie, opening in the historic Thompson Building in downtown Northport, Long Island: pick the cheese, pick the meats, grab the box.",
         "/", home_ld)
    + nav("/")
    + '''<section class="hero">
  <div class="hero-copy">
    <p class="lab mono">Build-your-own charcuterie &middot; Northport, New York</p>
    <h1 class="mark">RIND</h1>
    <p class="mark-sub mono">by Block Island Charcuterie</p>
    <p class="sub">Pick the cheese, pick the cured meats, pick what you like on the side — and walk out with a beautiful box made your way. A build-your-own cheese bar with a full retail shop, opening soon in the historic Thompson Building in downtown Northport.</p>
    <p class="hero-cta"><a class="btn" href="/contact">Get the opening-day email</a> <a class="ghost" href="/build-your-own">Build your own &rarr;</a></p>
  </div>
  ''' + BOARD_SVG + '''
</section>
<section class="panels">
  <article class="board wax-paprika">
    <p class="lab mono">The bar</p>
    <h2>Built like Chipotle,<br>curated like a cheese shop</h2>
    <p>The counter runs one way: cheeses, then cured meats, then the accouterments, then the size — from an individual box to boards big enough for a crowd. Grab-and-go, very quick.</p>
    <p><a href="/build-your-own">See how it works &rarr;</a></p>
  </article>
  <article class="board wax-sage">
    <p class="lab mono">The shop</p>
    <h2>Cheese by the cut, meats by the slice</h2>
    <p>Local and international cheeses, cured meats and specialty items — plus crackers, olives, salumi and other a la carte extras to shop by the side of your board.</p>
    <p><a href="/the-concept">Read the concept &rarr;</a></p>
  </article>
  <article class="board wax-gold">
    <p class="lab mono">The parties</p>
    <h2>Holiday boards &amp; grazing tables</h2>
    <p>Preorder bigger boards for holidays and special events, or book custom boards and full grazing tables for the celebration itself.</p>
    <p><a href="/boards-for-events">Boards for events &rarr;</a></p>
  </article>
</section>
<section class="band">
  <div class="band-copy">
    <p class="lab mono">Opening soon</p>
    <h2>First word goes to the list</h2>
    <p>The exact opening day, the hours and the board list land right here — and people on the opening-day list get the email first. The shop is going in downtown Northport, in the Thompson Building, a short walk from Main Street and the village dock.</p>
    <p><a class="btn" href="/contact">Join the opening-day list</a></p>
  </div>
  <div class="band-map"><iframe src="''' + MAP_Q + '''" loading="lazy" title="Map: RIND by Block Island Charcuterie, 24 Woodbine Avenue, Northport NY" allow="management:coordinate"></iframe><p class="mapcap">Thompson Building &middot; 24 Woodbine Ave, entrance on Scudder Ave &middot; <a href="''' + DIRS + '''">Get directions &nearr;</a></p></div>
</section>''')

# ---------------- THE CONCEPT (hub + FAQ + story) ----------------
faq_items = [
    ("When do you open?",
     "Around Thanksgiving 2026. The exact day and the hours post here first — and people on the <a href=\"/contact\">opening-day list</a> get the email before anyone else."),
    ("What does build-your-own mean?",
     "Founder Kaleigh Bernier describes the counter as Chipotle-style with a retail area: you pick your cheeses, cured meats and accouterments as you move down the bar, pick a size — individual box to multi-serving — and the box comes together in front of you. Grab-and-go, very quick."),
    ("Can I preorder boards for a party or the holidays?",
     "Yes — that's the whole point of the preorder line. Bigger boards for holidays and special events, plus custom boards and grazing tables for larger celebrations. <a href=\"/boards-for-events\">The details are here</a>, and the <a href=\"/contact\">form works for event inquiries</a> too."),
    ("Where exactly are you?",
     "The historic Thompson Building at 24 Woodbine Avenue in downtown Northport, with the entrance on Scudder Avenue — a short walk from Main Street, the village dock and Cow Harbor Park."),
    ("How much will boards cost?",
     "Prices post here the week we open — nothing is guessed before it's real. What you can count on: local and international cheeses, cured meats, accouterments, and boxes built to your picks at the counter."),
]
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a.replace("&#8217;", "'").replace("&#8209;", "-").replace("<a href=\"/contact\">", "").replace("<a href=\"/boards-for-events\">", "").replace("</a>", "")}}
                         for q, a in faq_items]}
pages["the-concept.html"] = (
    head("Scripts to Cheese: the Story & Concept — RIND by Block Island Charcuterie, Northport NY",
         "How a Broadway stage manager built a charcuterie business on Block Island and is now bringing the build-your-own cheese bar to downtown Northport — the concept, the story and the answers.",
         "/the-concept", [breadcrumb("Story & concept", "/the-concept"), faq_ld, store_node("/the-concept")])
    + nav("/the-concept")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Story &amp; concept</p>
  <h1>Scripts to cheese: from Broadway to Block Island to downtown Northport</h1>
  <p class="lede">RIND is the Northport storefront of Kaleigh Bernier — a Broadway stage manager turned charcuterie maker, who started curating cheese boards on Block Island during the pandemic and is now bringing the build-your-own counter to her new hometown.</p>
  <h2>The fix-it origin</h2>
  <p>Kaleigh is a Massachusetts native who studied theater in New York City and worked as a Broadway stage manager until the pandemic stopped the theaters cold. While waiting for Broadway to restart she was living on Block Island, Rhode Island — and found that the cheeses and cured meats she loved in the city were close to impossible to get on a small island. Her mother&#8217;s advice was blunt: <em>if you care about it, then fix it.</em></p>
  <p>She did. In 2021 she launched Block Island Charcuterie, building boards and elaborate grazing displays for weddings, private parties and other events — with marbled Sage Derby and butter-yellow Midnight Moon goat cheese among the staples — and grew it into the island&#8217;s charcuterie business. She still picks up substitute stage-manager shifts on Broadway (The Lost Boys and &amp; Juliet among them), and the island business continues seasonally while the Northport shop opens.</p>
  <h2>Why Northport</h2>
  <p>The move came through her fiancé, Nick Graci — a Northport native she met in theater school, who now runs NorthStream, a Long Island video production company. Kaleigh wanted a year-round home for a seasonal island business, and Northport — waterfront, boating community, tight network of local shops — looked like the place she already loved.</p>
  <p>&#8220;There&#8217;s just such a beautiful tie between Northport and Block Island,&#8221; she told Newsday. &#8220;All the yacht clubs go out to Block Island, so it kind of felt like a natural second place to open up.&#8221; And, to Greater Long Island: <em>&#8220;I wanted to bring that piece of my home to my new home.&#8221;</em></p>
  <h2>The counter</h2>
  <p>The concept, in Kaleigh&#8217;s own words, is &#8220;Chipotle-style with a retail area&#8221;: a build-your-own bar where customers select the components of an individual or multi-serving cheese and charcuterie box, with a full shop alongside — local and international cheeses, cured meats, crackers, olives, salumi and specialty items a la carte. &#8220;The idea is that it&#8217;s grab-and-go, very quick,&#8221; she says. &#8220;They&#8217;re having a picnic, they want something to eat in the park, they&#8217;re going out on a boat, they can come in and grab something that&#8217;s delicious, beautiful, healthy.&#8221;</p>
  <p>Ahead of the counter sit the preorder boards — bigger formats for holidays and events, custom boards and grazing tables — and on the cards: a cheese-of-the-month club and classes as the shop settles in.</p>
  <h2>The room</h2>
  <p>The shop is going into the Thompson Building: built in 1889 for the Edward Thompson Co., where enormous volumes of the American and English Encyclopedia of Law were printed until 1935, later a seat-belt factory, now restored office and retail space that keeps its original beams, brick and ironwork. The building&#8217;s owners hold tenants to the preserved brick and wood — which suits a shop built around beautiful, old-world provisions. Expect exposed brick and original beams over the counter when the doors open.</p>
  <h2>In the news</h2>
  <ul class="press">
    <li><a href="https://www.newsday.com/business/rind-by-block-island-charcuterie-northport-cxbsmqvv">Newsday — RIND by Block Island Charcuterie to open new store in Northport</a></li>
    <li><a href="https://greaterlongisland.com/say-cheese-new-charcuterie-shop-coming-to-downtown-northport/">Greater Long Island — Say cheese! New charcuterie shop coming to downtown Northport</a></li>
    <li><a href="https://hoodline.com/2026/10/broadway-stage-manager-swaps-scripts-for-cheese-boards-in-downtown-northport/">Hoodline — Broadway stage manager swaps scripts for cheese boards in downtown Northport</a></li>
  </ul>
  <p>The island original lives on: <a href="https://www.blockislandcharcuterie.com/">Block Island Charcuterie</a> continues seasonally for weddings, parties and events on Block Island, Rhode Island.</p>
  <h2>Questions people ask</h2>
  <dl class="faq">
''' + "".join('    <dt>%s</dt>\n    <dd>%s</dd>\n' % (q, a) for q, a in faq_items) + '''  </dl>
  <p class="lab mono">Keep going</p>
  <p class="cta-row"><a class="btn" href="/contact">Join the opening-day list</a> <a href="/build-your-own">Build your own</a> &middot; <a href="/boards-for-events">Boards &amp; events</a> &middot; <a href="/visit">Visit</a></p>
</article>''')

# ---------------- BUILD-YOUR-OWN DETAIL ----------------
pages["build-your-own.html"] = (
    head("Build-Your-Own Cheese Boards & Boxes — RIND, Northport NY",
         "The build-your-own charcuterie bar at RIND in Northport NY: pick cheeses, cured meats and accouterments at the counter, pick your size — individual box to multi-serving — and grab it to go.",
         "/build-your-own",
         [breadcrumb("Build your own", "/build-your-own"),
          service_node("Build-your-own charcuterie bar", "Build-your-own charcuterie counter",
                       "Customers select cheeses, cured meats and accouterments at the counter for individual or multi-serving charcuterie boxes, grab-and-go, at the Thompson Building in downtown Northport NY.",
                       "/build-your-own")])
    + nav("/build-your-own")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; <a href="/the-concept">Story &amp; concept</a> &middot; Build your own</p>
  <p class="lab mono">The counter &middot; how it works</p>
  <h1>Pick the cheese. Pick the meats. Grab the box.</h1>
  <p class="lede">One direction, one line, no guessing: the bar runs cheese first, then cured meats, then the good stuff on the side, then the size. Watch it come together and take it with you.</p>
  <ol class="steps">
    <li><span>Pick your cheeses</span>Local and international — a proper case, cut to order, from sharp aged wheels to soft bloomy rounds.</li>
    <li><span>Pick your cured meats</span>Salumi and charcuterie by the slice — the center of every good board.</li>
    <li><span>Pick the accouterments</span>Crackers, olives, and whatever the case has that week — the figs, cornichons, sugared fruit and rosemary that make a board look like a still-life.</li>
    <li><span>Pick your size</span>From a single-serving box to multi-serving boards for a crowd.</li>
  </ol>
  <h2>Grab-and-go, very quick</h2>
  <p>&#8220;The idea is that it&#8217;s grab-and-go, very quick,&#8221; founder Kaleigh Bernier says. &#8220;They&#8217;re having a picnic, they want something to eat in the park, they&#8217;re going out on a boat, they can come in and grab something that&#8217;s delicious, beautiful, healthy.&#8221; Downtown Northport is built for exactly that — Main Street runs downhill to the village dock, and the box is made to travel.</p>
  <h2>And if you just want to shop</h2>
  <p>The retail side carries the same goods a la carte: cut cheese, charcuterie, crackers, salumi, olives and specialty items — build a board at home or add to one you grabbed at the counter.</p>
  <p class="cta-row"><a class="btn" href="/contact">Get the opening-day email</a> <a href="/boards-for-events">Need a big board? Go here &rarr;</a></p>
</article>''')

# ---------------- BOARDS & EVENTS DETAIL ----------------
pages["boards-for-events.html"] = (
    head("Holiday Boards, Custom Boards & Grazing Tables — RIND, Northport & Long Island NY",
         "Preorder larger charcuterie boards for holidays and special events from RIND in Northport NY, plus custom boards and grazing tables for weddings, parties and dockside celebrations.",
         "/boards-for-events",
         [breadcrumb("Boards & events", "/boards-for-events"),
          service_node("Holiday board preorders, custom boards and grazing tables", "Event charcuterie and catering boards",
                       "Preordered charcuterie boards for holidays and events, custom boards and grazing tables served across Northport and Long Island, from the Thompson Building shop by the founder of Block Island Charcuterie.",
                       "/boards-for-events")])
    + nav("/boards-for-events")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; <a href="/the-concept">Story &amp; concept</a> &middot; Boards &amp; events</p>
  <p class="lab mono">Boards &middot; events</p>
  <h1>The big boards, preorder line</h1>
  <p class="lede">Not everything fits in a grab-and-go box. RIND takes preorders for larger charcuterie boards for holidays and special events — order ahead, pick up, walk out with the party handled.</p>
  <h2>Custom boards &amp; grazing tables</h2>
  <p>For the bigger celebrations — weddings, showers, company parties, dockside gatherings — founder Kaleigh Bernier builds custom boards and full grazing tables, the same formats she built for weddings and private events on Block Island. The boards are curated, not assembled: cheeses and cured meats chosen for the crowd, accouterments arranged to be eaten, not admired.</p>
  <h2>Northport-sized occasions</h2>
  <p>The shop was sited for how this town eats: yacht-club get-togethers, tailgates on the water, Thanksgiving tables and holiday parties. Plans in the works include pairings with downtown neighbors — Sand City Brewing, a few blocks up Main Street — for food-and-drink events once the doors are open.</p>
  <ul class="spread">
    <li><span>Holiday boards</span>Preorder for Thanksgiving, the winter holidays and every gifting occasion between</li>
    <li><span>Event boards</span>Bigger formats for parties and gatherings, made to your picks</li>
    <li><span>Grazing tables</span>Full curated displays for weddings and large celebrations</li>
    <li><span>Island crossover</span>Block Island events? The same maker still runs the seasonal island business</li>
  </ul>
  <p>Event inquiries go through the form and land in the shop&#8217;s inbox: <a href="https://www.blockislandcharcuterie.com/">Block Island Charcuterie</a> handles the island-side weddings and parties on its own site.</p>
  <p class="cta-row"><a class="btn" href="/contact">Ask about an event</a> <a href="/build-your-own">Counter line &rarr;</a></p>
</article>''')

# ---------------- VISIT ----------------
pages["visit.html"] = (
    head("Visit — The Thompson Building, 24 Woodbine Ave, Northport NY 11768",
         "RIND by Block Island Charcuterie opens soon in the historic Thompson Building at 24 Woodbine Avenue, entrance on Scudder Avenue, downtown Northport NY — a short walk from Main Street and the village dock.",
         "/visit",
         [breadcrumb("Visit", "/visit"),
          service_node("Visit RIND in downtown Northport", "Retail storefront",
                       "Build-your-own charcuterie shop in the Thompson Building, 24 Woodbine Avenue with entrance on Scudder Avenue, Northport NY 11768, opening late 2026.",
                       "/visit")])
    + nav("/visit")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Visit</p>
  <h1>The Thompson Building</h1>
  <p class="lede">Downtown Northport, between Woodbine and Scudder Avenues — the door is on Scudder. Built for a printing house in 1889; now home to a cheese shop. The exact opening day posts here first.</p>
  <div class="visit-grid">
    <div class="board wax-paprika">
      <p class="lab mono">Address</p>
      <p class="addr">%s</p>
      <p>Entrance on Scudder Avenue &middot; a short walk from Main Street and the village dock at Cow Harbor Park.</p>
      <p><a href="%s">Get directions &nearr;</a></p>
      <p class="lab mono">Opening</p>
      <p>Around Thanksgiving 2026. The day, the hours and the board list post on this site first — the <a href="/contact">opening-day list</a> gets the email before anyone else.</p>
    </div>
    <div class="map-tall"><iframe src="%s" loading="lazy" title="Map of RIND by Block Island Charcuterie at 24 Woodbine Avenue, Northport NY" allow="management:coordinate"></iframe><p class="mapcap">24 Woodbine Ave, entrance on Scudder Ave &middot; Northport village</p></div>
  </div>
  <h2>The room itself is the story</h2>
  <p>The Thompson Building went up in 1889 for the Edward Thompson Co., the publishing house that put Northport on the map: enormous volumes of the American and English Encyclopedia of Law came off presses in this building until 1935, shipped all over the world. It spent the 1950s making seat belts, sat empty for a decade, and came back restored — with the original beams, brick and ironwork kept, and tenants held to the preserved surfaces.</p>
  <p>Other downtown neighbors in the building include a designer and a clothing brand; the cheese counter is the first food shop. And when the board is in hand, the walk is the point: Main Street leads down to Cow Harbor Park and the village dock, which is exactly where a build-your-own box is headed.</p>
</article>''' % (ADDR, DIRS, MAP_Q))

# ---------------- CONTACT ----------------
pages["contact.html"] = (
    head("Opening-Day List & Contact — RIND by Block Island Charcuterie, Northport NY",
         "Join the opening-day list for RIND in Northport NY: leave your email and the first word about the opening day, hours and boards comes to you. Questions welcome.",
         "/contact",
         [breadcrumb("Contact", "/contact"),
          service_node("Opening-day list and contact", "Customer contact",
                       "Leave your email to hear first when RIND by Block Island Charcuterie opens in the Thompson Building, 24 Woodbine Avenue, Northport NY 11768.",
                       "/contact")])
    + nav("/contact")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Contact</p>
  <p class="lab mono">Opening-day list</p>
  <h1>Be first through the door</h1>
  <p class="lede">Leave your email. When the opening day is set, the first word goes to this list: the day, the hours, the board list. And if something specific is going on your ideal board — a cheese you hunt for, a party you&#8217;re planning — say so here.</p>
  <form class="cform" method="post" action="/contact">
    <p><label for="f-name">Name</label><input id="f-name" name="name" type="text" maxlength="120" required></p>
    <p><label for="f-email">Email <span class="fine">so we can tell you when we open</span></label><input id="f-email" name="email" type="email" maxlength="120" required></p>
    <p><label for="f-msg">Questions, event inquiries, or a cheese you want in the case? <span class="fine">(optional)</span></label><textarea id="f-msg" name="message" rows="4" maxlength="4000"></textarea></p>
    <p><button class="btn" type="submit">Send it</button></p>
  </form>
  <div class="board wax-sage">
    <p class="lab mono">Email us direct</p>
    <p class="addr"><a href="mailto:%s">%s</a></p>
    <p>The shop&#8217;s inbox — the same team that runs <a href="https://www.blockislandcharcuterie.com/">Block Island Charcuterie</a> on the island.</p>
  </div>
  <div class="map-tall"><iframe src="%s" loading="lazy" title="Map: 24 Woodbine Avenue, Northport NY — RIND by Block Island Charcuterie" allow="management:coordinate"></iframe><p class="mapcap">Thompson Building &middot; 24 Woodbine Ave, entrance on Scudder Ave &middot; <a href="%s">Get directions &nearr;</a></p></div>
</article>''' % (EMAIL, EMAIL, MAP_Q, DIRS))

# ---------------- PRIVACY ----------------
pages["privacy.html"] = (
    head("Privacy — RIND by Block Island Charcuterie, Northport NY",
         "How this site handles what you send it: contact-form messages go to the shop's inbox and are used only to answer you and the opening-day announcements. No cookies, no trackers.",
         "/privacy",
         [breadcrumb("Privacy", "/privacy"), store_node("/privacy")])
    + nav("/privacy")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Privacy</p>
  <h1>What you send us</h1>
  <p>Messages from this site&#8217;s form go straight to the shop&#8217;s inbox — the name, email and note you type, nothing more. We use them to answer you and to send the opening-day announcement to people who asked for it. We do not sell, rent or trade your details.</p>
  <p>This site sets no cookies and runs no advertising or analytics trackers. Pages load from our own host with our own stylesheet; there is no third-party script on any page.</p>
  <p>Questions about this page? <a href="/contact">Use the form</a> and ask.</p>
</article>''')

# ---------------- 404 / THANKS (utility) ----------------
pages["404.html"] = (
    head("Page not found — RIND, Northport NY",
         "That page is off the board. RIND by Block Island Charcuterie opens soon in the Thompson Building in downtown Northport, Long Island.",
         "/404", utility=True)
    + nav("")
    + '''<article class="page">
  <p class="lab mono">404</p>
  <h1>That page is off the board</h1>
  <p class="lede">No cheese was harmed. The two pages that matter are below.</p>
  <p class="cta-row"><a class="btn" href="/">Back to the front</a> <a href="/contact">Join the opening-day list</a></p>
</article>''')

pages["thanks.html"] = (
    head("You're on the list — RIND, Northport NY",
         "Thanks — RIND by Block Island Charcuterie will email you first when the doors open in the Thompson Building, downtown Northport, Long Island.",
         "/thanks", utility=True)
    + nav("")
    + '''<article class="page">
  <p class="lab mono">Received</p>
  <h1>You&#8217;re on the list</h1>
  <p class="lede">When the opening day is set, this list hears it first: the day, the hours, the board list. Keep an eye on your inbox.</p>
  <p class="cta-row"><a class="btn" href="/">Back to the site</a></p>
</article>''')

# ---------------- CSS ----------------
CSS = """:root{
  --ink:#241c14; --roast:#3a2c1d; --rind:#c05a2c; --rind-dk:#8f3c18;
  --gold:#dfa443; --sage:#5d6b45; --bone:#f6f0e2; --paper:#fdf9f0;
  --cream:#f8f2e4; --soft:#eadfbe; --rule:#453423; --dim:#8b7b66;
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{color-scheme:light}
body{background:var(--paper);color:var(--ink);font-family:var(--serif);font-size:17px;line-height:1.6}
.topline{height:8px;background:linear-gradient(90deg,var(--rind-dk),var(--rind) 40%,var(--gold) 75%,var(--sage))}
.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:var(--cream);padding:.5rem 1rem;z-index:9}
.skip:focus{left:1rem;top:1rem}
a{color:var(--rind-dk)}
a:hover{color:var(--roast)}
.mono{font-family:var(--mono)}
header.site{padding:1rem max(1.1rem, calc((100vw - 1012px)/2));border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:.6rem 1.5rem;align-items:center;justify-content:space-between}
.brand{font-size:13px;margin:0;display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.brand a{color:var(--ink);text-decoration:none;display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.wordmark{font-weight:700;font-size:1.35rem;letter-spacing:.28em;text-transform:uppercase}
.brand em{font-style:normal;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--rind-dk)}
header.site nav p{display:flex;flex-wrap:wrap;gap:.35rem 1.1rem;justify-content:flex-end;margin:0}
header.site nav a{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--rule)}
header.site nav a:hover{color:var(--rind-dk);text-decoration:underline;text-underline-offset:4px}
header.site nav a[aria-current="page"]{color:var(--rind-dk);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
main{max-width:1060px;margin:0 auto;padding:0 1.5rem 3.5rem}
.lab{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--rind-dk);margin-bottom:.6rem}
.hero{background:var(--ink);color:var(--cream);margin:1.5rem 0;padding:clamp(2rem,5.5vw,4rem) clamp(1.2rem,4vw,3.5rem);display:grid;grid-template-columns:minmax(0,1.15fr) minmax(240px,.85fr);gap:2rem 2.5rem;align-items:center;border-radius:16px}
.hero .lab{color:var(--gold)}
.hero h1.mark{font-size:clamp(4.2rem,13vw,7rem);line-height:.95;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin:.1rem 0 0}
.mark-sub{font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--soft);margin:.7rem 0 1rem}
.hero .sub{max-width:34rem;color:var(--cream);font-size:1.05rem;line-height:1.55;margin-bottom:1.4rem}
.hero-cta{display:flex;flex-wrap:wrap;gap:.8rem 1.2rem;align-items:center}
.board-art{width:100%;height:auto;display:block;border-radius:16px}
.btn{display:inline-block;background:var(--rind);color:#fff;font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;padding:.8rem 1.3rem;border-radius:8px;border:1px solid var(--roast)}
.btn:hover{background:var(--rind-dk);color:#fff}
.btn.sm{padding:.45rem .8rem;font-size:11px}
a.ghost{color:var(--gold);font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;text-decoration:underline;text-underline-offset:5px}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.2rem;margin:1.6rem 0 2.2rem}
.panels>.board{height:100%}
.board{background:#fff;border:1px solid var(--rule);border-top:5px solid var(--rind);border-radius:4px 4px 14px 14px;padding:1.6rem 1.4rem 1.4rem;display:flex;flex-direction:column}
.board.wax-sage{border-top-color:var(--sage)}
.board.wax-gold{border-top-color:var(--gold)}
.board h2{font-size:1.3rem;line-height:1.2;margin-bottom:.5rem}
.board p{margin-bottom:.7rem}
.board p:last-child{margin-bottom:0;margin-top:auto}
.band{display:grid;grid-template-columns:minmax(300px,1.25fr) minmax(280px,1fr);gap:1.4rem;align-items:center;background:var(--bone);border:1px solid var(--rule);border-radius:16px;padding:1.6rem}
.band h2{font-size:1.6rem;margin-bottom:.4rem}
.band-map{width:100%}
.band-map iframe,.map-tall iframe{width:100%;aspect-ratio:4/3;border:1px solid var(--rule);border-radius:10px;display:block;background:var(--bone)}
.mapcap{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);text-align:center;margin-top:.5rem}
.page{padding-top:1.8rem}
.crumbs{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-bottom:1rem}
h1{font-size:clamp(1.9rem,4.5vw,2.9rem);line-height:1.1;margin-bottom:.8rem}
.lede{font-size:1.15rem;line-height:1.55;max-width:44rem;margin-bottom:1.4rem;color:var(--rule)}
.page h2{font-size:1.35rem;margin:1.6rem 0 .5rem}
.page p{max-width:46rem;margin-bottom:1rem}
ol.steps{list-style:none;counter-reset:step;margin:0 0 1.4rem;border-top:1px solid var(--rule);max-width:46rem}
ol.steps li{counter-increment:step;display:grid;grid-template-columns:44px minmax(0,1fr);gap:0 1rem;padding:.8rem 0;border-bottom:1px solid var(--rule);font-size:.98rem}
ol.steps li::before{content:counter(step,decimal-leading-zero);font-family:var(--mono);font-size:1.05rem;color:var(--rind-dk);border-right:3px solid var(--gold);padding-right:.6rem}
ol.steps li span{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--roast);margin-bottom:.2rem}
ul.spread{list-style:none;margin:0 0 1.2rem;border-top:1px solid var(--rule);max-width:46rem}
ul.spread li{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:.5rem 1.4rem;padding:.65rem 0;border-bottom:1px solid var(--rule);font-size:.98rem}
ul.spread li span{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--rind-dk);padding-top:.15rem}
dl.faq{margin:1.6rem 0;border-top:1px solid var(--rule)}
dl.faq dt{font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--rind-dk);padding:.9rem 0 .2rem}
dl.faq dd{padding:0 0 1rem;border-bottom:1px solid var(--rule);max-width:46rem}
ul.press{list-style:none;margin:0 0 1.2rem}
ul.press li{padding:.5rem 0;border-bottom:1px solid var(--rule)}
.cta-row{display:flex;flex-wrap:wrap;gap:.8rem 1.2rem;align-items:center;margin-top:1.4rem}
.addr{font-family:var(--mono);font-size:14px;letter-spacing:.04em;margin-bottom:.6rem;max-width:46rem}
.visit-grid{display:grid;grid-template-columns:minmax(280px,1fr) minmax(280px,1.2fr);gap:1.4rem;align-items:start;margin-bottom:1.6rem}
.map-tall{width:100%}
.cform{max-width:34rem;margin:0 0 1.8rem}
.cform p{margin-bottom:1rem}
.cform label{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--rule);margin-bottom:.35rem}
.fine{color:var(--dim);text-transform:none;letter-spacing:.02em}
.cform input,.cform textarea{width:100%;font-family:var(--serif);font-size:16px;padding:.65rem .8rem;border:1px solid var(--rule);border-radius:8px;background:#fff;color:var(--ink)}
.cform input:focus,.cform textarea:focus{outline:2px solid var(--rind);outline-offset:1px}
footer{background:var(--ink);color:var(--cream);padding:1.8rem 1.5rem;text-align:center}
footer p.footline{font-family:var(--mono);font-size:12px;letter-spacing:.08em;line-height:1.9;max-width:none;margin:0 auto}
footer a{color:var(--gold)}
footer p.fine{color:#d8c3a5;font-size:11px}
@media (max-width:640px){
  body{font-size:16px}
  header.site nav p{justify-content:flex-start}
  .hero{grid-template-columns:1fr;padding:2rem 1.1rem}
  .band,.visit-grid{grid-template-columns:1fr}
  ul.spread li{grid-template-columns:1fr;gap:.2rem}
  main{padding:0 1.1rem 3rem}
}"""

def write(name, content):
    with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as f:
        f.write(content if content.endswith("\n") else content + "\n")

os.makedirs(PUBLIC, exist_ok=True)
for name, content in pages.items():
    write(name, content + FOOTER)
write("style.css", CSS)

core = ["index.html", "the-concept.html", "build-your-own.html", "boards-for-events.html",
        "visit.html", "contact.html", "privacy.html"]
today = "2026-11-25"
locs = "\n".join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' %
                 (ORIGIN, "/" if f == "index.html" else "/" + f[:-5], today) for f in core)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % locs)
write("robots.txt", "User-agent: *\nDisallow:\n\nSitemap: %s/sitemap.xml\n" % ORIGIN)
# static assets that live at repo root must ride into public/ (server serves public/ only)
import shutil
for asset in ("pixel.gif", "favicon.svg"):
    src = os.path.join(HERE, asset)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(PUBLIC, asset))
print("built %d pages + css + sitemap + robots" % len(pages))
