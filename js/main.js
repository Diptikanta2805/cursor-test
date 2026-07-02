/**
 * Strategic Signal — Interactive portfolio for Diptikanta Panigrahi
 */

// ── Theme ──────────────────────────────────────────────
const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme');
if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);

themeToggle?.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// ── Network Canvas (strategic alliance visualization) ─
const canvas = document.getElementById('network-canvas');
const ctx = canvas?.getContext('2d');

const nodes = [];
const NODE_COUNT = 40;
const CONNECTION_DIST = 140;
let mouseX = -1000;
let mouseY = -1000;

function resizeCanvas() {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initNodes();
}

function initNodes() {
  nodes.length = 0;
  for (let i = 0; i < NODE_COUNT; i++) {
    nodes.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      radius: Math.random() * 2 + 1,
    });
  }
}

function getAccentColor() {
  return getComputedStyle(document.documentElement)
    .getPropertyValue('--accent').trim() || '#1e4d6b';
}

function drawNetwork() {
  if (!ctx || !canvas) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const accent = getAccentColor();

  for (const node of nodes) {
    node.x += node.vx;
    node.y += node.vy;
    if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
    if (node.y < 0 || node.y > canvas.height) node.vy *= -1;

    const dx = mouseX - node.x;
    const dy = mouseY - node.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 200) {
      node.x -= dx * 0.002;
      node.y -= dy * 0.002;
    }
  }

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < CONNECTION_DIST) {
        const alpha = (1 - dist / CONNECTION_DIST) * 0.35;
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        ctx.lineTo(nodes[j].x, nodes[j].y);
        ctx.strokeStyle = accent;
        ctx.globalAlpha = alpha;
        ctx.lineWidth = 0.8;
        ctx.stroke();
      }
    }
  }

  ctx.globalAlpha = 1;
  for (const node of nodes) {
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
    ctx.fillStyle = accent;
    ctx.globalAlpha = 0.6;
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  requestAnimationFrame(drawNetwork);
}

window.addEventListener('resize', resizeCanvas);
document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

resizeCanvas();
drawNetwork();

// ── Research Compass ───────────────────────────────────
const compassThemes = {
  genai: 'Generative AI adoption and implementation strategy — how firms orchestrate resources to capture value from transformative technologies.',
  leadership: 'CEO and top management team cognition — how executive attention and mental models shape strategic choices under uncertainty.',
  alliances: 'Strategic alliances as complementors — when partnerships amplify or erode returns from innovation investments.',
  learning: 'Organizational learning routines — how firms build absorptive capacity for autonomous and agentic AI systems.',
  innovation: 'Innovation capabilities and exploratory orientation — the tension between exploitation and exploration in technology strategy.',
};

const compassDetail = document.getElementById('compass-detail');
document.querySelectorAll('.compass-node').forEach((node) => {
  node.addEventListener('click', () => {
    document.querySelectorAll('.compass-node').forEach((n) => n.classList.remove('active'));
    node.classList.add('active');
    const theme = node.dataset.theme;
    if (compassDetail && compassThemes[theme]) {
      compassDetail.textContent = compassThemes[theme];
      compassDetail.classList.add('active');
    }
  });
});

// ── Counter animation ──────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = parseInt(el.dataset.count, 10);
    const duration = 1500;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}

const heroObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounters();
        heroObserver.disconnect();
      }
    });
  },
  { threshold: 0.5 }
);

const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObserver.observe(heroStats);

// ── Scroll reveal ──────────────────────────────────────
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
);

document.querySelectorAll('[data-reveal]').forEach((el) => revealObserver.observe(el));

// ── Timeline progress ──────────────────────────────────
const timeline = document.getElementById('timeline');
const timelineProgress = document.getElementById('timeline-progress');
const timelineItems = document.querySelectorAll('.timeline-item');

const timelineObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  },
  { threshold: 0.3 }
);

timelineItems.forEach((item) => timelineObserver.observe(item));

function updateTimelineProgress() {
  if (!timeline || !timelineProgress) return;
  const rect = timeline.getBoundingClientRect();
  const windowH = window.innerHeight;
  const start = rect.top + window.scrollY;
  const end = start + rect.height;
  const scroll = window.scrollY + windowH * 0.5;
  const progress = Math.max(0, Math.min(1, (scroll - start) / (end - start)));
  timelineProgress.style.height = `${progress * 100}%`;
}

window.addEventListener('scroll', updateTimelineProgress, { passive: true });
updateTimelineProgress();

// ── Command Palette ────────────────────────────────────
const cmdPalette = document.getElementById('cmd-palette');
const cmdTrigger = document.getElementById('cmd-trigger');
const cmdInput = document.getElementById('cmd-input');
const cmdResults = document.getElementById('cmd-results');

const cmdItems = [
  { label: 'Research', href: '#research', type: 'section' },
  { label: 'Teaching', href: '#teaching', type: 'section' },
  { label: 'Trajectory', href: '#trajectory', type: 'section' },
  { label: 'Job Market Dossier', href: '#dossier', type: 'section' },
  { label: 'Contact', href: '#contact', type: 'section' },
  { label: 'LinkedIn Profile', href: 'https://www.linkedin.com/in/diptikanta-panigrahi/', type: 'external' },
  { label: 'KU Faculty Page', href: 'https://business.ku.edu/people/diptikanta-panigrahi', type: 'external' },
  { label: 'AOM Proceedings Paper', href: 'https://doi.org/10.5465/amproc.2025.16553abstract', type: 'external' },
  { label: 'Toggle Dark Mode', action: 'theme', type: 'action' },
];

let selectedIndex = 0;

function renderCmdResults(filter = '') {
  if (!cmdResults) return;
  const q = filter.toLowerCase();
  const filtered = cmdItems.filter((item) => item.label.toLowerCase().includes(q));
  selectedIndex = 0;

  cmdResults.innerHTML = filtered
    .map(
      (item, i) => `
      <li data-index="${i}" class="${i === 0 ? 'selected' : ''}" data-href="${item.href || ''}" data-action="${item.action || ''}" data-type="${item.type}">
        <span>${item.label}</span>
        <span>${item.type}</span>
      </li>`
    )
    .join('');

  cmdResults.querySelectorAll('li').forEach((li) => {
    li.addEventListener('click', () => executeCmdItem(li));
  });
}

function executeCmdItem(li) {
  const type = li.dataset.type;
  const href = li.dataset.href;
  const action = li.dataset.action;

  cmdPalette?.close();

  if (action === 'theme') {
    themeToggle?.click();
    return;
  }
  if (type === 'external' && href) {
    window.open(href, '_blank', 'noopener');
    return;
  }
  if (href) {
    document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
  }
}

function openCmdPalette() {
  cmdPalette?.showModal();
  cmdInput.value = '';
  renderCmdResults();
  setTimeout(() => cmdInput?.focus(), 50);
}

cmdTrigger?.addEventListener('click', openCmdPalette);

document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openCmdPalette();
  }
});

cmdInput?.addEventListener('input', (e) => renderCmdResults(e.target.value));

cmdInput?.addEventListener('keydown', (e) => {
  const items = cmdResults?.querySelectorAll('li');
  if (!items?.length) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
    items.forEach((li, i) => li.classList.toggle('selected', i === selectedIndex));
    items[selectedIndex].scrollIntoView({ block: 'nearest' });
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    selectedIndex = Math.max(selectedIndex - 1, 0);
    items.forEach((li, i) => li.classList.toggle('selected', i === selectedIndex));
    items[selectedIndex].scrollIntoView({ block: 'nearest' });
  } else if (e.key === 'Enter') {
    e.preventDefault();
    executeCmdItem(items[selectedIndex]);
  } else if (e.key === 'Escape') {
    cmdPalette?.close();
  }
});

// ── Contact form (mailto fallback) ───────────────────
const contactForm = document.getElementById('contact-form');
const ACADEMIC_EMAIL = 'diptikanta@ku.edu';

contactForm?.addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(contactForm);
  const name = data.get('name');
  const email = data.get('email');
  const message = data.get('message');
  const subject = encodeURIComponent(`Job Market Inquiry from ${name}`);
  const body = encodeURIComponent(`From: ${name} <${email}>\n\n${message}`);
  window.location.href = `mailto:${ACADEMIC_EMAIL}?subject=${subject}&body=${body}`;
});

// ── CV download check ──────────────────────────────────
const cvLink = document.getElementById('cv-download');
if (cvLink) {
  fetch('assets/cv.pdf', { method: 'HEAD' })
    .then((res) => {
      if (res.ok) {
        cvLink.href = 'assets/cv.pdf';
        cvLink.removeAttribute('aria-disabled');
        cvLink.classList.remove('btn--ghost');
        cvLink.classList.add('btn--primary');
        const note = cvLink.nextElementSibling;
        if (note?.classList.contains('dossier-note')) note.style.display = 'none';
      }
    })
    .catch(() => {});
}

// ── Active nav highlight ───────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.main-nav a');

const navObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((link) => {
          link.style.color =
            link.getAttribute('href') === `#${entry.target.id}`
              ? 'var(--text)'
              : '';
        });
      }
    });
  },
  { threshold: 0.4, rootMargin: '-80px 0px -50% 0px' }
);

sections.forEach((section) => navObserver.observe(section));
