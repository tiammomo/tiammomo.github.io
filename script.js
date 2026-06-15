/* Tiammomo Portfolio — Interactions */

document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('[data-header]');
  const navToggle = document.querySelector('.header-nav-toggle');
  const navLinks = document.querySelectorAll('.header-nav a');
  const filters = document.querySelectorAll('[data-filter]');
  const projects = document.querySelectorAll('.project-card');
  const copyBtn = document.querySelector('[data-copy]');
  const yearEl = document.querySelector('[data-year]');

  // ── Year ──
  yearEl.textContent = new Date().getFullYear();

  // ── Header scroll state ──
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 20);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  // ── Mobile nav ──
  const closeNav = () => {
    document.body.classList.remove('nav-lock');
    header.classList.remove('nav-open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const open = navToggle.getAttribute('aria-expanded') === 'true';
    document.body.classList.toggle('nav-lock', !open);
    header.classList.toggle('nav-open', !open);
    navToggle.setAttribute('aria-expanded', String(!open));
  });

  navLinks.forEach(link => link.addEventListener('click', closeNav));

  // ── Project filters ──
  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      const sel = btn.dataset.filter;
      filters.forEach(f => f.classList.toggle('is-active', f === btn));
      projects.forEach(card => {
        const cats = card.dataset.category.split(' ');
        card.classList.toggle('is-hidden', sel !== 'all' && !cats.includes(sel));
      });
    });
  });

  // ── Copy contact ──
  copyBtn.addEventListener('click', async () => {
    const val = copyBtn.dataset.copy;
    const label = copyBtn.textContent.trim();
    const copiedLabel = copyBtn.dataset.copiedLabel || '已复制';
    try {
      await navigator.clipboard.writeText(val);
      copyBtn.textContent = copiedLabel;
      setTimeout(() => (copyBtn.textContent = label), 1400);
    } catch {
      location.href = val.includes('@') ? `mailto:${val}` : val;
    }
  });

  // ── Active nav tracking ──
  const sections = document.querySelectorAll('main section[id]');
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          navLinks.forEach(link =>
            link.classList.toggle('is-active', link.getAttribute('href') === `#${id}`)
          );
        }
      });
    },
    { threshold: 0.3, rootMargin: '-64px 0px -50% 0px' }
  );
  sections.forEach(s => observer.observe(s));
});
