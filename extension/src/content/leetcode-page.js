// Content Script for LeetCode Page Event Interception

console.log('[LeetCode Analytics] Content Script Loaded.');

// Listen for submission result DOM changes or Network events
function observeSubmissionResult() {
  const targetNode = document.querySelector('[data-e2e-locator="submission-result"]') || document.body;
  if (!targetNode) return;

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      const text = mutation.target.textContent || '';
      if (text.includes('Accepted') || text.includes('Wrong Answer') || text.includes('Time Limit Exceeded')) {
        const slug = window.location.pathname.split('/')[2] || 'unknown';
        chrome.runtime.sendMessage({
          action: 'NEW_SUBMISSION_EVENT',
          data: {
            problem_id: 1,
            title_slug: slug,
            result: text.includes('Accepted') ? 'Accepted' : (text.includes('Wrong Answer') ? 'Wrong Answer' : 'Time Limit Exceeded'),
            language: 'cpp'
          }
        });
      }
    });
  });

  observer.observe(targetNode, { childList: true, subtree: true });
}

if (document.readyState === 'complete') {
  observeSubmissionResult();
} else {
  window.addEventListener('load', observeSubmissionResult);
}
