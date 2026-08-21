# Fire & Light Stellenbosch — website

Static site for [Fire & Light Church, Stellenbosch](https://fireandlight.co.za)
(formerly Kingdom Light Church). No build step, no dependencies.

## Deploying

Hosted on **Cloudflare Pages**, connected to this repository — pushing to `main`
publishes.

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` |
| Root directory | `/` |
| Production branch | `main` |

Cloudflare created this as a **Worker** (Workers Static Assets), not a Pages
project — new git-connected static sites land there now. It serves at
`fire-and-light-church.gericke-fourie.workers.dev`. Note `wrangler pages
project list` will show nothing; use `wrangler deployments list --name
fire-and-light-church`.

`_headers` sets the cache policy. **No filename here carries a content hash**, so
HTML/CSS/JS must revalidate every request — otherwise an edge copy serves stale
code after a deploy and a fix appears not to have worked.

## Editing content

Pages are **generated**. `_build.py` holds every page's copy, the navigation
tree, the SVG icon set and the shared shell (head, header, footer):

```bash
python3 _build.py      # rewrites the 10 .html files + sitemap.xml + robots.txt
```

Edit `_build.py`, not the HTML — the HTML is overwritten on every build.

Preview locally:

```bash
python3 serve.py
```

Use `serve.py`, **not** `python3 -m http.server`. The site's links are
extensionless (`/contact`) because Workers Static Assets strips `.html`;
`http.server` would 404 on every one of them. `serve.py` maps `/contact` to
`contact.html` so local URLs match production.

## Design system

Built against the church's brand system card. The values are not improvised:

- **Type** — Barlow (headings uppercase, tracked `.03em`); IBM Plex Mono for
  times, addresses and metadata only.
- **Colour** — one warm ramp, no secondary hue: crimson `#d60034`, flame
  `#e8402f`, orange `#f2762f`, sun `#f7983a`, amber `#fbb03b`, UI amber
  `#f5a93c`, on warm ink `#1d1d1b` and paper `#faf9f6`. Neutrals are warm,
  never blue-grey.
- **Gradients** — two only, never re-angled: `mark` at 135°, `band` at 90°.
- **Motion** — 220ms `cubic-bezier(.2,.6,.2,1)`, 8px rise, 2px hover lift,
  `scale(.98)` press. No bounce.
- **Pillars** — the arched crimson→sun capsule is reserved for the four pillars
  and used nowhere else.
- **Logo** — colour lockup on paper; white knockout on ink, photography and the
  gradient band. Never recoloured, outlined or rotated.

## Information architecture

The nav follows the visitor's decision, not the church's org chart:

```
Home | Visit | About ▾ | Sermons | Kids | Give | Contact
                ├ Our Story
                ├ Our Values
                ├ What We Believe
                └ Our Team
```

**`/visit` is the destination for the site's primary CTA.** "Plan your visit"
appears in the header, the service bar, the closing band and on Kids — before
this page existed all of those landed on `/contact`, a contact form that
answered none of a first-time visitor's questions.

`/who-we-are` and `/mission-and-vision` were merged into `/our-story`: they
restated the same mission and vision text and each re-rendered the four
pillars, which the homepage already showed. `_redirects` keeps the old URLs
alive with 301s — do not delete it.

`/statement-of-faith` keeps its URL (existing links, search results) but is
titled **What We Believe** so the page and its nav label agree.

The homepage runs hero → service bar → name-change notice → who we are →
latest message → what we carry → next steps → invitation. The pillars used to
sit second, putting abstract theology before the reader knew who was speaking.

### Content gaps

The Visit page deliberately states **only** what the site already established.
These are unanswered and worth filling in — none of it should be invented:

- Parking — where, and is it safe on a Sunday morning?
- How long the service runs.
- Whether there is coffee or anything before/after.
- Wheelchair access and whether the Mark Street side entrance has steps.
- Kids: any age range, or is it genuinely all ages in the service?

## Accessibility notes

Heading order is checked on every build-and-review pass: exactly one `<h1>` per
page and no skipped levels. Two traps:

- The homepage hero is a logo, so its `<h1>` is visually hidden (`.fl-vh`).
  Without it the page had no `h1` at all.
- Footer section headings are `<h2 class="fl-footer__h">`, not `<h4>`. The
  class carries the small caption styling — style them by class, never by tag,
  or changing the level for heading order silently resizes them.

## Notable implementation details

**Sermons page.** The latest video loads itself from the channel's *uploads
playlist* (`list=UU…`, the channel ID with `UC` swapped for `UU`) — no API key,
no RSS feed, no CORS proxy, nothing to expire. Channel is
`@FireLightStellenbosch` / `UCdKWohKcSp-YRycCB6vAWLw`. Note there is a second,
dormant channel with a near-identical handle — don't wire that one up.

**Hero.** The brand intro is a logo reveal on black, so `mix-blend-mode: screen`
drops its background out over the photograph. Its dim lead-in is trimmed and its
shadows crushed at encode time, otherwise the first second is invisible and the
video's bounding box shows as a faint rectangle. The static wordmark stays
visible until the video reports `playing`, so blocked autoplay, a missing file
or `prefers-reduced-motion` all still show a logo.

**Contact form.** No backend — it composes a `mailto:` and hands off to the
visitor's mail client, which is honest rather than silently dropping messages.
If it ever needs real submissions, that means a host with form handling.

## Assets

`_source/` holds the colour logo masters. The white knockouts in `assets/img/`
are generated from them; a true knockout is *entirely* white, ampersand included.
