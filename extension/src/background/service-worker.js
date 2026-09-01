// Background Service Worker for Manifest V3

import { fetchAllProblemsFast, fetchUserSubmissionHistory, fetchUserContestRanking } from '../sync/initial-sync.js';
import { sendInitialSyncData, sendIncrementalSubmission } from '../api/backend.js';

chrome.runtime.onInstalled.addListener(() => {
  console.log('LeetCode Analytics Collector Service Worker Installed.');
  chrome.storage.local.set({ syncStatus: 'IDLE', lastSyncTime: null, progressText: '' });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'TRIGGER_FULL_SYNC') {
    handleFullSync()
      .then(result => sendResponse({ status: 'SUCCESS', result }))
      .catch(error => sendResponse({ status: 'FAILED', error: error.message }));
    return true;
  }

  if (request.action === 'NEW_SUBMISSION_EVENT') {
    handleNewSubmission(request.data)
      .then(result => sendResponse({ status: 'SUCCESS', result }))
      .catch(error => sendResponse({ status: 'FAILED', error: error.message }));
    return true;
  }
});

async function handleFullSync() {
  chrome.storage.local.set({ syncStatus: 'RUNNING', progressText: 'Fetching problems...' });
  try {
    const problems = await fetchAllProblemsFast(100, (fetched, total) => {
      const progress = `Fetching problems: ${fetched} / ${total}`;
      chrome.storage.local.set({ progressText: progress });
    });

    chrome.storage.local.set({ progressText: 'Fetching user submission history...' });

    // Map slug to problem_id
    const slugMap = new Map();
    problems.forEach(p => slugMap.set(p.title_slug, p.problem_id));

    // Fetch user actual submission history from LeetCode
    const rawSubmissions = await fetchUserSubmissionHistory(0, 100);
    const userSubmissions = [];

    rawSubmissions.forEach(sub => {
      const pid = slugMap.get(sub.title_slug) || 1;
      userSubmissions.push({
        submission_id: sub.submission_id,
        problem_id: pid,
        submitted_at: sub.submitted_at,
        result: sub.result,
        language: sub.language,
        runtime_ms: sub.runtime_ms,
        memory_kb: sub.memory_kb
      });
    });

    const payload = {
      sync_type: 'INITIAL',
      problems: problems,
      submissions: userSubmissions,
      contests: []
    };

    chrome.storage.local.set({ progressText: 'Sending payload to backend...' });

    const res = await sendInitialSyncData(payload);
    const now = new Date().toISOString();
    chrome.storage.local.set({ 
      syncStatus: 'SUCCESS', 
      lastSyncTime: now, 
      recordsFetched: res.records_fetched,
      progressText: `Complete! ${res.records_fetched} records & ${userSubmissions.length} user submissions synced.` 
    });
    return res;
  } catch (err) {
    chrome.storage.local.set({ syncStatus: 'FAILED', error: err.message, progressText: `Error: ${err.message}` });
    throw err;
  }
}

async function handleNewSubmission(submissionData) {
  const response = await sendIncrementalSubmission({
    submission_id: submissionData.submission_id || Date.now(),
    problem_id: submissionData.problem_id || 1,
    title_slug: submissionData.title_slug || 'two-sum',
    submitted_at: new Date().toISOString(),
    result: submissionData.result || 'Accepted',
    language: submissionData.language || 'cpp',
    runtime_ms: submissionData.runtime_ms || 0,
    memory_kb: submissionData.memory_kb || 0
  });
  return response;
}
