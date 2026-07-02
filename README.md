# Diptikanta Panigrahi — Personal Academic Website

A distinctive, interactive portfolio site for the academic job market (AY 2026–2027).

## Features

- **Research Compass** — Interactive radial navigation of five research streams
- **Strategic Network** — Canvas visualization of alliance-like node connections (responds to cursor)
- **Command Palette** — Press `⌘K` / `Ctrl+K` to jump anywhere instantly
- **Flip Cards** — Hover research papers to reveal abstracts
- **Scholar–Practitioner Timeline** — Scroll-animated career arc from industry to academia
- **Dark / Light Mode** — Persistent theme preference
- **Job Market Dossier** — CV, research statement, teaching statement, references

## Quick Start

Open locally with any static server:

```bash
# Python
python3 -m http.server 8080

# Node (npx)
npx serve .
```

Then visit [http://localhost:8080](http://localhost:8080).

## Customize

1. **Email** — Update `EMAIL_PLACEHOLDER` in `js/main.js` with your academic email
2. **CV** — Add `assets/cv.pdf`; the download button activates automatically
3. **Research statements** — Link PDFs in the dossier section or add `assets/research-statement.pdf`
4. **Profile photo** — Optional: add to hero section in `index.html`

## Deploy

### GitHub Pages

1. Push this repo to GitHub
2. Settings → Pages → Source: `main` branch, root `/`
3. Site live at `https://<username>.github.io/<repo>/`

### Netlify / Vercel

Drag-and-drop the folder or connect the repo — no build step required.

## Tech Stack

Pure HTML, CSS, and vanilla JavaScript — no frameworks, no build step, fast and portable.

## License

Personal portfolio — all content © Diptikanta Panigrahi.
