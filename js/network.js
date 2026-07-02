/**
 * Interactive network visualization for hero section
 * Represents research concept interconnections
 */

(function () {
  const canvas = document.getElementById('network-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height, nodes, animationId;
  let mouse = { x: -1000, y: -1000 };

  const CONCEPTS = [
  { label: 'GenAI', color: '#3ecfbd' },
  { label: 'Cognition', color: '#c9a55c' },
  { label: 'Innovation', color: '#e8c878' },
  { label: 'Learning', color: '#8b7fd4' },
  { label: 'Alliances', color: '#e87d8f' },
  { label: 'Leadership', color: '#c9a55c' },
  { label: 'Strategy', color: '#3ecfbd' },
  { label: 'Analytics', color: '#9ba3b4' },
  ];

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = canvas.parentElement.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    initNodes();
  }

  function initNodes() {
    const count = window.innerWidth < 768 ? 28 : 48;
    nodes = [];

    for (let i = 0; i < count; i++) {
      const concept = CONCEPTS[i % CONCEPTS.length];
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 2.5 + 1.5,
        color: concept.color,
        alpha: Math.random() * 0.5 + 0.3,
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    const connectionDist = window.innerWidth < 768 ? 100 : 140;

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < connectionDist) {
          const alpha = (1 - dist / connectionDist) * 0.15;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(201, 165, 92, ${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    const centerX = width / 2;
    const centerY = height / 2;

    nodes.forEach((node) => {
      const dx = mouse.x - node.x;
      const dy = mouse.y - node.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < 120 && dist > 0) {
        const force = (120 - dist) / 120 * 0.02;
        node.vx -= (dx / dist) * force;
        node.vy -= (dy / dist) * force;
      }

      const cdx = centerX - node.x;
      const cdy = centerY - node.y;
      const cdist = Math.sqrt(cdx * cdx + cdy * cdy);
      if (cdist > 50) {
        node.vx += (cdx / cdist) * 0.003;
        node.vy += (cdy / cdist) * 0.003;
      }

      node.x += node.vx;
      node.y += node.vy;

      node.vx *= 0.99;
      node.vy *= 0.99;

      if (node.x < 0 || node.x > width) node.vx *= -1;
      if (node.y < 0 || node.y > height) node.vy *= -1;

      node.x = Math.max(0, Math.min(width, node.x));
      node.y = Math.max(0, Math.min(height, node.y));

      const gradient = ctx.createRadialGradient(
        node.x, node.y, 0,
        node.x, node.y, node.radius * 3
      );
      gradient.addColorStop(0, node.color.replace(')', `, ${node.alpha})`).replace('rgb', 'rgba').replace('#', ''));
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = node.color;
      ctx.globalAlpha = node.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    });

    animationId = requestAnimationFrame(draw);
  }

  function onMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  }

  function onMouseLeave() {
    mouse.x = -1000;
    mouse.y = -1000;
  }

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function start() {
    resize();
    if (!prefersReducedMotion.matches) {
      draw();
    } else {
      ctx.clearRect(0, 0, width, height);
      nodes.forEach((node) => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.globalAlpha = node.alpha * 0.5;
        ctx.fill();
        ctx.globalAlpha = 1;
      });
    }
  }

  window.addEventListener('resize', () => {
    cancelAnimationFrame(animationId);
    start();
  });

  canvas.addEventListener('mousemove', onMouseMove);
  canvas.addEventListener('mouseleave', onMouseLeave);

  canvas.addEventListener('touchmove', (e) => {
    if (e.touches.length) {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.touches[0].clientX - rect.left;
      mouse.y = e.touches[0].clientY - rect.top;
    }
  }, { passive: true });

  start();
})();
