document.addEventListener('DOMContentLoaded', () => {
  const syncBtn = document.getElementById('syncBtn');
  const statusEl = document.getElementById('status');

  // Load status from background storage
  chrome.storage.local.get(['syncStatus', 'lastSyncTime'], (data) => {
    if (data.syncStatus) {
      statusEl.textContent = data.syncStatus;
    }
  });

  syncBtn.addEventListener('click', () => {
    statusEl.textContent = 'Syncing...';
    chrome.runtime.sendMessage({ action: 'TRIGGER_FULL_SYNC' }, (response) => {
      if (response && response.status === 'SUCCESS') {
        statusEl.textContent = 'Sync Complete!';
      } else {
        statusEl.textContent = 'Sync Failed';
      }
    });
  });
});
