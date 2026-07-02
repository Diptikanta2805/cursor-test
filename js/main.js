/**
 * Diptikanta Panigrahi — Personal Academic Website
 * Interactive features: network canvas, attention lab, scroll reveals
 */

(function () {
  'use strict';

  // ─── Utilities ───────────────────────────────────────────
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  // ─── Navigation ──────────────────────────────────────────
  const nav = $('#nav');
  const navToggle = $('#navToggle');
  const navLinks = $('#navLinks');

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });

  navToggle?.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
  });

  $$('.nav-links a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  // ─── Cursor Glow ─────────────────────────────────────────
  const glow = $('.cursor-glow');
  if (glow && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mousemove', (e) => {
      glow.style.left = e.clientX + 'px';
      glow.style.top = e.clientY + 'px';
    }, { passive: true });
  }

  // ─── Morphing Hero Text ──────────────────────────────────
  const morphText = $('#morphText');
  const phrases = [
    'Strategic Cognition',
    'Generative AI Strategy',
    'Innovation Capabilities',
    'Executive Attention',
    'Organizational Learning',
    'Data-Driven Strategy'
  ];
  let phraseIdx = 0;

  function cyclePhrase() {
    if (!morphText) return;
    morphText.style.opacity = '0';
    setTimeout(() => {
      phraseIdx = (phraseIdx + 1) % phrases.length;
      morphText.textContent = phrases[phraseIdx];
      morphText.style.opacity = '1';
    }, 400);
  }

  setInterval(cyclePhrase, 3200);

  // ─── Network Canvas (Hero) ───────────────────────────────
  const networkCanvas = $('#networkCanvas');
  if (networkCanvas) {
    const ctx = networkCanvas.getContext('2d');
    let nodes = [];
    let mouse = { x: -1000, y: -1000 };
    let animId;

    const nodeLabels = [
      'TMT Cognition', 'GenAI', 'Innovation', 'Alliances',
      'Attention', 'Learning', 'Leadership', 'Strategy'
    ];

    function resizeNetwork() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = networkCanvas.parentElement.getBoundingClientRect();
      networkCanvas.width = rect.width * dpr;
      networkCanvas.height = rect.height * dpr;
      networkCanvas.style.width = rect.width + 'px';
      networkCanvas.style.height = rect.height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      initNodes(rect.width, rect.height);
    }

    function initNodes(w, h) {
      const count = Math.min(12, Math.floor((w * h) / 45000));
      nodes = Array.from({ length: count }, (_, i) => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: 2 + Math.random() * 3,
        label: nodeLabels[i % nodeLabels.length],
        pulse: Math.random() * Math.PI * 2
      }));
    }

    function drawNetwork() {
      const w = networkCanvas.width / (window.devicePixelRatio || 1);
      const h = networkCanvas.height / (window.devicePixelRatio || 1);

      ctx.clearRect(0, 0, w, h);

      // Update positions
      nodes.forEach(n => {
        n.x += n.vx;
        n.y += n.vy;
        n.pulse += 0.02;

        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;

        // Mouse attraction
        const dx = mouse.x - n.x;
        const dy = mouse.y - n.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 200 && dist > 0) {
          n.vx += dx / dist * 0.015;
          n.vy += dy / dist * 0.015;
        }

        // Damping
        n.vx *= 0.995;
        n.vy *= 0.995;
      });

      // Draw connections
      const maxDist = 160;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < maxDist) {
            const alpha = (1 - dist / maxDist) * 0.25;
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.strokeStyle = `rgba(201, 162, 39, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }

      // Draw nodes
      nodes.forEach(n => {
        const glow = 0.5 + Math.sin(n.pulse) * 0.3;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r + 4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(201, 162, 39, ${glow * 0.15})`;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(201, 162, 39, ${0.6 + glow * 0.4})`;
        ctx.fill();
      });

      animId = requestAnimationFrame(drawNetwork);
    }

    networkCanvas.parentElement.addEventListener('mousemove', (e) => {
      const rect = networkCanvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }, { passive: true });

    networkCanvas.parentElement.addEventListener('mouseleave', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });

    resizeNetwork();
    drawNetwork();
    window.addEventListener('resize', resizeNetwork);
  }

  // ─── Attention Allocation Lab ────────────────────────────
  const coreSlider = $('#coreSlider');
  const supportSlider = $('#supportSlider');
  const allianceSlider = $('#allianceSlider');
  const attentionCanvas = $('#attentionCanvas');

  if (coreSlider && attentionCanvas) {
    const coreVal = $('#coreValue');
    const supportVal = $('#supportValue');
    const allianceVal = $('#allianceValue');
    const totalEl = $('#totalAllocation');
    const insightText = $('#insightText');

    const insights = {
      balanced: 'Balanced allocation with alliance emphasis — exploratory firms in my research achieve higher returns when partnerships complement core implementation.',
      coreHeavy: 'Core-heavy allocation signals deep operational integration. My AOM 2025 study finds core-function GenAI implementation amplifies value for innovation-capable firms.',
      supportHeavy: 'Support-function focus may limit market value gains. Firms allocating GenAI primarily to back-office functions see diminished abnormal returns in my S&P 500 analysis.',
      allianceHeavy: 'Alliance-dominant strategy — strategic partnerships can substitute for internal innovation capabilities when orchestrating GenAI adoption.',
      overAllocated: 'Attention exceeds capacity. Like executives facing bandwidth constraints, total allocation over 100 suggests strategic spread — focus may generate higher returns.',
      underAllocated: 'Unallocated attention represents strategic ambiguity. Markets reward decisive GenAI implementation backed by clear resource orchestration.'
    };

    function getInsight(core, support, alliance, total) {
      if (total > 100) return insights.overAllocated;
      if (total < 100) return insights.underAllocated;
      if (alliance > 45) return insights.allianceHeavy;
      if (core > 50) return insights.coreHeavy;
      if (support > 45) return insights.supportHeavy;
      return insights.balanced;
    }

    function normalizeSliders(changed) {
      let core = +coreSlider.value;
      let support = +supportSlider.value;
      let alliance = +allianceSlider.value;
      let total = core + support + alliance;

      if (total > 100) {
        const excess = total - 100;
        const others = ['core', 'support', 'alliance'].filter(s => s !== changed);
        const o1 = others[0] === 'core' ? core : others[0] === 'support' ? support : alliance;
        const o2 = others[1] === 'core' ? core : others[1] === 'support' ? support : alliance;
        const sum = o1 + o2 || 1;
        const reduce1 = Math.round(excess * (o1 / sum));
        const reduce2 = excess - reduce1;

        if (others[0] === 'core') core = Math.max(0, core - reduce1);
        else if (others[0] === 'support') support = Math.max(0, support - reduce1);
        else alliance = Math.max(0, alliance - reduce1);

        if (others[1] === 'core') core = Math.max(0, core - reduce2);
        else if (others[1] === 'support') support = Math.max(0, support - reduce2);
        else alliance = Math.max(0, alliance - reduce2);

        coreSlider.value = core;
        supportSlider.value = support;
        allianceSlider.value = alliance;
      }

      return { core: +coreSlider.value, support: +supportSlider.value, alliance: +allianceSlider.value };
    }

    function drawAttentionViz(core, support, alliance) {
      const canvas = attentionCanvas;
      const actx = canvas.getContext('2d');
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      actx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const w = rect.width;
      const h = rect.height;
      const cx = w / 2;
      const cy = h / 2;
      const total = core + support + alliance || 1;

      actx.clearRect(0, 0, w, h);

      const segments = [
        { value: core, color: '#c9a227', label: 'Core' },
        { value: support, color: '#4a7c9b', label: 'Support' },
        { value: alliance, color: '#3d8b7a', label: 'Alliances' }
      ];

      // Donut chart
      const outerR = Math.min(w, h) * 0.35;
      const innerR = outerR * 0.55;
      let startAngle = -Math.PI / 2;

      segments.forEach(seg => {
        const slice = (seg.value / total) * Math.PI * 2;
        if (slice <= 0) return;

        actx.beginPath();
        actx.arc(cx, cy, outerR, startAngle, startAngle + slice);
        actx.arc(cx, cy, innerR, startAngle + slice, startAngle, true);
        actx.closePath();
        actx.fillStyle = seg.color + 'cc';
        actx.fill();
        actx.strokeStyle = seg.color;
        actx.lineWidth = 2;
        actx.stroke();

        // Label
        const midAngle = startAngle + slice / 2;
        const labelR = (outerR + innerR) / 2;
        const lx = cx + Math.cos(midAngle) * labelR;
        const ly = cy + Math.sin(midAngle) * labelR;
        const pct = Math.round((seg.value / total) * 100);

        if (pct > 8) {
          actx.fillStyle = '#f0ece4';
          actx.font = '600 13px Instrument Sans, sans-serif';
          actx.textAlign = 'center';
          actx.textBaseline = 'middle';
          actx.fillText(pct + '%', lx, ly);
        }

        startAngle += slice;
      });

      // Center text
      actx.fillStyle = '#f0ece4';
      actx.font = '600 14px Instrument Sans, sans-serif';
      actx.textAlign = 'center';
      actx.fillText('Attention', cx, cy - 8);
      actx.font = '400 12px Instrument Sans, sans-serif';
      actx.fillStyle = '#9a958a';
      actx.fillText('Allocation', cx, cy + 10);

      // Orbiting particles
      const time = Date.now() * 0.001;
      segments.forEach((seg, i) => {
        const angle = time + i * 2.1;
        const r = outerR + 20 + Math.sin(time * 2 + i) * 8;
        const px = cx + Math.cos(angle) * r;
        const py = cy + Math.sin(angle) * r;
        actx.beginPath();
        actx.arc(px, py, 3, 0, Math.PI * 2);
        actx.fillStyle = seg.color;
        actx.fill();
      });
    }

    function updateLab(changed) {
      const { core, support, alliance } = normalizeSliders(changed);
      const total = core + support + alliance;

      coreVal.textContent = core;
      supportVal.textContent = support;
      allianceVal.textContent = alliance;
      totalEl.textContent = total;

      totalEl.classList.remove('over', 'under');
      if (total > 100) totalEl.classList.add('over');
      else if (total < 100) totalEl.classList.add('under');

      insightText.textContent = getInsight(core, support, alliance, total);
      drawAttentionViz(core, support, alliance);
    }

    coreSlider.addEventListener('input', () => updateLab('core'));
    supportSlider.addEventListener('input', () => updateLab('support'));
    allianceSlider.addEventListener('input', () => updateLab('alliance'));
    window.addEventListener('resize', () => updateLab(null));

    // Animate attention canvas
    function animateAttention() {
      drawAttentionViz(+coreSlider.value, +supportSlider.value, +allianceSlider.value);
      requestAnimationFrame(animateAttention);
    }
    animateAttention();
    updateLab(null);
  }

  // ─── Counter Animation ───────────────────────────────────
  function animateCounters() {
    $$('[data-count]').forEach(el => {
      if (el.dataset.animated) return;
      const target = +el.dataset.count;
      const duration = 1800;
      const start = performance.now();

      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased);
        if (progress < 1) requestAnimationFrame(tick);
        else el.dataset.animated = 'true';
      }

      requestAnimationFrame(tick);
    });
  }

  // ─── Scroll Reveal ───────────────────────────────────────
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        if (entry.target.querySelector('[data-count]')) {
          animateCounters();
        }
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  $$('.timeline-item, .pillar-card, .pub-card, .teaching-card, .section-header').forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });

  $$('.timeline-item').forEach(el => revealObserver.observe(el));

  // ─── Contact Form ────────────────────────────────────────
  const contactForm = $('#contactForm');
  contactForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = $('#name').value.trim();
    const email = $('#email').value.trim();
    const message = $('#message').value.trim();
    const subject = encodeURIComponent(`Job Market Inquiry from ${name}`);
    const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`);
    window.location.href = `mailto:diptikanta@ku.edu?subject=${subject}&body=${body}`;
  });

  // ─── Footer Year ─────────────────────────────────────────
  const yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
