/* Tiammomo Portfolio — Interactions */

document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('[data-header]');
  const navToggle = document.querySelector('.header-nav-toggle');
  const navLinks = document.querySelectorAll('.header-nav a');
  const filters = document.querySelectorAll('[data-filter]');
  const copyBtn = document.querySelector('[data-copy]');
  const yearEl = document.querySelector('[data-year]');
  const projectGrid = document.querySelector('[data-project-grid]');

  const escapeHtml = (value) =>
    String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');

  const localized = (value, locale) => {
    if (!value || typeof value !== 'object') return value ?? '';
    return value[locale] ?? value.zh ?? value.en ?? '';
  };

  const currentFilter = () =>
    document.querySelector('[data-filter].is-active')?.dataset.filter ?? 'all';

  const applyProjectFilter = (selected = currentFilter()) => {
    document.querySelectorAll('.project-card').forEach((card) => {
      const categories = card.dataset.category.split(' ');
      card.classList.toggle(
        'is-hidden',
        selected !== 'all' && !categories.includes(selected),
      );
    });
  };

  const renderProjectCard = (project, index, locale) => {
    const caseLabel = locale === 'en' ? 'Case Study' : '案例详情';
    const liveLabel = localized(project.liveLabel, locale) || (locale === 'en' ? 'Live Demo' : '在线体验');
    const githubLabel = 'GitHub';
    const categories = project.categories.join(' ');
    const status = localized(project.availability, locale) || (project.status === 'wip' ? 'WIP' : 'Active');
    const statusAttr = escapeHtml(project.status);
    const alt = escapeHtml(localized(project.image.alt, locale));
    const summary = escapeHtml(localized(project.summary, locale));
    const meta = localized(project.meta, locale);
    const imageSource = project.image.webp
      ? `<source srcset="${escapeHtml(project.image.webp)}" type="image/webp" />`
      : '';
    const caseLink = project.caseUrl
      ? `<a class="project-link" href="${escapeHtml(project.caseUrl)}">${caseLabel} →</a>`
      : '';
    const liveLink = project.liveUrl
      ? `<a class="project-link" href="${escapeHtml(project.liveUrl)}" rel="noreferrer">${liveLabel} →</a>`
      : '';
    const githubLink = project.githubUrl
      ? `<a class="project-link project-link-muted" href="${escapeHtml(project.githubUrl)}" rel="noreferrer">${githubLabel} →</a>`
      : '';

    return `
      <article class="project-card" data-category="${escapeHtml(categories)}">
        <div class="project-card-top">
          <span class="project-num">${String(index + 1).padStart(2, '0')}</span>
          <span class="project-status" data-status="${statusAttr}"><span class="status-dot"></span> ${status}</span>
        </div>
        <figure class="project-card-media">
          <picture>
            ${imageSource}
            <img src="${escapeHtml(project.image.png)}" alt="${alt}" loading="lazy" />
          </picture>
        </figure>
        <h3 class="project-name">${escapeHtml(project.name)}</h3>
        <p class="project-desc">${summary}</p>
        <div class="project-tags">
          ${project.tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
        </div>
        <div class="project-meta">
          ${meta.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}
        </div>
        <div class="project-actions">
          ${caseLink}
          ${liveLink}
          ${githubLink}
        </div>
      </article>
    `;
  };

  const renderProjects = async () => {
    if (!projectGrid) return;

    try {
      const response = await fetch('data/projects.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`Project data failed: ${response.status}`);
      const projects = await response.json();
      const locale = projectGrid.dataset.locale || 'zh';
      projectGrid.innerHTML = projects
        .map((project, index) => renderProjectCard(project, index, locale))
        .join('');
      applyProjectFilter();
    } catch (error) {
      console.warn('Using static project cards fallback.', error);
    }
  };

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 20);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  if (header && navToggle) {
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

    navLinks.forEach((link) => link.addEventListener('click', closeNav));
  }

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      const selected = button.dataset.filter;
      filters.forEach((item) => item.classList.toggle('is-active', item === button));
      applyProjectFilter(selected);
    });
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const value = copyBtn.dataset.copy;
      const label = copyBtn.textContent.trim();
      const copiedLabel = copyBtn.dataset.copiedLabel || '已复制';
      try {
        await navigator.clipboard.writeText(value);
        copyBtn.textContent = copiedLabel;
        setTimeout(() => (copyBtn.textContent = label), 1400);
      } catch {
        location.href = value.includes('@') ? `mailto:${value}` : value;
      }
    });
  }

  const sections = document.querySelectorAll('main section[id]');
  if (sections.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            navLinks.forEach((link) =>
              link.classList.toggle('is-active', link.getAttribute('href') === `#${id}`),
            );
          }
        });
      },
      { threshold: 0.3, rootMargin: '-64px 0px -50% 0px' },
    );
    sections.forEach((section) => observer.observe(section));
  }

  renderProjects();
});
