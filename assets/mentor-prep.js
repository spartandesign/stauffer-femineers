const copyButton = document.querySelector('[data-copy-code]');
const code = document.querySelector('#starter-code');
const status = document.querySelector('#copy-status');
if (copyButton && code && status) {
  copyButton.hidden = false;
  copyButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = 'Copied. Paste into the JavaScript view of a new MakeCode project, then choose Blocks.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Code selected. Press Ctrl+C or Command+C, or use the download link.';
    }
  });
}
