/* Constellation canvas — interactive particle network in hero */

(function () {
  const canvas = document.getElementById('constellation');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  let mouse = { x: -1000, y: -1000 };
  let animationId;

  const PARTICLE_COUNT = 80;
  const CONNECTION_DIST = 140;
  const MOUSE_DIST = 180;

  const COLORS = {
    particle: 'rgba(232, 0, 45, 0.7)',
    particleDim: 'rgba(201, 168, 76, 0.5)',
    line: 'rgba(232, 0, 45, 0.12)',
    lineBright: 'rgba(201, 168, 76, 0.25)',
    mouse: 'rgba(45, 212, 191, 0.3)',
  };

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = canvas.width = rect.width;
    height = canvas.height = rect.height;
  }

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.radius = Math.random() * 1.5 + 0.5;
      this.isGold = Math.random() > 0.7;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      const dx = mouse.x - this.x;
      const dy = mouse.y - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < MOUSE_DIST) {
        const force = (MOUSE_DIST - dist) / MOUSE_DIST * 0.02;
        this.vx -= dx * force;
        this.vy -= dy * force;
      }

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      this.x = Math.max(0, Math.min(width, this.x));
      this.y = Math.max(0, Math.min(height, this.y));

      this.vx *= 0.99;
      this.vy *= 0.99;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.isGold ? COLORS.particleDim : COLORS.particle;
      ctx.fill();
    }
  }

  function init() {
    resize();
    particles = Array.from({ length: PARTICLE_COUNT }, () => new Particle());
  }

  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONNECTION_DIST) {
          const alpha = 1 - dist / CONNECTION_DIST;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = particles[i].isGold || particles[j].isGold
            ? `rgba(201, 168, 76, ${alpha * 0.2})`
            : `rgba(232, 0, 45, ${alpha * 0.12})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }

      const mdx = mouse.x - particles[i].x;
      const mdy = mouse.y - particles[i].y;
      const mDist = Math.sqrt(mdx * mdx + mdy * mdy);

      if (mDist < MOUSE_DIST) {
        const alpha = 1 - mDist / MOUSE_DIST;
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.strokeStyle = `rgba(45, 212, 191, ${alpha * 0.3})`;
        ctx.lineWidth = 0.8;
        ctx.stroke();
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach(p => { p.update(); p.draw(); });
    drawConnections();
    animationId = requestAnimationFrame(animate);
  }

  canvas.parentElement.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  canvas.parentElement.addEventListener('mouseleave', () => {
    mouse.x = -1000;
    mouse.y = -1000;
  });

  window.addEventListener('resize', () => {
    resize();
    particles.forEach(p => p.reset());
  });

  init();
  animate();
})();
