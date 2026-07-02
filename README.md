# Diptikanta Panigrahi — Personal Academic Website

A distinctive job-market portfolio site for a PhD candidate in Strategic Management at the University of Kansas.

## Features

- **Interactive Strategy Network** — Animated particle graph in the hero, themed around research domains (TMT cognition, GenAI, innovation, alliances)
- **The Attention Lab** — Interactive slider demo inspired by GenAI adoption research on strategic attention allocation
- **Morphing Hero** — Cycling research keywords that reflect the scholarly agenda
- **Job Market Section** — CV, research statement, and teaching statement availability with contact form
- **Career Timeline** — Industry analytics background (Accenture, Grant Thornton) through to academic research

## Quick Start

Open locally with any static server:

```bash
python3 -m http.server 8080
```

Then visit [http://localhost:8080](http://localhost:8080).

## Deploy

### GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set source to `main` branch, root `/`
4. Your site will be live at `https://<username>.github.io/<repo>/`

### Netlify / Vercel

Drag and drop the project folder, or connect the GitHub repo. No build step required.

## Customize

- Update job market year in `index.html` (hero badge and contact section)
- Add PDF links for CV, research statement, and teaching statement in the materials section
- Replace "Available upon request" with direct download links when ready

## Structure

```
index.html      # Main page
css/style.css   # Design system & layout
js/main.js      # Interactions (network canvas, attention lab, scroll reveals)
```

## Contact

Diptikanta Panigrahi — diptikanta@ku.edu
