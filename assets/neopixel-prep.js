const copyStarter = document.querySelector('#copy-starter');
const starterCode = document.querySelector('#starter-code');
const copyStatus = document.querySelector('#copy-status');

if (copyStarter && starterCode && copyStatus) {
  copyStarter.hidden = false;
  copyStarter.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(starterCode.textContent);
      copyStatus.textContent = 'Copied. Paste into MakeCode JavaScript after adding the neopixel extension.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(starterCode);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      copyStatus.textContent = 'Code selected. Press Ctrl+C or Command+C to copy, or use the download.';
    }
  });
}
