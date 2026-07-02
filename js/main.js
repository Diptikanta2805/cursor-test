/**
 * Main interactions: navigation, research nodes, scroll reveals, timeline
 */

(function () {
  'use strict';

  // Navigation scroll state
  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  function onScroll() {
    if (window.scrollY > 60) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav toggle
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.classList.toggle('open', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Cursor glow follow
  const cursorGlow = document.querySelector('.cursor-glow');
  if (cursorGlow && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let glowX = 0, glowY = 0;
    let targetX = 0, targetY = 0;

    document.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
    });

    function animateGlow() {
      glowX += (targetX - glowX) * 0.08;
      glowY += (targetY - glowY) * 0.08;
      cursorGlow.style.left = glowX + 'px';
      cursorGlow.style.top = glowY + 'px';
      requestAnimationFrame(animateGlow);
    }
    animateGlow();
  }

  // Research constellation nodes
  const researchNodes = document.querySelectorAll('.research-node');
  const detailPanels = document.querySelectorAll('.detail-panel');

  researchNodes.forEach((node) => {
    node.addEventListener('click', () => {
      const target = node.dataset.node;

      researchNodes.forEach((n) => {
        n.classList.remove('active');
        n.setAttribute('aria-pressed', 'false');
      });
      node.classList.add('active');
      node.setAttribute('aria-pressed', 'true');

      detailPanels.forEach((panel) => {
        panel.classList.toggle('active', panel.dataset.panel === target);
      });
    });
  });

  // Scroll reveal observer
  const revealElements = document.querySelectorAll(
    '.section-header, .about-grid, .paper-card, .teaching-card, .awards-strip, .contact-grid, .stat-card'
  );

  revealElements.forEach((el) => el.classList.add('reveal'));

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  revealElements.forEach((el) => revealObserver.observe(el));

  // Timeline scroll progress
  const timeline = document.getElementById('timeline');
  const timelineProgress = document.getElementById('timeline-progress');
  const timelineItems = document.querySelectorAll('.timeline-item');

  if (timeline && timelineProgress) {
    const timelineObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.3 }
    );

    timelineItems.forEach((item) => timelineObserver.observe(item));

    function updateTimelineProgress() {
      const rect = timeline.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      const start = windowHeight * 0.8;
      const end = -rect.height + windowHeight * 0.3;
      const progress = Math.max(0, Math.min(1, (start - rect.top) / (start - end)));
      timelineProgress.style.height = (progress * 100) + '%';
    }

    window.addEventListener('scroll', updateTimelineProgress, { passive: true });
    updateTimelineProgress();
  }

  // Active nav link highlighting
  const sections = document.querySelectorAll('section[id], header[id]');
  const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

  function highlightNav() {
    let current = '';
    sections.forEach((section) => {
      const top = section.offsetTop - 120;
      if (window.scrollY >= top) {
        current = section.getAttribute('id');
      }
    });

    navAnchors.forEach((anchor) => {
      anchor.style.color = anchor.getAttribute('href') === '#' + current
        ? 'var(--text-primary)'
        : '';
    });
  }

  window.addEventListener('scroll', highlightNav, { passive: true });

  // Stagger stat cards
  document.querySelectorAll('.stat-card').forEach((card, i) => {
    card.style.transitionDelay = (i * 0.1) + 's';
  });

  document.querySelectorAll('.paper-card').forEach((card, i) => {
    card.style.transitionDelay = (i * 0.08) + 's';
  });
})();
