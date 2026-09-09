const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');

if (toggle && nav) {
  document.body.classList.add('nav-ready');
  toggle.hidden = false;
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  };
  toggle.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      setMenu(false);
      toggle.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target) && !toggle.contains(event.target)) setMenu(false);
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', () => setMenu(false));
}

// Deep links open any enclosing disclosures, including links from Canvas.
const revealHash = () => {
  if (!location.hash) return;
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  for (let element = target; element; element = element.parentElement) {
    if (element.tagName === 'DETAILS') element.open = true;
  }
  requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
};
window.addEventListener('hashchange', revealHash);
revealHash();

const sessionPicker = document.querySelector('#mentor-session');
if (sessionPicker) {
  sessionPicker.parentElement.hidden = false;
  if ([...sessionPicker.options].some((option) => option.value === location.hash.slice(1))) {
    sessionPicker.value = location.hash.slice(1);
  }
  sessionPicker.addEventListener('change', () => {
    document.querySelectorAll('.mentor-session').forEach((session) => {
      session.open = session.id === sessionPicker.value;
    });
    location.hash = sessionPicker.value;
    revealHash();
  });
}

const tutorialQuery = document.querySelector('#tutorial-query');
if (tutorialQuery) {
  document.querySelector('.tutorial-search').hidden = false;
  const entries = [...document.querySelectorAll('[data-tutorial]')];
  const normalize = (text) => text.toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  const updateTopics = () => {
    const terms = normalize(tutorialQuery.value).split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach((entry) => {
      const category = entry.closest('.tutorial-category').getAttribute('aria-label');
      const text = normalize(`${category} ${entry.textContent}`);
      entry.hidden = !terms.every((term) => text.includes(term));
      if (!entry.hidden) count += 1;
    });
    document.querySelectorAll('.tutorial-category').forEach((category) => {
      category.hidden = ![...category.querySelectorAll('[data-tutorial]')].some((entry) => !entry.hidden);
    });
    document.querySelector('#tutorial-count').textContent = `${count} of ${entries.length} guides`;
    document.querySelector('#tutorial-empty').hidden = count !== 0;
  };
  tutorialQuery.addEventListener('input', updateTopics);
  updateTopics();
}

document.querySelectorAll('[data-year]').forEach((item) => {
  item.textContent = new Date().getFullYear();
});

document.querySelectorAll('[data-print]').forEach((button) => {
  button.addEventListener('click', () => window.print());
});
