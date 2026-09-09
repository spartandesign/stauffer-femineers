// Optional browser QA: requires Playwright and Microsoft Edge.
const { chromium } = require('playwright');
const { readdirSync, mkdirSync } = require('node:fs');
const { resolve, join } = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');

(async () => {
  const root = resolve(__dirname, '..');
  const out = join(root, 'tmp', 'navigation-qa');
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const errors = [];
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    const go = file => page.goto(pathToFileURL(join(root, file.split('#')[0])).href + (file.includes('#') ? '#' + file.split('#')[1] : ''));
    for (const file of readdirSync(root).filter(name => name.endsWith('.html'))) {
      await go(file);
      assert.deepEqual(await page.locator('#main-nav a').allTextContents(), ['Home', 'My Project', 'Tutorials', 'Mentors'], file);
    }
    for (const width of [1366, 768, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      for (const file of ['index.html', 'my-project.html', 'wearables-project.html', 'robotics-project.html', 'tutorials.html', 'mentors.html']) {
        await go(file);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${file}: overflow at ${width}`);
        if (width <= 900) {
          await page.locator('.nav-toggle').click();
          assert.equal(await page.locator('.nav-toggle').getAttribute('aria-expanded'), 'true');
          assert(await page.getByRole('link', { name: 'Tutorials', exact: true }).isVisible());
          await page.keyboard.press('Escape');
          assert.equal(await page.locator('.nav-toggle').getAttribute('aria-expanded'), 'false');
        }
      }
    }
    await go('wearables-project.html');
    await page.locator('#november-16 > summary').click();
    await page.locator('#november-16').getByRole('link', { name: 'Open the full pathway guide', exact: true }).click();
    assert(page.url().endsWith('/wearable-build.html'));
    assert(await page.getByRole('navigation', { name: 'Breadcrumb' }).getByRole('link', { name: 'Wearables', exact: true }).isVisible());
    await go('mentors.html#january-25');
    assert.equal(await page.locator('#january-25').getAttribute('open'), '');
    await page.locator('#mentor-session').selectOption('february-22');
    assert.equal(await page.locator('#february-22').getAttribute('open'), '');
    assert(page.url().endsWith('#february-22'));
    await go('tutorials.html');
    const total = await page.locator('[data-tutorial]').count();
    await page.locator('#tutorial-query').fill('micro:bit');
    assert(await page.locator('[data-tutorial]:visible').count() > 0);
    assert(await page.locator('[data-tutorial]:visible').count() < total);
    await page.locator('#tutorial-query').fill('no-results-xyz');
    assert(await page.locator('#tutorial-empty').isVisible());
    await page.locator('#tutorial-query').fill('');
    assert.equal(await page.locator('[data-tutorial]:visible').count(), total);
    await page.setViewportSize({ width: 1366, height: 1100 });
    for (const file of ['index', 'wearables-project', 'mentors', 'tutorials']) {
      await go(file + '.html');
      await page.screenshot({ path: join(out, file + '-desktop.png'), fullPage: true });
    }
    await page.setViewportSize({ width: 390, height: 1000 });
    await go('wearables-project.html');
    await page.screenshot({ path: join(out, 'student-mobile.png'), fullPage: true });
    const nojs = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 1000 } });
    await nojs.goto(pathToFileURL(join(root, 'tutorials.html')).href);
    assert.equal(await nojs.locator('#main-nav a:visible').count(), 4);
    assert.equal(await nojs.locator('[data-tutorial]:visible').count(), total);
    await nojs.goto(pathToFileURL(join(root, 'wearables-project.html')).href);
    await nojs.locator('#november-16 > summary').click();
    assert(await nojs.locator('#november-16 .detail-body').isVisible());
    assert.deepEqual(errors, []);
    console.log(`PASS: all site menus, desktop/tablet/mobile layouts, workday-to-guide journey, mentor deep links, tutorial search (${total} guides), keyboard menu dismissal, and no-JavaScript access.`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
