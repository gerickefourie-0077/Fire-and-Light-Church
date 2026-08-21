#!/usr/bin/env python3
"""Fire & Light Stellenbosch — static site generator.

Emits plain, dependency-free HTML. Run `python3 _build.py` from the project
root after editing content below. The generated .html files are the
deliverable; this script only exists to keep the shared shell consistent.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

SITE = "https://fireandlight.co.za"
EMAIL = "info@fireandlight.co.za"
WA_NUMBER = "27828722036"
WA_TEXT = "Hi%20Fire%20%26%20Light%2C%20I%27d%20like%20to%20find%20out%20more."
WA = f"https://wa.me/{WA_NUMBER}?text={WA_TEXT}"

YT_CHANNEL_ID = "UCdKWohKcSp-YRycCB6vAWLw"
YT_UPLOADS = "UU" + YT_CHANNEL_ID[2:]          # uploads playlist = channel id, UC -> UU
YT_URL = "https://www.youtube.com/@FireLightStellenbosch"
FB_URL = "https://www.facebook.com/FireandLightStellenbosch"
IG_URL = "https://www.instagram.com/fireandlightstellenbosch"
SPOTIFY_SHOW = "35pGlAxb1WEI8qnWjEBOoq"
SPOTIFY_URL = f"https://open.spotify.com/show/{SPOTIFY_SHOW}"
MAPS_URL = "https://maps.app.goo.gl/iU2yoU8QisaxYmEC7"

# ---------------------------------------------------------------- icons ----

ICONS = {
    "facebook": '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/>',
    "instagram": '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 01-1.38-.9 3.7 3.7 0 01-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07M12 0C8.74 0 8.33.01 7.05.07c-1.28.06-2.15.26-2.91.56-.79.31-1.46.72-2.13 1.38A5.9 5.9 0 00.63 4.14c-.3.76-.5 1.63-.56 2.91C.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.28.26 2.15.56 2.91.31.79.72 1.46 1.38 2.13a5.9 5.9 0 002.13 1.38c.76.3 1.63.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.28-.06 2.15-.26 2.91-.56a5.9 5.9 0 002.13-1.38 5.9 5.9 0 001.38-2.13c.3-.76.5-1.63.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.28-.26-2.15-.56-2.91a5.9 5.9 0 00-1.38-2.13A5.9 5.9 0 0019.86.63c-.76-.3-1.63-.5-2.91-.56C15.67.01 15.26 0 12 0z"/><path d="M12 5.84A6.16 6.16 0 1018.16 12 6.16 6.16 0 0012 5.84zM12 16a4 4 0 114-4 4 4 0 01-4 4z"/><circle cx="18.41" cy="5.59" r="1.44"/>',
    "youtube": '<path d="M23.5 6.19a3.02 3.02 0 00-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 00.5 6.19C0 8.08 0 12 0 12s0 3.92.5 5.81a3.02 3.02 0 002.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 002.12-2.14C24 15.92 24 12 24 12s0-3.92-.5-5.81zM9.55 15.57V8.43L15.82 12z"/>',
    "spotify": '<path d="M12 0a12 12 0 100 24 12 12 0 000-24zm5.5 17.32a.75.75 0 01-1.03.25c-2.82-1.73-6.37-2.12-10.55-1.16a.75.75 0 11-.33-1.46c4.57-1.05 8.5-.6 11.66 1.34.35.22.46.68.25 1.03zm1.47-3.27a.94.94 0 01-1.29.31c-3.23-1.98-8.15-2.56-11.97-1.4a.94.94 0 11-.54-1.79c4.36-1.32 9.78-.68 13.49 1.6.44.27.58.85.31 1.28zm.13-3.4C15.23 8.35 8.9 8.14 5.2 9.26a1.12 1.12 0 11-.65-2.15C8.8 5.82 15.79 6.07 20.2 8.69a1.12 1.12 0 11-1.14 1.93z"/>',
    "whatsapp": '<path d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/><path d="M12.04 0h-.01C5.4 0 .02 5.38.02 12.02a11.9 11.9 0 001.64 6.04L.06 24l6.1-1.6a11.94 11.94 0 005.88 1.53c6.63 0 12.01-5.38 12.01-12.02S18.67 0 12.04 0zm6.99 16.96c-.29.82-1.44 1.5-2.36 1.7-.63.13-1.45.24-4.22-.9-2.95-1.22-4.85-4.22-5-4.41-.14-.2-1.19-1.59-1.19-3.03s.73-2.14 1.02-2.44c.24-.24.63-.35 1-.35h.3c.29.01.43.03.62.48.24.56.81 2 .88 2.14.07.14.14.34.04.53-.09.2-.17.29-.31.46-.14.16-.28.29-.42.47-.13.15-.28.32-.12.6.16.28.72 1.19 1.55 1.93 1.07.95 1.94 1.26 2.26 1.39.24.1.52.08.7-.11.22-.24.5-.65.78-1.05.2-.28.45-.32.72-.22.27.1 1.7.8 2 .95.29.14.48.21.55.33.07.13.07.73-.22 1.55z"/>',
    "mail": '<path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4.24-8 4.76-8-4.76V6l8 4.75L20 6z"/>',
    "pin": '<path d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1114.5 9 2.5 2.5 0 0112 11.5z"/>',
    "clock": '<path d="M12 2a10 10 0 1010 10A10 10 0 0012 2zm1 10.59V6h-2v7.41l4.7 4.7 1.42-1.42z"/>',
    "play": '<path d="M8 5v14l11-7z"/>',
    "heart": '<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54z"/>',
    "users": '<path d="M16 11a4 4 0 10-4-4 4 4 0 004 4zm-8 0a4 4 0 10-4-4 4 4 0 004 4zm0 2c-2.67 0-8 1.34-8 4v3h10v-3c0-1 .36-1.9.97-2.65A14.6 14.6 0 008 13zm8 0c-.35 0-.74.02-1.15.06A4.9 4.9 0 0116 17v3h8v-3c0-2.66-5.33-4-8-4z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
            f'focusable="false">{ICONS[name]}</svg>')



PILLAR_ICONS = {
    "unlock":   '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.287 1.288L3 12l5.8 1.9a2 2 0 0 1 1.288 1.287L12 21l1.9-5.8a2 2 0 0 1 1.287-1.288L21 12l-5.8-1.9a2 2 0 0 1-1.288-1.287Z"/>',
    "flame":    '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "heart":    '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
}


def line_icon(name):
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'{PILLAR_ICONS[name]}</svg>')


# ------------------------------------------------------------ navigation ---

# The visitor journey drives this order: a first-time visitor decides on
# "Visit", everything else is for people who already decided. "Plan your visit"
# is the site's primary CTA in four places, so it needs a real destination —
# it used to land on the contact form, which answered none of its questions.
NAV = [
    ("Home", "index.html", None),
    ("Visit", "visit.html", None),
    ("About", None, [
        ("Our Story", "our-story.html"),
        ("Our Values", "our-values.html"),
        ("What We Believe", "statement-of-faith.html"),
        ("Our Team", "meet-our-team.html"),
    ]),
    ("Sermons", "sermons.html", None),
    ("Kids", "kids-ministry.html", None),
    ("Give", "give.html", None),
    ("Contact", "contact.html", None),
]

CHEV = ('<svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="2.2" '
        'aria-hidden="true"><path d="M1 1.5 6 6.5l5-5"/></svg>')


def url_for(slug):
    """Map a source filename to the URL the site actually serves.

    Cloudflare Workers Static Assets strips `.html` and 307-redirects
    `/contact.html` -> `/contact`. Emitting the served URL directly avoids a
    redirect hop on every internal link and keeps each canonical tag pointing
    at a real 200 rather than at a redirect.
    """
    return "/" if slug == "index.html" else "/" + slug[:-5]


def prettify_urls(html):
    """Rewrite page links and absolute page URLs to their extensionless form.

    Page links become root-relative so they resolve identically from every
    depth. Asset paths are deliberately left relative — the Claude Design
    preview serves the project from a sandbox where a leading slash would
    escape it, and relative asset paths resolve correctly from `/name` anyway.
    """
    html = re.sub(r'href="index\.html(#[^"]*)?"',
                  lambda m: 'href="/%s"' % (m.group(1) or ""), html)
    html = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"',
                  lambda m: 'href="/%s%s"' % (m.group(1), m.group(2) or ""), html)
    html = html.replace(f"{SITE}/index.html", f"{SITE}/")
    html = re.sub(re.escape(SITE) + r'/([a-z0-9-]+)\.html',
                  lambda m: f"{SITE}/" + m.group(1), html)
    return html


def build_nav(current):
    items = []
    for label, href, sub in NAV:
        if sub:
            open_child = any(h == current for _, h in sub)
            links = "".join(
                f'<li><a href="{h}"{aria(h, current)}>{t}</a></li>' for t, h in sub)
            cur = ' style="color:var(--fl-amber)"' if open_child else ""
            items.append(
                f'<li class="fl-nav__item">'
                f'<button class="fl-nav__link fl-nav__toggle" type="button" '
                f'aria-expanded="false"{cur}>{label} {CHEV}</button>'
                f'<ul class="fl-nav__sub">{links}</ul></li>')
        else:
            items.append(
                f'<li class="fl-nav__item">'
                f'<a class="fl-nav__link" href="{href}"{aria(href, current)}>{label}</a></li>')
    return "".join(items)


def aria(href, current):
    return ' aria-current="page"' if href == current else ""


# ---------------------------------------------------------------- shell ----

def social_iconrow():
    return f"""<ul class="fl-iconrow">
        <li><a href="{FB_URL}" target="_blank" rel="noopener" aria-label="Fire &amp; Light on Facebook">{icon('facebook')}</a></li>
        <li><a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Fire &amp; Light on Instagram">{icon('instagram')}</a></li>
        <li><a href="{YT_URL}" target="_blank" rel="noopener" aria-label="Fire &amp; Light on YouTube">{icon('youtube')}</a></li>
        <li><a href="{SPOTIFY_URL}" target="_blank" rel="noopener" aria-label="Fire &amp; Light on Spotify">{icon('spotify')}</a></li>
        <li><a href="{WA}" target="_blank" rel="noopener" aria-label="Message Fire &amp; Light on WhatsApp">{icon('whatsapp')}</a></li>
      </ul>"""


def page(slug, title, description, body, current=None):
    current = current or slug
    nav = build_nav(current)

    # A CTA that links to the page you are already on is a dead control, so on
    # /visit the header offers the next step instead of a self-link.
    if slug == "visit.html":
        header_cta = (f'<a class="fl-btn fl-btn--primary" href="{WA}" target="_blank" '
                      f'rel="noopener">Message us</a>')
    else:
        header_cta = '<a class="fl-btn fl-btn--primary" href="visit.html">Plan your visit</a>'

    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE}{url_for(slug)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fire &amp; Light Stellenbosch">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}{url_for(slug)}">
<meta property="og:image" content="{SITE}/assets/img/share-banner.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fire &amp; Light — Fire within, Light through">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#241F1C">
<link rel="icon" href="assets/img/FL-Logo-Horiz-Whitergb.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="assets/css/fireandlight.css">
<script>document.documentElement.className+=" fl-js";</script>
</head>
<body>

<a class="fl-skip" href="#main">Skip to content</a>

<header class="fl-header">
  <div class="fl-header__bar">
    <a class="fl-header__logo" href="index.html" aria-label="Fire &amp; Light Stellenbosch — home">
      <img src="assets/img/logo-horizontal-white.png" alt="Fire &amp; Light Stellenbosch" width="1200" height="538">
    </a>

    <button class="fl-burger" type="button" aria-expanded="false" aria-controls="fl-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>

    <nav class="fl-nav" id="fl-nav" aria-label="Main">
      <ul class="fl-nav__list">{nav}</ul>
    </nav>

    <div class="fl-header__cta">
      {header_cta}
    </div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="fl-footer">
  <div class="fl-wrap">
    <div class="fl-footer__grid">

      <div>
        <img class="fl-footer__logo" src="assets/img/logo-horizontal-white.png"
             alt="Fire &amp; Light Stellenbosch" width="1200" height="538" loading="lazy">
        <p>Fire within · Light through</p>
        {social_iconrow()}
      </div>

      <div>
        <h2 class="fl-footer__h">We meet</h2>
        <p>PJ Olivier Art School<br>
           3 Blom Street, Stellenbosch<br>
           <strong>Side entrance @ Mark Street</strong></p>
        <p><strong>Sundays 9:30am</strong></p>
      </div>

      <div>
        <h2 class="fl-footer__h">Explore</h2>
        <ul class="fl-footer__list">
          <li><a href="visit.html">Plan your visit</a></li>
          <li><a href="our-story.html">Our Story</a></li>
          <li><a href="our-values.html">Our Values</a></li>
          <li><a href="sermons.html">Sermons</a></li>
          <li><a href="kids-ministry.html">Kids</a></li>
          <li><a href="give.html">Give</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div>
        <h2 class="fl-footer__h">Get in touch</h2>
        <ul class="fl-footer__list">
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp&nbsp;· Message us</a></li>
          <li><a href="{MAPS_URL}" target="_blank" rel="noopener">Find us on the map</a></li>
        </ul>
      </div>

    </div>

    <div class="fl-footer__bottom">
      <p>© 2026 Fire &amp; Light Church Stellenbosch. All rights reserved.</p>
      <p>Formerly Kingdom Light Church</p>
    </div>
  </div>
</footer>

<script src="assets/js/fireandlight.js"></script>
</body>
</html>
"""


def tagline_band():
    return """<section class="fl-tagline-band" aria-label="Fire within, Light through">
  <video class="fl-tagline-band__video" autoplay muted loop playsinline preload="metadata"
         poster="assets/video/tagline-band-poster.jpg" aria-hidden="true">
    <source src="assets/video/tagline-band.mp4" type="video/mp4">
  </video>
  <img class="fl-tagline-band__still" src="assets/img/tagline-white.png"
       alt="Fire within — Light through" width="900" height="518" loading="lazy">
</section>"""

def banner(title, lede=""):
    p = f"<p>{lede}</p>" if lede else ""
    return f"""<section class="fl-banner">
  <div class="fl-wrap">
    <h1>{title}</h1>
    {p}
    <hr class="fl-rule">
  </div>
</section>"""


# ============================================================== content ====

PILLARS = [
    ("Freedom", "unlock",
     "True freedom is found in Jesus! Through His finished work we are set free from sin, shame, "
     "and fear. As His presence and word ignites us, we step fully into our identity and live "
     "bold, Spirit-led lives."),
    ("Worship", "sparkles",
     "Worship is our wholehearted response to God. It’s more than a song, it’s absolute surrender. "
     "We believe that as we host His presence, God changes the atmosphere."),
    ("Revival", "flame",
     "Revival is hearts awakened and lives set ablaze. It starts with personal surrender and "
     "spreads to families, campuses, and cities. As we carry His fire everywhere we go, the light "
     "of the Gospel will change the world!"),
    ("Encounter", "heart",
     "Encounters change everything. When heaven touches earth, chains break and identity is "
     "restored. We pursue His presence with expectation, knowing one moment with Jesus can "
     "redefine a life."),
]

VALUES = [
    ("Word &amp; Faith Based",
     "As a church we are anchored in the Word of God and we walk by faith. Scripture is our "
     "foundation, our authority, and our guide for life and ministry. We do not build on trends or "
     "opinions, we build on the truth of God’s word. We believe faith is active, bold, and "
     "practical. We take God at His Word and live with confident expectation that He will do what "
     "He has said.",
     [("All Scripture is God-breathed and is useful for teaching, rebuking, correcting and training in righteousness.", "2 Timothy 3:16"),
      ("So then faith comes by hearing, and hearing by the word of God.", "Romans 10:17"),
      ("The just shall live by faith.", "Romans 1:17"),
      ("Heaven and earth will pass away, but My words will never pass away.", "Matthew 24:35")]),

    ("Spirit Empowered &amp; Presence Focused",
     "As church we depend fully on the Holy Spirit. We expect His leading, His power, His gifts, "
     "and His fruit to be evident in our lives and gatherings. More than programs or performance, "
     "we prioritize encountering God. His presence is central, not optional. We create space for "
     "Him to move, speak, heal, restore, and transform.",
     [("Not by might nor by power, but by My Spirit, says the Lord Almighty.", "Zechariah 4:6"),
      ("But you will receive power when the Holy Spirit has come upon you.", "Acts 1:8"),
      ("Where the Spirit of the Lord is, there is freedom.", "2 Corinthians 3:17"),
      ("My presence will go with you, and I will give you rest.", "Exodus 33:14")]),

    ("Relationship &amp; Family",
     "We believe church is not something we attend, it’s a family we belong to. We deeply value "
     "both spiritual and natural family, and we intentionally choose honor, unity, and healthy, "
     "life-giving communication. We believe spiritual growth happens best in the context of "
     "strong, godly relationships. We carry one another’s burdens, celebrate victories together, "
     "and build a culture of belonging across generations.",
     [("By this everyone will know that you are My disciples, if you love one another.", "John 13:35"),
      ("They devoted themselves to the apostles’ teaching and to fellowship…", "Acts 2:42"),
      ("Carry each other’s burdens, and in this way you will fulfill the law of Christ.", "Galatians 6:2"),
      ("How good and pleasant it is when God’s people live together in unity.", "Psalm 133:1")]),

    ("Build &amp; Equip People",
     "We are committed to developing people into who God has called them to be. Our goal is not "
     "just attendance, but transformation. Not just gathering people, but equipping them. We "
     "invest in leadership, discipleship, and personal growth. We help people to discover their "
     "gifts, strengthen their character, and to step confidently into their calling.",
     [("To equip His people for works of service, so that the body of Christ may be built up.", "Ephesians 4:12"),
      ("And the things you have heard… entrust to reliable people who will also be qualified to teach others.", "2 Timothy 2:2"),
      ("We proclaim Him… so that we may present everyone fully mature in Christ.", "Colossians 1:28"),
      ("As each has received a gift, use it to serve one another.", "1 Peter 4:10")]),

    ("Worship &amp; Prayer",
     "Worship and prayer are the heartbeat of our church. We minister to the Lord first and live "
     "from a place of intimacy with Him. Through passionate worship and consistent prayer, we "
     "align our hearts with heaven and partner with God’s kingdom on earth.",
     [("God is spirit, and His worshipers must worship in the Spirit and in truth.", "John 4:24"),
      ("Devote yourselves to prayer, being watchful and thankful.", "Colossians 4:2"),
      ("Pray without ceasing.", "1 Thessalonians 5:17"),
      ("Enter His gates with thanksgiving and His courts with praise.", "Psalm 100:4")]),
]

BELIEFS = [
    ("The Triune God",
     "We believe in one true and eternal God, the Creator, Sustainer, and Redeemer of all things. "
     "He exists in three persons: God the Father, God the Son, and God the Holy Spirit—distinct in "
     "person, but unified in essence. He is holy, just, loving, and true, and is worthy of all "
     "worship, obedience, and adoration."),
    ("The Scriptures",
     "We believe the Bible, consisting of the sixty-six canonical books of the Old and New "
     "Testaments, is the inspired, infallible, and authoritative Word of God. It is the final and "
     "trustworthy foundation for all faith, life, doctrine, and practice."),
    ("Creation, Humanity, and the Fall",
     "We believe God created all things out of nothing, declaring them good. Humans were made in "
     "God’s image—to know, enjoy, and glorify Him. Yet through sin, humanity fell from this "
     "position, becoming separated from God and subject to spiritual death and the effects of sin "
     "in the world. All are in need of salvation and cannot save themselves."),
    ("Jesus Christ, Our Redeemer",
     "We believe in the Lord Jesus Christ—the eternal Son of God, born of the virgin Mary, fully "
     "God and fully man. He lived a sinless life, was crucified for our sins, died, was buried, "
     "rose again on the third day, and ascended into heaven. He is now exalted at the right hand "
     "of the Father and will return in glory. Through Him alone is salvation made possible."),
    ("Salvation by Grace Through Faith",
     "We believe that salvation is the free gift of God, offered by grace and received through "
     "faith in Jesus Christ. We are justified, regenerated, adopted, and sanctified through the "
     "work of the Holy Spirit. This salvation is not by works but is entirely dependent on God’s "
     "mercy and Christ’s finished work."),
    ("The Holy Spirit and Empowered Living",
     "We believe in the indwelling presence and ongoing ministry of the Holy Spirit, who empowers "
     "believers for holy living, spiritual growth, and supernatural ministry that include signs, "
     "wonders and miracles. We believe in the baptism of the Holy Spirit, which is accompanied by "
     "speaking in tongues as a sign, and empowers believers for bold witness and effective "
     "ministry."),
    ("The Church and Its Mission",
     "We believe the Church is the body of Christ made up of all believers. The local church "
     "exists to glorify God, disciple nations, preach the Gospel, and undo the works of the enemy. "
     "We are called to build Christ’s Kingdom in every sphere of society, bringing light into "
     "darkness and life to the lost."),
    ("Believer’s Baptism &amp; Communion",
     "We affirm baptism and communion as ordinances instituted by Christ. Baptism is the outward "
     "testimony of an inward transformation, signifying identification with the death, burial, and "
     "resurrection of Christ. Communion is a sacred act of remembrance and celebration of Christ’s "
     "sacrifice."),
    ("Sanctity of Life, Marriage, and Gender",
     "We believe all human life is sacred and made in the image of God—from conception to natural "
     "death. Marriage is a holy covenant between one man and one woman. We affirm the God-given "
     "identity of male and female and the equal dignity and worth of every person."),
    ("The Return of Christ",
     "We believe in the literal, visible, and glorious return of Jesus Christ. He will judge the "
     "living and the dead, reward the righteous, and restore all creation. Those in Christ will "
     "live eternally with Him; those who reject Him will face eternal separation."),
]


def pillars_html():
    out = []
    for name, ic, text in PILLARS:
        out.append(f"""<article class="fl-pillar fl-reveal">
        <div class="fl-pillar__tablet">{line_icon(ic)}</div>
        <h2>{name}</h2>
        <p>{text}</p>
      </article>""")
    return "\n".join(out)


def player_html():
    return f"""<div class="fl-player">
        <iframe src="https://www.youtube.com/embed/videoseries?list={YT_UPLOADS}&amp;rel=0"
                title="Latest sermon — Fire &amp; Light Stellenbosch"
                loading="lazy" allowfullscreen
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"></iframe>
      </div>"""


# ================================================================ pages ====

PAGES = {}

# ------------------------------------------------------------------ home ---

PAGES["index.html"] = dict(
    title="Fire &amp; Light Stellenbosch | Fire Within — Light Through",
    description=("A Spirit-empowered church in Stellenbosch. We gather Sundays 9:30am at PJ "
                 "Olivier Art School, Mark Street side entrance. Formerly Kingdom Light Church."),
    body=f"""
<section class="fl-hero">
  <div class="fl-hero__media">
    <img src="assets/img/home-page-image-overlay@2x-scaled.webp"
         alt="The Stellenbosch mountains at sunset" width="2560" height="1717" fetchpriority="high">
  </div>

  <div class="fl-hero__inner">
    <h1 class="fl-vh">Fire &amp; Light Stellenbosch — a Spirit-empowered church in Stellenbosch</h1>
    <div class="fl-hero__markwrap" role="img" aria-label="Fire &amp; Light">
      <video class="fl-hero__markvideo" autoplay muted playsinline preload="auto"
             poster="assets/video/intro-poster.jpg" aria-hidden="true">
        <source src="assets/video/intro.mp4" type="video/mp4">
      </video>
      <img class="fl-hero__mark" src="assets/img/logo-horizontal-white.png"
           alt="" aria-hidden="true" width="1200" height="538" fetchpriority="high">
    </div>
  </div>
</section>

<!-- Service details lifted out of the hero into their own full-width strip.
     Amber UI per the brand card; square, like the announcement bar. -->
<section class="fl-servicebar" aria-label="Service times and location">
  <div class="fl-wrap fl-servicebar__inner">
    <div class="fl-servicebar__when">
      <span class="fl-servicebar__k">Sundays</span>
      <strong class="fl-servicebar__time">9:30am</strong>
    </div>
    <div class="fl-servicebar__where">
      <p><strong>P.J. Olivier Art School</strong> · 3 Blom Street, Stellenbosch</p>
      <p>Use the <strong>side entrance @ Mark Street</strong></p>
    </div>
    <div class="fl-btn-row fl-servicebar__do">
      <a class="fl-btn fl-btn--ink" href="visit.html">Plan your visit</a>
      <a class="fl-btn fl-btn--ink-ghost" href="sermons.html">{icon('play')} Latest sermon</a>
    </div>
  </div>
</section>

<section class="fl-notice" id="notice">
  <div class="fl-wrap">
    <h2>We have changed our name and look.</h2>
    <p>Kingdom Light Church is now Fire &amp; Light — same heart, same love.</p>
  </div>
</section>

<section class="fl-section fl-section--warm" id="welcome">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">Welcome</span>
        <h2>This is who we are</h2>
        <hr class="fl-rule">
        <p>Fire &amp; Light Stellenbosch exists to see Stellenbosch and the nations transformed by
           the fire of God’s presence and the light of Jesus Christ — bringing life, truth, and
           freedom.</p>
        <p>We are a Spirit-empowered church with a passion to host God’s presence and create space
           for real encounters with Him. We believe transformation happens when people experience
           Jesus personally, grow deeply in their faith, and are equipped to live out their calling.</p>
        <div class="fl-btn-row" style="margin-top:1.75rem">
          <a class="fl-btn fl-btn--gradient" href="our-story.html">Our story</a>
          <a class="fl-btn fl-btn--ghost" href="meet-our-team.html">Meet the team</a>
        </div>
      </div>
      <div class="fl-split__media fl-reveal">
        <img src="assets/img/Hennie-Salomie.jpg" alt="Hennie and Salomie Botha, senior leaders"
             width="1400" height="934" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="fl-section fl-section--ink" id="latest">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">Latest message</span>
        <h2>Catch up on Sunday</h2>
        <hr class="fl-rule">
        <p>Missed a service, or want to hear it again? The newest message loads here
           automatically, straight from our YouTube channel.</p>
        <div class="fl-btn-row" style="margin-top:1.75rem">
          <a class="fl-btn fl-btn--gradient" href="sermons.html">All sermons</a>
          <a class="fl-btn fl-btn--light" href="{SPOTIFY_URL}" target="_blank" rel="noopener">
            {icon('spotify')} Listen on Spotify</a>
        </div>
      </div>
      <div class="fl-reveal">
        {player_html()}
      </div>
    </div>
  </div>
</section>

<section class="fl-section fl-section--warm" id="pillars">
  <div class="fl-wrap">
    <div class="fl-center" style="max-width:60ch;margin-inline:auto">
      <span class="fl-eyebrow">What we carry</span>
      <h2>Fire within. Light through.</h2>
      <hr class="fl-rule">
      <p class="fl-lead">Four things shape everything we do as a church family.</p>
    </div>
    <div class="fl-grid fl-grid--pillars" style="margin-top:clamp(2.5rem,5vw,3.5rem)">
      {pillars_html()}
    </div>
  </div>
</section>

<section class="fl-section" id="next-steps">
  <div class="fl-wrap">
    <div class="fl-grid fl-grid--3">

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('users')}</div>
        <h3>Bright Sparks</h3>
        <p>Family is a core value for us, and our kids are a real part of Sunday mornings — not an
           afterthought.</p>
        <p style="margin-top:1rem"><a href="kids-ministry.html">Kids Ministry →</a></p>
      </article>

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('heart')}</div>
        <h3>Give</h3>
        <p>Partner with what God is doing in Stellenbosch through your giving, your time, or your
           prayers.</p>
        <p style="margin-top:1rem"><a href="give.html">Ways to give →</a></p>
      </article>

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('whatsapp')}</div>
        <h3>Talk to us</h3>
        <p>Questions, prayer requests, or just want to know what a Sunday looks like? Send us a
           message.</p>
        <p style="margin-top:1rem"><a href="{WA}" target="_blank" rel="noopener">WhatsApp us →</a></p>
      </article>

    </div>
  </div>
</section>

<section class="fl-section fl-section--tight fl-cta-band">
  <div class="fl-wrap">
    <h2>Come as you are</h2>
    <p>We’d love to meet you this Sunday at 9:30am. Use the side entrance in Mark Street — there’ll
       be someone at the door to point you the right way.</p>
    <div class="fl-btn-row" style="margin-top:1.75rem">
      <a class="fl-btn fl-btn--light" href="visit.html">Plan your visit</a>
      <a class="fl-btn fl-btn--light" href="{MAPS_URL}" target="_blank" rel="noopener">Get directions</a>
    </div>
  </div>
</section>
""")

# ----------------------------------------------------------------- visit ---
# The destination for the site's primary CTA. Everything here is drawn from
# facts the site already stated (service time, address, side entrance, kids in
# the same service); nothing about parking, service length or dress is claimed,
# because none of that was ever established. See README for the content gaps.

PAGES["visit.html"] = dict(
    title="Plan Your Visit | Fire &amp; Light Stellenbosch",
    description=("Everything you need for a first visit to Fire & Light Stellenbosch. Sundays "
                 "9:30am at P.J. Olivier Art School, 3 Blom Street — side entrance in Mark Street."),
    body=f"""
{banner("Plan your visit",
        "Sundays at 9:30am. Come as you are — here is everything you need to find us.")}

<section class="fl-section">
  <div class="fl-wrap">
    <div class="fl-split">

      <div class="fl-reveal">
        <span class="fl-eyebrow">The essentials</span>
        <h2>When and where</h2>
        <hr class="fl-rule">

        <ul class="fl-info">
          <li>
            <span class="fl-info__icon">{icon('clock')}</span>
            <span>
              <span class="fl-info__k">When</span>
              Sunday service &middot; 9:30am
            </span>
          </li>
          <li>
            <span class="fl-info__icon">{icon('pin')}</span>
            <span>
              <span class="fl-info__k">Where</span>
              P.J. Olivier Art School (Kunssentrum)<br>
              3 Blom Street, Stellenbosch<br>
              <strong>Use the side entrance in Mark Street</strong><br>
              <a href="{MAPS_URL}" target="_blank" rel="noopener">Open in Google Maps &rarr;</a>
            </span>
          </li>
          <li>
            <span class="fl-info__icon">{icon('users')}</span>
            <span>
              <span class="fl-info__k">Kids</span>
              Bright Sparks runs in the same service &mdash;
              <a href="kids-ministry.html">more about kids</a>
            </span>
          </li>
        </ul>
      </div>

      <div class="fl-map fl-reveal">
        <iframe title="Map to P.J. Olivier Art School, Stellenbosch" loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                src="https://www.google.com/maps?q=-33.937705,18.858154(P.J.+Olivier+Art+Centre)&amp;z=17&amp;output=embed"></iframe>
      </div>

    </div>
  </div>
</section>

<section class="fl-section fl-section--warm">
  <div class="fl-wrap fl-wrap--narrow fl-reveal">
    <span class="fl-eyebrow">What to expect</span>
    <h2>Come as you are</h2>
    <hr class="fl-rule">
    <p class="fl-lead">There is no dress code and nothing you need to bring. Use the side entrance
       in Mark Street and there will be someone at the door to point you the right way.</p>
    <p>Kids are intentionally part of the worship experience on a Sunday morning — we believe
       families should worship together, so your children stay with you in the service rather than
       being signed in somewhere else.</p>
    <p>If you would rather know what a Sunday looks like before you come, message us and we will
       tell you honestly.</p>
    <div class="fl-btn-row" style="margin-top:1.75rem">
      <a class="fl-btn fl-btn--gradient" href="{WA}" target="_blank" rel="noopener">
        {icon('whatsapp')} Ask us anything</a>
      <a class="fl-btn fl-btn--ghost" href="sermons.html">{icon('play')} Hear a message first</a>
    </div>
  </div>
</section>

<section class="fl-section fl-section--ink">
  <div class="fl-wrap fl-wrap--narrow fl-reveal" style="text-align:center">
    <span class="fl-eyebrow">Already know us?</span>
    <h2>We were Kingdom Light Church</h2>
    <hr class="fl-rule" style="margin-inline:auto">
    <p class="fl-lead">Same church, same people, same address — a new name and a new look.
       If you are looking for Kingdom Light Church in Stellenbosch, you have found it.</p>
  </div>
</section>
""")

# --------------------------------------------------------------- sermons ---

PAGES["sermons.html"] = dict(
    title="Sermons | Fire &amp; Light Stellenbosch",
    description=("Watch the latest Sunday message from Fire & Light Stellenbosch, browse the video "
                 "library, or listen to the full sermon archive on Spotify and Apple Podcasts."),
    body=f"""
{banner("Sermons", "The latest Sunday message, and everything that came before it.")}

<section class="fl-section fl-section--ink">
  <div class="fl-wrap">
    <span class="fl-eyebrow">Now playing — latest upload</span>
    <h2>This Sunday’s message</h2>
    <hr class="fl-rule">
    {player_html()}
    <p class="fl-player-note">The newest sermon plays first. Use the playlist button in the top
       corner of the player to browse the full video library.</p>

    <div class="fl-btn-row" style="margin-top:2rem">
      <a class="fl-btn fl-btn--gradient" href="{YT_URL}" target="_blank" rel="noopener">
        {icon('youtube')} Subscribe on YouTube</a>
      <a class="fl-btn fl-btn--light" href="{YT_URL}/videos" target="_blank" rel="noopener">
        Browse all videos</a>
    </div>
  </div>
</section>

<section class="fl-section">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">The full archive</span>
        <h2>Listen anywhere</h2>
        <hr class="fl-rule">
        <p>Every Sunday message is published to our podcast — hundreds of them, going back years.
           Follow the show and each new sermon lands automatically, ready for the drive, the gym,
           or the walk.</p>
        <div class="fl-btn-row" style="margin-top:1.75rem">
          <a class="fl-btn fl-btn--gradient" href="{SPOTIFY_URL}" target="_blank" rel="noopener">
            {icon('spotify')} Follow on Spotify</a>
          <a class="fl-btn fl-btn--ghost"
             href="https://podcasts.apple.com/podcast/id1573552956" target="_blank" rel="noopener">
            Apple Podcasts</a>
        </div>
      </div>
      <div class="fl-podcast fl-reveal">
        <iframe src="https://open.spotify.com/embed/show/{SPOTIFY_SHOW}?theme=0"
                title="Fire and Light Stellenbosch podcast" loading="lazy"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
      </div>
    </div>
  </div>
</section>

<section class="fl-section fl-section--tight fl-cta-band">
  <div class="fl-wrap">
    <h2>Better in person</h2>
    <p>Sundays 9:30am at PJ Olivier Art School, Stellenbosch.</p>
    <div class="fl-btn-row" style="margin-top:1.5rem">
      <a class="fl-btn fl-btn--light" href="visit.html">Plan your visit</a>
    </div>
  </div>
</section>
""")

# ----------------------------------------------------------- who we are ----


PAGES["our-story.html"] = dict(
    title="Our Story | Fire &amp; Light Stellenbosch",
    description=("Eight years of God's faithfulness, a new season, and a clear mandate: to bring "
                 "the fire of His presence and the light of His truth to Stellenbosch and beyond."),
    body=f"""
{banner("Our Story", "Where we have come from, and where we are going.")}

<section class="fl-section">
  <div class="fl-wrap fl-wrap--narrow">
    <p class="fl-lead">Over the past eight years, our story has been one of God’s faithfulness —
       it’s been a prophetic calling and a clear mandate to bring the fire of His presence and the
       light of His truth to our region, our province, and our nation.</p>

    <p>In 2026 we are stepping into a new season — a new mandate and a new wineskin. This is not
       just a name change. It is a defining moment in our journey as a church family.</p>

    <p>We are a Spirit-empowered church with a passion to host God’s presence and create space for
       real encounters with Him. We believe transformation happens when people experience Jesus
       personally, grow deeply in their faith, and are equipped to live out their calling.</p>

    <p>We believe every person is called to carry God’s fire within them and shine His light
       through them.</p>
  </div>
</section>

<section class="fl-section fl-section--warm">
  <div class="fl-wrap">
    <div class="fl-grid fl-grid--2">

      <article class="fl-card fl-reveal" style="padding:clamp(2rem,4vw,3rem)">
        <span class="fl-eyebrow">Our Vision</span>
        <hr class="fl-rule">
        <p class="fl-lead">To see Stellenbosch and the nations transformed by the fire of God’s
           presence and the light of Jesus Christ, bringing life, truth, and freedom.</p>
      </article>

      <article class="fl-card fl-reveal" style="padding:clamp(2rem,4vw,3rem)">
        <span class="fl-eyebrow">Our Mission</span>
        <hr class="fl-rule">
        <p class="fl-lead">Fire &amp; Light Stellenbosch exists to glorify God by proclaiming the
           Gospel of Jesus Christ, making disciples empowered by the Holy Spirit, and advancing
           God’s Kingdom in every sphere of society, carrying His fire within us and shining His
           light through us.</p>
      </article>

    </div>
  </div>
</section>

<section class="fl-section fl-section--tight fl-cta-band">
  <div class="fl-wrap">
    <h2>This is who we are.</h2>
    <p>This is our mandate. And this is our moment.<br><strong>Welcome to the family.</strong></p>
    <div class="fl-btn-row" style="margin-top:1.75rem">
      <a class="fl-btn fl-btn--light" href="our-values.html">Our Values</a>
      <a class="fl-btn fl-btn--light" href="statement-of-faith.html">What We Believe</a>
    </div>
  </div>
</section>

{tagline_band()}
""")

# ---------------------------------------------------------------- team -----

PAGES["meet-our-team.html"] = dict(
    title="Meet our Team | Fire &amp; Light Stellenbosch",
    description=("Meet Hennie and Salomie Botha, senior leaders of Fire & Light Stellenbosch, and "
                 "the leadership team serving the church family."),
    body=f"""
{banner("Meet our Team", "The people God has placed here to serve and lead this family.")}

<section class="fl-section">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-split__media fl-reveal">
        <img src="assets/img/Hennie-Salomie.jpg" alt="Hennie and Salomie Botha"
             width="1400" height="934" loading="lazy">
      </div>
      <div class="fl-reveal">
        <span class="fl-eyebrow">Senior leaders</span>
        <h2>Hennie &amp; Salomie Botha</h2>
        <hr class="fl-rule">
        <p>Hennie and Salomie are a strong ministry couple that love God’s Kingdom and have a
           passion to bring a revival culture wherever they go.</p>
        <p>Hennie has been in pastoral ministry for 25 years, including serving as national
           coordinator for Champions for Christ South Africa. His focus is supernatural
           transformation in people, and practically bringing the Kingdom of God to others.</p>
        <p>Salomie is a trained musician with a heart for worship leadership. She has given herself
           to equipping the next generation of worship leaders and musicians, and led a worship
           school for five years.</p>
        <p>They have twin daughters, Shammei and Chené, and serve in Stellenbosch as family
           pastors.</p>
      </div>
    </div>
  </div>
</section>

<section class="fl-section fl-section--warm">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">Serving alongside them</span>
        <h2>Leadership Team</h2>
        <hr class="fl-rule">
        <p>A team of leaders who carry the vision of the house and serve the church family week
           in, week out.</p>
        <ul class="fl-people">
          <li>Marna Aucamp</li>
          <li>Christel Smit</li>
          <li>Gerhard de Villiers</li>
          <li>Louise de Villiers</li>
          <li>André van Eeden</li>
          <li>Marlien van Eeden</li>
        </ul>
      </div>
      <div class="fl-split__media fl-reveal">
        <img src="assets/img/Leadership.jpg" alt="The Fire &amp; Light leadership team"
             width="1400" height="934" loading="lazy">
      </div>
    </div>
  </div>
</section>
""")

# --------------------------------------------------- mission and vision ----


# -------------------------------------------------------------- values -----


def values_html():
    out = []
    for i, (name, body, scriptures) in enumerate(VALUES, start=1):
        verses = "".join(
            f"<li>“{text}”<cite>{ref}</cite></li>" for text, ref in scriptures)
        out.append(f"""<article class="fl-value fl-reveal">
        <div class="fl-value__num">{i}</div>
        <div>
          <h2>{name}</h2>
          <p>{body}</p>
          <ul class="fl-scripture">{verses}</ul>
        </div>
      </article>""")
    return "\n".join(out)


PAGES["our-values.html"] = dict(
    title="Our Values | Fire &amp; Light Stellenbosch",
    description=("The five values that shape Fire & Light Stellenbosch: Word & faith, Spirit "
                 "empowered, relationship & family, building people, and worship & prayer."),
    body=f"""
{banner("Our Values", "Five commitments that shape how we live and gather.")}

<section class="fl-section">
  <div class="fl-wrap fl-wrap--narrow">
    {values_html()}
  </div>
</section>

<section class="fl-section fl-section--tight fl-cta-band">
  <div class="fl-wrap">
    <h2>Come and see</h2>
    <p>Values are easier felt than read. Join us on a Sunday at 9:30am.</p>
    <div class="fl-btn-row" style="margin-top:1.5rem">
      <a class="fl-btn fl-btn--light" href="visit.html">Plan your visit</a>
    </div>
  </div>
</section>
""")

# -------------------------------------------------- statement of faith -----


def beliefs_html():
    out = []
    for name, body in BELIEFS:
        out.append(f"""<article class="fl-belief fl-reveal" style="margin-bottom:clamp(2rem,4vw,2.75rem)">
        <h2>{name}</h2>
        <p>{body}</p>
      </article>""")
    return "\n".join(out)


PAGES["statement-of-faith.html"] = dict(
    title="What We Believe | Fire &amp; Light Stellenbosch",
    description=("What we believe: the triune God, the Scriptures, salvation by grace through "
                 "faith, the Holy Spirit, the Church, and the return of Christ."),
    body=f"""
{banner("What We Believe", "Our statement of faith — what we believe, and what we build on.")}

<section class="fl-section">
  <div class="fl-wrap fl-wrap--narrow fl-beliefs">
    {beliefs_html()}
  </div>
</section>
""")

# -------------------------------------------------------- kids ministry ----

PAGES["kids-ministry.html"] = dict(
    title="Kids Ministry — Bright Sparks | Fire &amp; Light Stellenbosch",
    description=("Bright Sparks is the kids ministry at Fire & Light Stellenbosch. We put a high "
                 "emphasis on our children and believe families should worship together."),
    body=f"""
{banner("Kids Ministry", "Bright Sparks — where the next generation belongs.")}

<section class="fl-section">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">Bright Sparks</span>
        <h2>We love Kids Church!</h2>
        <hr class="fl-rule">
        <p>Family is such an important value for us as a church and we put high emphasis on our
           kids during Sunday mornings. We believe as we invest in the next generation we will see
           God move mightily through them in years to come!</p>
        <p>Kids are intentionally part of the worship experience during Sunday morning services. We
           believe that families should worship together to create a culture of worship.</p>
        <div class="fl-btn-row" style="margin-top:1.75rem">
          <a class="fl-btn fl-btn--gradient" href="{WA}" target="_blank" rel="noopener">
            {icon('whatsapp')} Ask us about kids</a>
          <a class="fl-btn fl-btn--ghost" href="visit.html">Plan your visit</a>
        </div>
      </div>
      <div class="fl-split__media fl-reveal">
        <img src="assets/img/bright-sparks.jpg" alt="Bright Sparks kids ministry"
             width="1920" height="1080" loading="lazy">
      </div>
    </div>
  </div>
</section>
""")

# ---------------------------------------------------------------- give -----

PAGES["give.html"] = dict(
    title="Give | Fire &amp; Light Stellenbosch",
    description=("Give to Fire & Light Stellenbosch by EFT or SnapScan, volunteer on a team, or "
                 "join the prayer team. Banking details and ways to partner with us."),
    body=f"""
{banner("Give", "Three ways to partner with what God is doing here.")}

<section class="fl-section fl-section--tight">
  <div class="fl-wrap fl-wrap--narrow fl-center">
    <blockquote class="fl-quote">
      “Give, and you will receive. Your gift will return to you in full — pressed down, shaken
      together to make room for more, running over, and poured into your lap.”
      <footer>Luke 6:38 NLT</footer>
    </blockquote>
  </div>
</section>

<section class="fl-section">
  <div class="fl-wrap">
    <div class="fl-grid fl-grid--3">

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('users')}</div>
        <h2>Volunteer</h2>
        <p>Serve on one of our departments — worship, media, technical, or hospitality. There’s a
           place for your gift here.</p>
        <p style="margin-top:1rem"><a href="{WA}" target="_blank" rel="noopener">Get involved →</a></p>
      </article>

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('heart')}</div>
        <h2>Tithes &amp; Offerings</h2>
        <p>Give by EFT, by SnapScan, or during our Sunday services. Every gift goes into the
           mission of this house.</p>
        <p style="margin-top:1rem"><a href="#banking">Banking details →</a></p>
      </article>

      <article class="fl-card fl-card--lift fl-reveal">
        <div class="fl-info__icon" style="margin-bottom:1rem">{icon('clock')}</div>
        <h2>Prayer</h2>
        <p>Prayer is the engine room. Join our prayer team and stand with us for Stellenbosch and
           the nations.</p>
        <p style="margin-top:1rem"><a href="contact.html">Contact us →</a></p>
      </article>

    </div>
  </div>
</section>

<section class="fl-section fl-section--warm" id="banking">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">EFT</span>
        <h2>Banking details</h2>
        <hr class="fl-rule">
        <ul class="fl-bank">
          <li><span class="k">Account holder</span><span class="v">Fire and Light Stellenbosch</span></li>
          <li><span class="k">Bank</span><span class="v">FNB — Cheque Account</span></li>
          <li><span class="k">Account number</span><span class="v">63 208 789 264</span></li>
          <li><span class="k">Branch code</span><span class="v">200610</span></li>
          <li><span class="k">Swift code</span><span class="v">FIRNZAJJ</span></li>
        </ul>
      </div>

      <div class="fl-snap fl-reveal">
        <span class="fl-eyebrow">SnapScan</span>
        <h2 style="font-size:clamp(1.4rem,3vw,1.9rem)">Scan to give</h2>
        <hr class="fl-rule" style="margin-inline:auto">
        <img src="assets/img/FL_Snapscan.jpg" alt="SnapScan QR code for Fire &amp; Light Stellenbosch"
             width="350" height="429" loading="lazy">
        <p>Open SnapScan on your phone and scan the code.</p>
      </div>
    </div>
  </div>
</section>
""")

# ------------------------------------------------------------- contact -----

PAGES["contact.html"] = dict(
    title="Contact | Fire &amp; Light Stellenbosch",
    description=("Send Fire & Light Stellenbosch a message, or follow along on WhatsApp, "
                 "Facebook, Instagram, YouTube and Spotify."),
    body=f"""
{banner("Contact", "Send us a message, or follow along through the week.")}

<section class="fl-section fl-section--tight">
  <div class="fl-wrap fl-reveal">
    <div class="fl-notice-card">
      <div>
        <span class="fl-eyebrow">Coming on a Sunday?</span>
        <h2 style="margin-top:.35rem">Everything you need is on one page</h2>
        <p>Service time, the address, the side entrance in Mark Street, the map, and what happens
           with your kids.</p>
      </div>
      <div class="fl-btn-row">
        <a class="fl-btn fl-btn--gradient" href="visit.html">Plan your visit</a>
      </div>
    </div>
  </div>
</section>

<section class="fl-section fl-section--warm">
  <div class="fl-wrap fl-wrap--narrow">
    <div class="fl-center">
      <span class="fl-eyebrow">Send a message</span>
      <h2>Get in touch</h2>
      <hr class="fl-rule" style="margin-inline:auto">
      <p class="fl-lead">Questions, prayer requests, or wanting to get involved — we read
         everything.</p>
    </div>

    <form class="fl-form" id="fl-contact-form" style="margin-top:2.5rem"
          action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <p class="fl-hp" aria-hidden="true">
        <label>Leave this empty <input type="text" name="fl-website" tabindex="-1" autocomplete="off"></label>
      </p>

      <div class="fl-field">
        <label for="fl-name">Your name</label>
        <input id="fl-name" name="name" type="text" required autocomplete="name">
      </div>

      <div class="fl-field">
        <label for="fl-email">Email address</label>
        <input id="fl-email" name="email" type="email" required autocomplete="email">
      </div>

      <div class="fl-field">
        <label for="fl-message">Message</label>
        <textarea id="fl-message" name="message" required></textarea>
      </div>

      <div class="fl-btn-row">
        <button class="fl-btn fl-btn--gradient" type="submit">Send it</button>
        <a class="fl-btn fl-btn--ghost" href="{WA}" target="_blank" rel="noopener">
          {icon('whatsapp')} WhatsApp instead</a>
      </div>

      <p class="fl-form__note" id="fl-form-note">This form opens your email app with the message
         ready to send, so nothing gets lost on the way.</p>
    </form>
  </div>
</section>

<section class="fl-section fl-section--warm" id="follow">
    <div class="fl-wrap fl-center" style="margin-bottom:clamp(2rem,4vw,3rem)">
      <span class="fl-eyebrow">Follow us</span>
      <h2>Stay connected through the week</h2>
      <hr class="fl-rule" style="margin-inline:auto">
    </div>
  <div class="fl-wrap">
    <ul class="fl-socials">

      <li><a class="fl-social" href="{WA}" target="_blank" rel="noopener">
        <span class="fl-social__icon fl-ic-whatsapp">{icon('whatsapp')}</span>
        <span><span class="fl-social__label">WhatsApp</span>
              <span class="fl-social__handle">Message us — quickest reply</span></span>
      </a></li>

      <li><a class="fl-social" href="{FB_URL}" target="_blank" rel="noopener">
        <span class="fl-social__icon fl-ic-facebook">{icon('facebook')}</span>
        <span><span class="fl-social__label">Facebook</span>
              <span class="fl-social__handle">/FireandLightStellenbosch</span></span>
      </a></li>

      <li><a class="fl-social" href="{IG_URL}" target="_blank" rel="noopener">
        <span class="fl-social__icon fl-ic-instagram">{icon('instagram')}</span>
        <span><span class="fl-social__label">Instagram</span>
              <span class="fl-social__handle">@fireandlightstellenbosch</span></span>
      </a></li>

      <li><a class="fl-social" href="{YT_URL}" target="_blank" rel="noopener">
        <span class="fl-social__icon fl-ic-youtube">{icon('youtube')}</span>
        <span><span class="fl-social__label">YouTube</span>
              <span class="fl-social__handle">@FireLightStellenbosch</span></span>
      </a></li>

      <li><a class="fl-social" href="{SPOTIFY_URL}" target="_blank" rel="noopener">
        <span class="fl-social__icon fl-ic-spotify">{icon('spotify')}</span>
        <span><span class="fl-social__label">Spotify</span>
              <span class="fl-social__handle">Sermon podcast</span></span>
      </a></li>

      <li><a class="fl-social" href="mailto:{EMAIL}">
        <span class="fl-social__icon fl-ic-mail">{icon('mail')}</span>
        <span><span class="fl-social__label">Email</span>
              <span class="fl-social__handle">{EMAIL}</span></span>
      </a></li>

    </ul>
  </div>
</section>

<section class="fl-section fl-section--ink">
  <div class="fl-wrap">
    <div class="fl-split">
      <div class="fl-reveal">
        <span class="fl-eyebrow">Latest upload</span>
        <h2>From our channel</h2>
        <hr class="fl-rule">
        <p>Our newest video, straight from YouTube. Subscribe and you’ll never miss a Sunday.</p>
        <div class="fl-btn-row" style="margin-top:1.75rem">
          <a class="fl-btn fl-btn--gradient" href="{YT_URL}" target="_blank" rel="noopener">
            {icon('youtube')} Subscribe</a>
          <a class="fl-btn fl-btn--light" href="sermons.html">All sermons</a>
        </div>
      </div>
      <div class="fl-reveal">{player_html()}</div>
    </div>
  </div>
</section>
""")

# -------------------------------------------------------- social media -----

# ================================================================ write ====

def main():
    written = []

    for slug, data in PAGES.items():
        html = prettify_urls(page(slug, data["title"], data["description"], data["body"]))
        path = os.path.join(HERE, slug)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(slug)

    # sitemap
    urls = "".join(f"\n  <url><loc>{SITE}{url_for(s)}</loc></url>" for s in PAGES)
    with open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                 f'{urls}\n</urlset>\n')

    with open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    print(f"Built {len(written)} pages:")
    for s in written:
        print("  ", s)
    print("   sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
