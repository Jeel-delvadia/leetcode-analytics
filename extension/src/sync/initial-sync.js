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

  // 2. Fetch User Profile Progress if signed in
  let userSubmissions = [];
  try {
    const statusRes = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ operationName: 'userStatus', query: USER_STATUS_QUERY })
    });
    const statusJson = await statusRes.json();
    const username = statusJson.data?.userStatus?.username || statusJson.data?.userStatus?.userSlug;

    if (username) {
      const progRes = await fetch(LEETCODE_GRAPHQL_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          operationName: 'userProfileUserQuestionProgressV2',
          query: USER_PROGRESS_QUERY,
          variables: { userSlug: username }
        })
      });
      const progJson = await progRes.json();
      const acceptedList = progJson.data?.userProfileUserQuestionProgressV2?.numAcceptedQuestions || [];
      
      // Store user solved summary in window / storage
      chrome.storage.local.set({ userProgressSummary: acceptedList });
    }
  } catch (e) {
    console.warn('User profile progress fetch error:', e);
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

export async function fetchUserContestRanking(username) {
  return [];
}
