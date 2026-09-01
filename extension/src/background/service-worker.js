// Background Service Worker for Manifest V3

import { fetchAllProblems, fetchUserContestRanking } from '../sync/initial-sync.js';
import { sendInitialSyncData, sendIncrementalSubmission } from '../api/backend.js';

chrome.runtime.onInstalled.addListener(() => {
  console.log('LeetCode Analytics Collector Service Worker Installed.');
  chrome.storage.local.set({ syncStatus: 'IDLE', lastSyncTime: null });
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
  chrome.storage.local.set({ syncStatus: 'RUNNING' });
  try {
    const problems = await fetchAllProblems(100);
    const contests = await fetchUserContestRanking('user');

    const payload = {
      sync_type: 'INITIAL',
      problems: problems,
      submissions: [],
      contests: contests
    };

    const res = await sendInitialSyncData(payload);
    const now = new Date().toISOString();
    chrome.storage.local.set({ syncStatus: 'SUCCESS', lastSyncTime: now, recordsFetched: res.records_fetched });
    return res;
  } catch (err) {
    chrome.storage.local.set({ syncStatus: 'FAILED', error: err.message });
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
