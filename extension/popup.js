document.addEventListener('DOMContentLoaded', () => {
  const syncBtn = document.getElementById('syncBtn');
  const statusEl = document.getElementById('status');
  const progressEl = document.getElementById('progress');

  function updateUI() {
    chrome.storage.local.get(['syncStatus', 'progressText'], (data) => {
      if (data.syncStatus) statusEl.textContent = data.syncStatus;
      if (data.progressText) progressEl.textContent = data.progressText;
    });
  }

  updateUI();
  const timer = setInterval(updateUI, 500);

  syncBtn.addEventListener('click', () => {
    statusEl.textContent = 'Syncing...';
    progressEl.textContent = 'Starting fast parallel sync...';
    chrome.runtime.sendMessage({ action: 'TRIGGER_FULL_SYNC' }, (response) => {
      updateUI();
      if (response && response.status === 'SUCCESS') {
        statusEl.textContent = 'Complete!';
      } else {
        statusEl.textContent = 'Failed';
      }
    });
  });
});
