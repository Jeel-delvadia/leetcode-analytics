// Background Service Worker for Manifest V3 - NO FALLBACK OR FABRICATED VALUES

import { fetchAllProblemsFast, fetchUserSubmissionHistory } from '../sync/initial-sync.js';
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
  chrome.storage.local.set({ syncStatus: 'RUNNING', progressText: 'Fetching authentic problems from LeetCode...' });
  try {
    const { raw_response: rawProblems, problems } = await fetchAllProblemsFast(100, (fetched, total) => {
      chrome.storage.local.set({ progressText: `Fetching problems: ${fetched} / ${total}` });
    });

    chrome.storage.local.set({ progressText: 'Fetching user authentic submission history...' });

    // Map title_slug to problem_id
    const slugMap = new Map();
    problems.forEach(p => {
      if (p.title_slug && p.problem_id) {
        slugMap.set(p.title_slug, p.problem_id);
      }
    });

    const { raw_response: rawSubmissions, submissions: rawSubs } = await fetchUserSubmissionHistory(0, 100);
    const userSubmissions = [];

    rawSubs.forEach(sub => {
      const pid = slugMap.get(sub.title_slug);
      if (pid) {
        userSubmissions.push({
          submission_id: sub.submission_id,
          problem_id: pid,
          submitted_at: sub.submitted_at,
          result: sub.result,
          language: sub.language,
          runtime_ms: sub.runtime_ms,
          memory_kb: sub.memory_kb
        });
      } else {
        console.warn(`[INGEST] Skipping submission ${sub.submission_id}: title_slug '${sub.title_slug}' not found in problem map.`);
      }
    });

    const payload = {
      sync_type: 'INITIAL',
      problems: problems,
      submissions: userSubmissions,
      contests: [],
      raw_problems_response: rawProblems,
      raw_submissions_response: rawSubmissions
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
  if (!submissionData.submission_id || !submissionData.problem_id) {
    throw new Error("Invalid submission event payload: missing submission_id or problem_id.");
  }

  const response = await sendIncrementalSubmission({
    submission_id: submissionData.submission_id,
    problem_id: submissionData.problem_id,
    title_slug: submissionData.title_slug || null,
    submitted_at: new Date().toISOString(),
    result: submissionData.result || null,
    language: submissionData.language || null,
    runtime_ms: submissionData.runtime_ms || null,
    memory_kb: submissionData.memory_kb || null
  });
  return response;
}
