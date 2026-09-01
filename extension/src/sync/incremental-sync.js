// Incremental Sync Module for New Submissions

import { sendIncrementalSubmission } from '../api/backend.js';

export async function processNewSubmissionEvent(submissionPayload) {
  try {
    const formattedPayload = {
      submission_id: submissionPayload.submission_id || Date.now(),
      problem_id: submissionPayload.problem_id,
      title_slug: submissionPayload.title_slug,
      submitted_at: new Date().toISOString(),
      result: submissionPayload.result,
      language: submissionPayload.language || 'cpp',
      runtime_ms: submissionPayload.runtime_ms || 0,
      memory_kb: submissionPayload.memory_kb || 0
    };

    const response = await sendIncrementalSubmission(formattedPayload);
    return response;
  } catch (error) {
    console.error('Failed incremental sync:', error);
    throw error;
  }
}
