// Initial Synchronization Module

const LEETCODE_GRAPHQL_URL = 'https://leetcode.com/graphql';

export async function fetchAllProblems(limit = 100) {
  let skip = 0;
  let hasMore = true;
  const allProblems = [];

  const query = `
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

  while (hasMore) {
    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        operationName: 'problemsetQuestionList',
        query: query,
        variables: {
          categorySlug: '',
          skip: skip,
          limit: limit,
          filters: {}
        }
      })
    });

    const json = await res.json();
    const data = json.data?.problemsetQuestionList;
    if (!data || !data.questions || data.questions.length === 0) {
      hasMore = false;
      break;
    }

    data.questions.forEach(q => {
      allProblems.push({
        problem_id: parseInt(q.frontendQuestionId, 10),
        frontend_id: q.frontendQuestionId,
        title: q.title,
        title_slug: q.titleSlug,
        difficulty: q.difficulty,
        acceptance_rate: parseFloat(q.acRate.toFixed(3)),
        total_submissions: null,
        total_accepted: null,
        is_paid: q.isPaidOnly,
        problem_url: `https://leetcode.com/problems/${q.titleSlug}/`,
        topics: q.topicTags ? q.topicTags.map(t => t.name) : []
      });
    });

    skip += limit;
    if (skip >= data.total) {
      hasMore = false;
    }
  }

  return allProblems;
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
    const res = await fetch(LEETCODE_GRAPHQL_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
