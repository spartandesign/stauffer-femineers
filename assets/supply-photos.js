// Native disclosures and image links work without JavaScript. Enhance photo
// links with one reusable modal; keep source links as ordinary external links.
(() => {
  if (!document.querySelector('.supply-photo-link')) return;
  const dialog = document.createElement('dialog');
  if (typeof dialog.showModal !== 'function') return;
  dialog.className = 'supply-photo-dialog no-print';
  dialog.setAttribute('aria-labelledby', 'supply-photo-title');
  dialog.setAttribute('aria-describedby', 'supply-photo-description');
  dialog.innerHTML = `<div class="supply-photo-dialog-header"><h2 id="supply-photo-title"></h2><button type="button" class="supply-photo-close" autofocus>Close</button></div><span class="supply-photo-kind"></span><img class="supply-photo-large" alt=""><p id="supply-photo-description"></p><p class="supply-photo-source"></p>`;
  document.body.append(dialog);
  const title = dialog.querySelector('h2');
  const kind = dialog.querySelector('.supply-photo-kind');
  const image = dialog.querySelector('img');
  const description = dialog.querySelector('#supply-photo-description');
  const source = dialog.querySelector('.supply-photo-source');
  let opener;

  document.addEventListener('click', (event) => {
    if (!(event.target instanceof Element)) return;
    const link = event.target.closest('.supply-photo-link');
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const card = link.closest('.supply-photo-card');
    const thumbnail = link.querySelector('img');
    opener = link;
    title.textContent = card.querySelector('.supply-photo-name').textContent;
    kind.textContent = card.querySelector('.supply-photo-kind').textContent;
    description.textContent = card.querySelector('.supply-photo-note').textContent;
    source.replaceChildren(...Array.from(card.querySelector('.supply-photo-source').childNodes, node => node.cloneNode(true)));
    image.src = link.href;
    image.alt = thumbnail.alt;
    dialog.showModal();
    document.body.classList.add('photo-modal-open');
  });

  dialog.querySelector('.supply-photo-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  // Native Escape cancellation fires close, keeping focus and scroll consistent.
  dialog.addEventListener('close', () => {
    document.body.classList.remove('photo-modal-open');
    opener?.focus({preventScroll: true});
    image.removeAttribute('src');
  });
})();
