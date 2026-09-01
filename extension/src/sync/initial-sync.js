// Live LeetCode Data & User Progress Sync

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
    }
  }
`;

const USER_STATUS_QUERY = `
  query userStatus {
    userStatus {
      username
      userSlug
      isSignedIn
    }
  }
`;

const USER_PROGRESS_QUERY = `
  query userProfileUserQuestionProgressV2($userSlug: String!) {
    userProfileUserQuestionProgressV2(userSlug: $userSlug) {
      numAcceptedQuestions {
        count
        difficulty
      }
      numFailedQuestions {
        count
        difficulty
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

  try {
    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ operationName: 'allQuestions', query: ALL_QUESTIONS_QUERY, variables: {} })
    });
    const json = await res.json();
    questions = json.data?.allQuestions || [];
    if (onProgress) onProgress(questions.length, questions.length);
  } catch (err) {
    console.error('Failed to fetch questions:', err);
  }

  return questions.map(q => ({
    problem_id: parseInt(q.questionFrontendId || q.questionId, 10),
    frontend_id: q.questionFrontendId || String(q.questionId),
    title: q.title,
    title_slug: q.titleSlug,
    difficulty: q.difficulty,
    acceptance_rate: 50.0,
    total_submissions: null,
    total_accepted: null,
    is_paid: q.isPaidOnly || false,
    problem_url: `https://leetcode.com/problems/${q.titleSlug}/`,
    topics: []
  }));
}

export async function fetchUserSubmissionHistory(offset = 0, limit = 100) {
  const query = `
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

  try {
    const csrfToken = await getCsrfToken();
    const headers = { 'Content-Type': 'application/json' };
    if (csrfToken) headers['x-csrftoken'] = csrfToken;

    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        operationName: 'submissionList',
        query: query,
        variables: { offset, limit }
      })
    });
    const json = await res.json();
    const subs = json.data?.submissionList?.submissions || [];
    return subs.map(s => ({
      submission_id: parseInt(s.id, 10),
      title_slug: s.titleSlug,
      submitted_at: new Date(parseInt(s.timestamp, 10) * 1000).toISOString(),
      result: s.statusDisplay,
      language: s.lang,
      runtime_ms: parseInt((s.runtime || '0').replace(' ms', ''), 10) || 0,
      memory_kb: parseInt((s.memory || '0').replace(' MB', ''), 10) * 1024 || 0
    }));
  } catch (err) {
    console.warn('Submission history fetch error:', err);
    return [];
  }
}

export async function fetchUserContestRanking(username) {
  return [];
}
