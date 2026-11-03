/* Efectos visuales de Adivinator: partículas, tipeo, ondas, confeti. */
(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Partículas flotantes ---------- */
  const canvas = document.getElementById('particles');
  if (canvas && !reduceMotion) {
    const ctx = canvas.getContext('2d');
    let w, h, particles = [];
    const COLORS = ['57,255,136', '178,107,255', '40,215,255'];
    const resize = () => {
      w = canvas.width = innerWidth;
      h = canvas.height = innerHeight;
      particles = Array.from({ length: Math.min(90, w / 14) }, () => ({
        x: Math.random() * w, y: Math.random() * h,
        r: Math.random() * 2 + .6,
        vx: (Math.random() - .5) * .35, vy: -(Math.random() * .4 + .15),
        c: COLORS[Math.floor(Math.random() * COLORS.length)],
        a: Math.random() * Math.PI * 2,
      }));
    };
    const mouse = { x: -999, y: -999 };
    addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
    addEventListener('resize', resize);
    resize();
    (function frame() {
      ctx.clearRect(0, 0, w, h);
      for (const p of particles) {
        p.a += .02;
        p.x += p.vx + Math.sin(p.a) * .2;
        p.y += p.vy;
        const dx = p.x - mouse.x, dy = p.y - mouse.y, d = Math.hypot(dx, dy);
        if (d < 120) { p.x += dx / d * 1.5; p.y += dy / d * 1.5; }
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        if (p.x < -10) p.x = w + 10; else if (p.x > w + 10) p.x = -10;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.c},${.5 + Math.sin(p.a) * .3})`;
        ctx.shadowBlur = 12; ctx.shadowColor = `rgb(${p.c})`;
        ctx.fill();
      }
      requestAnimationFrame(frame);
    })();
  }

  /* ---------- Efecto de tipeo en el título ---------- */
  const typed = document.querySelector('[data-typewriter]');
  if (typed) {
    const text = typed.textContent.trim();
    const html = typed.innerHTML.trim();
    if (reduceMotion) {
      typed.innerHTML = html;
    } else {
      typed.innerHTML = '<span class="cursor"></span>';
      const cursor = typed.firstChild;
      const orb = document.querySelector('.orb');
      orb?.classList.add('thinking');
      let i = 0;
      const tick = () => {
        if (i < text.length) {
          cursor.insertAdjacentText('beforebegin', text[i++]);
          setTimeout(tick, 28 + Math.random() * 40);
        } else {
          typed.innerHTML = html;
          orb?.classList.remove('thinking');
          document.querySelectorAll('.opciones .btn, #Newanimal').forEach(el => el.classList.add('ready'));
        }
      };
      setTimeout(tick, 300);
    }
  }

  /* ---------- Onda al hacer clic en botones ---------- */
  document.addEventListener('click', e => {
    const btn = e.target.closest('.btn');
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const r = document.createElement('span');
    r.className = 'ripple';
    r.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - rect.left - size / 2}px;top:${e.clientY - rect.top - size / 2}px`;
    btn.appendChild(r);
    r.addEventListener('animationend', () => r.remove());
  });

  /* ---------- Confeti ---------- */
  if (document.body.dataset.confetti && !reduceMotion) {
    const colors = ['#39ff88', '#b26bff', '#28d7ff', '#ffd452', '#ff5aa0'];
    for (let i = 0; i < 120; i++) {
      const c = document.createElement('i');
      c.className = 'confetti';
      c.style.cssText = `left:${Math.random() * 100}vw;background:${colors[i % colors.length]};
        animation-duration:${2.5 + Math.random() * 2}s;animation-delay:${Math.random() * .8}s;
        transform:rotate(${Math.random() * 360}deg);border-radius:${Math.random() > .5 ? '50%' : '2px'}`;
      document.body.appendChild(c);
      c.addEventListener('animationend', () => c.remove());
    }
  }

  /* ---------- Contador animado ---------- */
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = +el.dataset.count;
    if (reduceMotion || target === 0) { el.textContent = target; return; }
    const start = performance.now(), dur = 1200;
    const step = now => {
      const t = Math.min(1, (now - start) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });

  /* ---------- Aparición escalonada de nodos del árbol ---------- */
  document.querySelectorAll('.tree li').forEach((li, i) => {
    li.style.animationDelay = `${Math.min(i * 60, 1500)}ms`;
  });
})();
