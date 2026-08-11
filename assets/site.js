const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');

// Keep recruitment prominent until the roster is selected. Change this to
// false after recruitment closes and the final roster is announced.
const recruitmentActive = true;

if (recruitmentActive && !document.body.classList.contains('recruitment-form-page')) {
  const recruitmentBanner = document.createElement('aside');
  recruitmentBanner.className = 'recruitment-banner no-print';
  recruitmentBanner.setAttribute('aria-label', 'Femineers recruitment is open');
  recruitmentBanner.innerHTML = '<div><strong>Join Stauffer Femineers</strong><span>Applications open August 18–September 4 · 50 spaces</span></div><a href="recruitment.html">Explore and apply →</a>';
  document.body.insertBefore(recruitmentBanner, document.body.firstChild);
  document.body.classList.add('recruitment-active');
}

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
}

document.querySelectorAll('[data-year]').forEach((item) => {
  item.textContent = new Date().getFullYear();
});

document.querySelectorAll('[data-print]').forEach((button) => {
  button.addEventListener('click', () => window.print());
});
