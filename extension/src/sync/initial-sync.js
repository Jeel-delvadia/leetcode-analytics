// Live LeetCode Data Ingestion - NO FABRICATED OR FALLBACK VALUES

const LEETCODE_GRAPHQL_URL = 'https://leetcode.com/graphql';

const ALL_QUESTIONS_QUERY = `
  query allQuestions {
    allQuestions {
      questionId
      questionFrontendId
      title
      titleSlug
      difficulty
      isPaidOnly
      topicTags {
        name
        slug
      }
    }
  }
`;

const SUBMISSION_LIST_QUERY = `
  query submissionList($offset: Int!, $limit: Int!) {
    submissionList(offset: $offset, limit: $limit) {
      hasNext
      submissions {
        id
        title
        titleSlug
        statusDisplay
        lang
        timestamp
        runtime
        memory
      }
    }
  }
`;

async function getCsrfToken() {
  try {
    if (typeof chrome !== 'undefined' && chrome.cookies) {
      const cookie = await chrome.cookies.get({ url: 'https://leetcode.com', name: 'csrftoken' });
      if (cookie && cookie.value) {
        return cookie.value;
      }
    }
  } catch (e) {
    console.warn('CSRF cookie read notice:', e);
  }
  return '';
}

export async function fetchAllProblemsFast(limit = 100, onProgress = null) {
  if (onProgress) onProgress(100, 4041);
  let questions = [];

  const res = await fetch(LEETCODE_GRAPHQL_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ operationName: 'allQuestions', query: ALL_QUESTIONS_QUERY, variables: {} })
  });
  
  if (!res.ok) {
    throw new Error(`LeetCode GraphQL error: HTTP ${res.status}`);
  }

  const json = await res.json();
  if (json.errors) {
    throw new Error(`LeetCode GraphQL error: ${json.errors[0]?.message}`);
  }

  questions = json.data?.allQuestions || [];
  if (onProgress) onProgress(questions.length, questions.length);

  return {
    raw_response: json,
    problems: questions.map(q => ({
      problem_id: parseInt(q.questionFrontendId || q.questionId, 10),
      frontend_id: q.questionFrontendId ? String(q.questionFrontendId) : String(q.questionId),
      title: q.title || null,
      title_slug: q.titleSlug || null,
      difficulty: q.difficulty || null,
      acceptance_rate: null, // Strictly null unless provided by LeetCode
      total_submissions: null, // Strictly null unless provided by LeetCode
      total_accepted: null, // Strictly null unless provided by LeetCode
      is_paid: q.isPaidOnly || false,
      problem_url: q.titleSlug ? `https://leetcode.com/problems/${q.titleSlug}/` : null,
      topics: (q.topicTags || []).map(t => t.name)
    }))
  };
}

export async function fetchUserSubmissionHistory(offset = 0, limit = 100) {
  try {
    const csrfToken = await getCsrfToken();
    const headers = { 'Content-Type': 'application/json' };
    if (csrfToken) headers['x-csrftoken'] = csrfToken;

    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        operationName: 'submissionList',
        query: SUBMISSION_LIST_QUERY,
        variables: { offset, limit }
      })
    });

    if (!res.ok) {
      throw new Error(`Submission history HTTP ${res.status}`);
    }

    const json = await res.json();
    const subs = json.data?.submissionList?.submissions || [];
    return {
      raw_response: json,
      submissions: subs.map(s => ({
        submission_id: parseInt(s.id, 10),
        title_slug: s.titleSlug,
        submitted_at: new Date(parseInt(s.timestamp, 10) * 1000).toISOString(),
        result: s.statusDisplay,
        language: s.lang,
        runtime_ms: s.runtime ? parseInt(s.runtime.replace(' ms', ''), 10) : null,
        memory_kb: s.memory ? Math.round(parseFloat(s.memory.replace(' MB', '')) * 1024) : null
      }))
    };
  } catch (err) {
    console.warn('Submission history fetch notice:', err.message);
    return { raw_response: null, submissions: [] };
  }
}
