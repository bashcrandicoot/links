# bashframes links

Link-in-bio page for bashframes, planned for https://bashcrandicoot.github.io/links/ (GitHub Pages, project repo named `links`).

- Base: [LittleLink](https://github.com/sethcottle/littlelink) by Seth Cottle, MIT (see `LICENSE.md`). `css/reset.css` and `css/style.css` are LittleLink's (Open Sans font-face removed); `css/bashframes.css` is the bashframes theme layered on top.
- Icons `images/icons/*` are from LittleLink.
- Fonts: Space Grotesk and JetBrains Mono, self-hosted Latin subsets, SIL OFL 1.1 (`fonts/OFL-*.txt`).
- Logo mark, one-line wordmark and barcode element are from the bashframes brand kit v1.0.
- One accent: Acid Lime `#C6FF00`, used only for the primary "Download Lodge" button and hover/focus states.
- No analytics, no third-party requests. Plain static HTML/CSS, no build step and no JS.

Deploy (not done yet): put these files at the root of a repo named `links`, then Settings → Pages → Deploy from branch `main` / root.

## Notes
- Hero: the featured card uses `images/featured-lodge-1200.jpg` / `-2400.jpg` (Brandy's card). Short paths `/apps/` and `/lodge/` are redirect pages to the GitHub Pages sites.
- Instagram: the handle changes to bashframes on Nov 9, 2026. In `index.html`, search for "pkt.guru" and update the href and the visible handle (2 spots).
- The header handle @bashframes links to https://www.youtube.com/@bashframes.
