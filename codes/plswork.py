from playwright.sync_api import sync_playwright
import json
import time

SEARCH_QUERY = '("LG TV" OR "LG AC" OR "LG refrigerator" OR "LG customer service" OR "LG Electronics") India -from:LGIndia -from:LG_Global since:2022-05-01 until:2023-01-01'
MAX_TWEETS = 1000

def scrape_lg_tweets():
    tweets = []
    seen_ids = set()

    def intercept_response(response):
        if "SearchTimeline" in response.url and response.request.resource_type == "xhr":
            try:
                data = response.json()
                instructions = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
                for instruction in instructions:
                    if 'entries' in instruction:
                        for entry in instruction['entries']:
                            if entry['entryId'].startswith("tweet-"):
                                try:
                                    result = entry['content']['itemContent']['tweet_results']['result']
                                    legacy = result.get("legacy", {})
                                    user = result.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {})
                                    tweet_id = legacy.get("id_str")
                                    if tweet_id in seen_ids:
                                        continue
                                    seen_ids.add(tweet_id)

                                    tweets.append({
                                        "user": user.get("screen_name"),
                                        "text": legacy.get("full_text"),
                                        "created_at": legacy.get("created_at"),
                                        "retweet_count": legacy.get("retweet_count"),
                                        "like_count": legacy.get("favorite_count")
                                    })
                                except:
                                    continue
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.on("response", intercept_response)

        print("page open")
        page.goto("https://twitter.com/login")
        page.wait_for_timeout(30000)  # 30 secs

       
        if "login" in page.url:
            print("login failed.")
            return

        search_url = f"https://twitter.com/search?q={SEARCH_QUERY.replace(' ', '%20')}&src=typed_query&f=live"
        print("xyz")
        page.goto(search_url)
        page.wait_for_timeout(10000) 

        print("abc")
        scroll_attempts = 0
        while len(tweets) < MAX_TWEETS and scroll_attempts < 100:
            page.mouse.wheel(0, 3000)
            time.sleep(1.5)
            scroll_attempts += 1
            print(f"collected: {len(tweets)} tweets...", end="\r")

        browser.close()

    print(f"final number of tweets collected: {len(tweets)}")

    with open("tweets11", "w") as f:
        json.dump(tweets[:MAX_TWEETS], f, indent=2)

    print("📁 Saved to 'lg_dualcool_tweets.json'")

if __name__ == "__main__":
    scrape_lg_tweets()

