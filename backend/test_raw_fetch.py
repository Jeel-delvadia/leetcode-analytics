import os
import json
import urllib.request
from datetime import datetime, timezone

DEBUG_RAW_DIR = os.path.join(os.path.dirname(__file__), "debug", "raw")

def verify_raw_leetcode_fetch():
    print("=== STAGE 1 & 2: RAW LEETCODE FETCH VERIFICATION ===")
    
    url = "https://leetcode.com/graphql"
    query = """
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
    """

    req = urllib.request.Request(
        url,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(f"HTTP error {resp.getcode()}")
        
        raw_json = json.loads(resp.read().decode())
        if "errors" in raw_json:
            raise RuntimeError(f"GraphQL errors: {raw_json['errors']}")

        questions = raw_json.get("data", {}).get("allQuestions", [])
        print(f"[STAGE 1 SUCCESS] Fetched {len(questions)} real LeetCode questions.")

        # Save to debug/raw/problems/
        prob_dir = os.path.join(DEBUG_RAW_DIR, "problems")
        os.makedirs(prob_dir, exist_ok=True)
        raw_path = os.path.join(prob_dir, f"problems_raw_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_json, f, indent=2)

        print(f"[STAGE 2 SUCCESS] Saved raw GraphQL response to: {raw_path}")
        print("Sample Question 1 Raw Fields:", json.dumps(questions[0], indent=2))
        return raw_path

if __name__ == "__main__":
    verify_raw_leetcode_fetch()
