// Backend API Client for Extension

const BACKEND_BASE_URL = 'http://localhost:8000/api/v1';

export async function sendInitialSyncData(payload) {
  const res = await fetch(`${BACKEND_BASE_URL}/sync/initial`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`Failed to send initial sync data: ${res.statusText}`);
  }
  return await res.json();
}

export async function sendIncrementalSubmission(submissionData) {
  const res = await fetch(`${BACKEND_BASE_URL}/sync/submission`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(submissionData)
  });
  if (!res.ok) {
    throw new Error(`Failed to send submission: ${res.statusText}`);
  }
  return await res.json();
}

export async function getSyncStatus() {
  const res = await fetch(`${BACKEND_BASE_URL}/sync/status`);
  if (!res.ok) {
    throw new Error(`Failed to fetch sync status: ${res.statusText}`);
  }
  return await res.json();
}
