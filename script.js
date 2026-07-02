/* Tiammomo Portfolio — Interactions */

document.addEventListener('DOMContentLoaded', () => {
  const legacyVisualLineRedirects = {
    '#visual-line-app': 'writing/app-development.html#visual-line-app',
    '#visual-line-infra': 'writing/infra.html#visual-line-infra',
    '#visual-line-inference': 'writing/inference.html#visual-line-inference',
    '#visual-line-algorithm': 'writing/algorithm.html#visual-line-algorithm',
  };

  const legacyTarget = legacyVisualLineRedirects[window.location.hash];
  if (legacyTarget && /(?:^|\/)writing\.html$/.test(window.location.pathname)) {
    window.location.replace(new URL(legacyTarget, window.location.href).href);
    return;
  }

  const header = document.querySelector('[data-header]');
  const navToggle = document.querySelector('.header-nav-toggle');
  const navLinks = document.querySelectorAll('.header-nav a');
  const filters = document.querySelectorAll('[data-filter]');
  const copyBtn = document.querySelector('[data-copy]');
  const yearEl = document.querySelector('[data-year]');
  const projectGrid = document.querySelector('[data-project-grid]');
  const projectIndex = document.querySelector('[data-project-index]');
  const statsSection = document.querySelector('[data-profile-stats]');
  const jsonCache = new Map();

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

  const loadJson = (source) => {
    if (!source) return Promise.reject(new Error('Missing JSON source'));
    if (!jsonCache.has(source)) {
      const request = fetch(source, { cache: 'no-store' })
        .then((response) => {
          if (!response.ok) throw new Error(`${source} failed: ${response.status}`);
          return response.json();
        })
        .catch((error) => {
          jsonCache.delete(source);
          throw error;
        });
      jsonCache.set(source, request);
    }
    return jsonCache.get(source);
  };

  const formatStatNumber = (value) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '';
    return new Intl.NumberFormat(document.documentElement.lang || 'zh-CN').format(numeric);
  };

  const currentFilter = () =>
    document.querySelector('[data-filter].is-active')?.dataset.filter ?? 'all';

  const applyProjectFilter = (selected = currentFilter()) => {
    document.querySelectorAll('.project-card, [data-project-index-row]').forEach((item) => {
      const categories = (item.dataset.category || '').split(' ');
      item.classList.toggle(
        'is-hidden',
        selected !== 'all' && !categories.includes(selected),
      );
    });
  };

  const withBase = (ref, base = '') => {
    if (!ref || /^(https?:|mailto:|tel:|#|\/)/.test(ref)) return ref;
    return `${base}${ref}`;
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
    const urlBase = projectGrid?.dataset.urlBase || '';
    const imageSource = project.image.webp
      ? `<source srcset="${escapeHtml(withBase(project.image.webp, urlBase))}" type="image/webp" />`
      : '';
    const caseLink = project.caseUrl
      ? `<a class="project-link" href="${escapeHtml(withBase(project.caseUrl, urlBase))}">${caseLabel} →</a>`
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
            <img src="${escapeHtml(withBase(project.image.png, urlBase))}" alt="${alt}" loading="lazy" />
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

  const renderProjectIndexRow = (project, locale) => {
    const urlBase = projectIndex?.dataset.urlBase || '';
    const categories = project.categories.join(' ');
    const status = localized(project.availability, locale) || (project.status === 'wip' ? 'WIP' : 'Active');
    const direction = localized(project.index?.direction, locale) || localized(project.meta, locale).join(' / ');
    const proof = localized(project.index?.proof, locale) || localized(project.summary, locale);
    const caseUrl = project.caseUrl ? withBase(project.caseUrl, urlBase) : '';
    const caseLabel = locale === 'en' ? 'Case' : '案例';

    return `
      <div class="archive-row" role="row" data-project-index-row data-category="${escapeHtml(categories)}">
        <strong>${escapeHtml(project.name)}</strong>
        <span>${escapeHtml(direction)}</span>
        <span>${escapeHtml(status)}</span>
        <span>${escapeHtml(proof)}</span>
        ${caseUrl ? `<a href="${escapeHtml(caseUrl)}">${caseLabel} →</a>` : '<span>--</span>'}
      </div>
    `;
  };

  const renderProjectIndex = async () => {
    if (!projectIndex) return;

    try {
      const source = projectIndex.dataset.projectSrc || projectGrid?.dataset.projectSrc || 'data/projects.json';
      const projects = await loadJson(source);
      const locale = projectIndex.dataset.locale || 'zh';
      const headers = locale === 'en'
        ? ['Project', 'Direction', 'Status', 'Proof', 'Entry']
        : ['项目', '方向', '状态', '可信度', '入口'];

      projectIndex.innerHTML = `
        <div class="archive-row archive-row--head" role="row">
          ${headers.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}
        </div>
        ${projects.map((project) => renderProjectIndexRow(project, locale)).join('')}
      `;
      applyProjectFilter();
    } catch (error) {
      console.warn('Project index failed.', error);
    }
  };

  const renderProjects = async () => {
    if (!projectGrid) return;

    try {
      const source = projectGrid.dataset.projectSrc || 'data/projects.json';
      const projects = await loadJson(source);
      const locale = projectGrid.dataset.locale || 'zh';
      projectGrid.innerHTML = projects
        .map((project, index) => renderProjectCard(project, index, locale))
        .join('');
      applyProjectFilter();
    } catch (error) {
      console.warn('Using static project cards fallback.', error);
    }
  };

  const renderStats = async () => {
    if (!statsSection) return;

    const statsSource = statsSection.dataset.statsSrc || 'data/profile-stats.json';
    const projectSource = statsSection.dataset.projectSrc || projectGrid?.dataset.projectSrc || 'data/projects.json';

    try {
      const [profileStats, projects] = await Promise.all([
        loadJson(statsSource),
        loadJson(projectSource).catch(() => null),
      ]);
      const snapshot = profileStats.stats || {};
      const values = {
        publicRepos: snapshot.publicRepos,
        selectedProjects: Array.isArray(projects) ? projects.length : snapshot.selectedProjects,
        totalStars: snapshot.totalStars,
        authoredPublicPullRequests: snapshot.authoredPublicPullRequests,
      };

      statsSection.querySelectorAll('[data-stat-value]').forEach((item) => {
        const key = item.dataset.statValue;
        const formatted = formatStatNumber(values[key]);
        if (formatted) item.textContent = formatted;
      });
    } catch (error) {
      console.warn('Using static stats fallback.', error);
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

  renderStats();
  renderProjects();
  renderProjectIndex();
});
