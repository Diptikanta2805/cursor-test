/* Main interactions — navigation, scroll reveals, typewriter, research orbits */

(function () {
  'use strict';

  /* ── Research topic data ── */
  const TOPICS = {
    genai: {
      title: 'Generative AI Adoption & Value Creation',
      desc: 'How do firms create market value from transformative GenAI technologies? My empirical work examines abnormal returns from GenAI announcements across S&P 500 firms, revealing how innovation capabilities, strategic alliances, and implementation scope jointly determine value capture.',
      methods: ['Event Study', 'Panel Data', 'S&P 500', 'Abnormal Returns'],
    },
    leadership: {
      title: 'Strategic Leadership & Top Management Teams',
      desc: 'Investigating how top management team composition, cognition, and decision-making processes shape strategic choices in technology adoption. Drawing on upper echelons theory to understand how leader characteristics influence organizational responses to disruptive innovation.',
      methods: ['Upper Echelons', 'TMT Analysis', 'Strategic Choice'],
    },
    cognition: {
      title: 'CEO / TMT Cognition',
      desc: 'Examining how cognitive frameworks of CEOs and top management teams affect strategic attention allocation, resource orchestration, and competitive positioning — particularly when navigating ambiguous, fast-moving technological landscapes like generative AI.',
      methods: ['Attention-Based View', 'Cognitive Mapping', 'Text Analysis'],
    },
    innovation: {
      title: 'Innovation Capabilities & Strategic Alliances',
      desc: 'Exploring the paradox of innovation capabilities: firms with stronger innovation portfolios may capture less value from GenAI unless they complement internal capabilities with strategic partnerships. Understanding when exploration vs. exploitation orientation amplifies returns.',
      methods: ['Resource Orchestration', 'Alliance Governance', 'Innovation Orientation'],
    },
    learning: {
      title: 'Organizational Learning & Adaptation',
      desc: 'How do organizations learn to integrate agentic AI frameworks and autonomous systems into existing routines? Studying the mechanisms of organizational adaptation when transformative technologies alter traditional assumptions about resources, capabilities, and competitive advantage.',
      methods: ['Organizational Learning', 'Agentic AI', 'Dynamic Capabilities'],
    },
  };

  const TAGLINES = [
    'Studying how firms orchestrate GenAI for competitive advantage →',
    'Bridging digital analytics expertise with strategic management theory →',
    'Examining CEO cognition in the age of autonomous systems →',
    'From Accenture data science to academic strategy research →',
  ];

  /* ── DOM refs ── */
  const nav = document.getElementById('nav');
  const mobileMenu = document.getElementById('mobile-menu');
  const navToggle = document.querySelector('.nav-toggle');
  const typewriterEl = document.getElementById('typewriter');
  const topicPanel = document.getElementById('topic-panel');
  const topicContent = document.getElementById('topic-content');
  const orbitNodes = document.querySelectorAll('.orbit-node');
  const cursorGlow = document.querySelector('.cursor-glow');

  /* ── Navigation scroll effect ── */
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  /* ── Mobile menu ── */
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
      mobileMenu.setAttribute('aria-hidden', !isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── Smooth active nav highlighting ── */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  const observerNav = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(link => {
          link.style.color = link.getAttribute('href') === `#${entry.target.id}`
            ? 'var(--text-primary)'
            : '';
        });
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => observerNav.observe(s));

  /* ── Scroll reveal ── */
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        const siblings = [...entry.target.parentElement.querySelectorAll('.reveal')];
        const idx = siblings.indexOf(entry.target);
        entry.target.style.transitionDelay = `${idx * 0.08}s`;
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => revealObserver.observe(el));

  /* ── Typewriter effect ── */
  let taglineIdx = 0;
  let charIdx = 0;
  let isDeleting = false;
  let typeTimeout;

  function typewrite() {
    const current = TAGLINES[taglineIdx];

    if (!isDeleting) {
      typewriterEl.textContent = current.substring(0, charIdx + 1);
      charIdx++;
      if (charIdx === current.length) {
        isDeleting = true;
        typeTimeout = setTimeout(typewrite, 2500);
        return;
      }
      typeTimeout = setTimeout(typewrite, 55);
    } else {
      typewriterEl.textContent = current.substring(0, charIdx - 1);
      charIdx--;
      if (charIdx === 0) {
        isDeleting = false;
        taglineIdx = (taglineIdx + 1) % TAGLINES.length;
        typeTimeout = setTimeout(typewrite, 400);
        return;
      }
      typeTimeout = setTimeout(typewrite, 30);
    }
  }

  if (typewriterEl) {
    setTimeout(typewrite, 800);
  }

  /* ── Research orbit interactions ── */
  function showTopic(key) {
    const topic = TOPICS[key];
    if (!topic) return;

    orbitNodes.forEach(n => n.classList.toggle('active', n.dataset.topic === key));
    topicPanel.classList.add('active');

    topicContent.innerHTML = `
      <h3 class="topic-title">${topic.title}</h3>
      <p class="topic-desc">${topic.desc}</p>
      <div class="topic-methods">
        ${topic.methods.map(m => `<span>${m}</span>`).join('')}
      </div>
    `;
  }

  orbitNodes.forEach(node => {
    node.addEventListener('click', () => showTopic(node.dataset.topic));
  });

  // Auto-select first topic after delay
  setTimeout(() => showTopic('genai'), 2000);

  /* ── Cursor glow follow ── */
  if (cursorGlow && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mousemove', (e) => {
      cursorGlow.style.left = e.clientX + 'px';
      cursorGlow.style.top = e.clientY + 'px';
    }, { passive: true });
  }

  /* ── Parallax on hero stats ── */
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const hero = document.getElementById('hero');
    if (hero && scrolled < window.innerHeight) {
      const content = hero.querySelector('.hero-content');
      if (content) {
        content.style.transform = `translateY(${scrolled * 0.25}px)`;
        content.style.opacity = 1 - scrolled / (window.innerHeight * 0.8);
      }
    }
  }, { passive: true });

})();
