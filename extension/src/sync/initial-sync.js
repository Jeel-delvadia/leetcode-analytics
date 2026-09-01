// Fast Parallelized Initial Synchronization Module with CSRF Header Support

const LEETCODE_GRAPHQL_URL = 'https://leetcode.com/graphql';

const QUERY = `
  query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
      categorySlug: $categorySlug
      limit: $limit
      skip: $skip
      filters: $filters
    ) {
      total: totalNum
      questions: questions {
        frontendQuestionId: questionFrontendId
        title
        titleSlug
        difficulty
        acRate
        isPaidOnly
        topicTags {
          name
          slug
        }
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

async function fetchProblemBatch(skip, limit = 100) {
  const csrfToken = await getCsrfToken();
  const headers = { 
    'Content-Type': 'application/json' 
  };
  if (csrfToken) {
    headers['x-csrftoken'] = csrfToken;
  }

  try {
    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        operationName: 'problemsetQuestionList',
        query: QUERY,
        variables: { categorySlug: '', skip, limit, filters: {} }
      })
    });
    const json = await res.json();
    return json.data?.problemsetQuestionList || { total: 0, questions: [] };
  } catch (err) {
    console.error('Fetch batch error:', err);
    return { total: 0, questions: [] };
  }
}

export async function fetchAllProblemsFast(limit = 100, onProgress = null) {
  const firstBatch = await fetchProblemBatch(0, limit);
  const totalNum = firstBatch.total || 0;
  let allProblems = [];

  if (firstBatch.questions && firstBatch.questions.length > 0) {
    firstBatch.questions.forEach(q => {
      allProblems.push(formatQuestion(q));
    });
  }

  if (onProgress) {
    onProgress(allProblems.length, totalNum);
  }

  if (totalNum > 0) {
    const skips = [];
    for (let s = limit; s < totalNum; s += limit) {
      skips.push(s);
    }

    const CHUNK_SIZE = 5;
    for (let i = 0; i < skips.length; i += CHUNK_SIZE) {
      const chunkSkips = skips.slice(i, i + CHUNK_SIZE);
      const results = await Promise.all(chunkSkips.map(s => fetchProblemBatch(s, limit)));
      
      results.forEach(res => {
        if (res.questions) {
          res.questions.forEach(q => allProblems.push(formatQuestion(q)));
        }
      });

      if (onProgress) {
        onProgress(allProblems.length, totalNum);
      }
    }
  }

  return allProblems;
}

function formatQuestion(q) {
  return {
    problem_id: parseInt(q.frontendQuestionId, 10) || Math.floor(Math.random() * 10000),
    frontend_id: q.frontendQuestionId,
    title: q.title,
    title_slug: q.titleSlug,
    difficulty: q.difficulty,
    acceptance_rate: parseFloat((q.acRate || 0).toFixed(3)),
    total_submissions: null,
    total_accepted: null,
    is_paid: q.isPaidOnly,
    problem_url: `https://leetcode.com/problems/${q.titleSlug}/`,
    topics: q.topicTags ? q.topicTags.map(t => t.name) : []
  };
}

export async function fetchUserContestRanking(username) {
  if (!username) return [];

  const query = `
    query userContestRankingInfo($username: String!) {
      userContestRankingHistory(username: $username) {
        attended
        rating
        ranking
        problemsSolved
        contest {
          title
          startTime
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
        operationName: 'userContestRankingInfo',
        query: query,
        variables: { username }
      })
    });
    const json = await res.json();
    const history = json.data?.userContestRankingHistory || [];
    return history.filter(h => h.attended).map((h, idx) => ({
      contest_id: idx + 1,
      contest_name: h.contest.title,
      contest_slug: h.contest.title.toLowerCase().replace(/\s+/g, '-'),
      contest_date: new Date(h.contest.startTime * 1000).toISOString(),
      contest_type: 'Weekly',
      attended: h.attended,
      rank: h.ranking,
      rating_after: h.rating,
      problems_solved: h.problemsSolved
    }));
  } catch (err) {
    console.warn('Contest ranking fetch error:', err);
    return [];
  }
}
