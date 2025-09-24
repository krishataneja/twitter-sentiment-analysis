from numpy import save
from playwright.sync_api import sync_playwright
from pprint import pprint
import json
import time

def scrape_tweets_about(query="mrbeast", max_tweets=10):
    tweets_data = []
    seen_texts = set()

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
                                    legacy = result.get('legacy', {})
                                    user = result.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
                                    tweet_text = legacy.get('full_text')

                                    if not tweet_text or tweet_text in seen_texts:
                                        continue
                                    seen_texts.add(tweet_text)

                                    tweets_data.append({
                                        "user": user.get("screen_name", None),
                                        "text": tweet_text,
                                        "created_at": legacy.get("created_at", ""),
                                        "retweet_count": legacy.get("retweet_count", 0),
                                        "like_count": legacy.get("favorite_count", 0)
                                    })

                                    if len(tweets_data) >= max_tweets:
                                        return
                                except Exception as inner_error:
                                    print(" Skipped one tweet due to unexpected format.")
            except Exception as e:
                print("parsing error", e)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.on("response", intercept_response)

        print("🚀 Opening Twitter search page...")
        page.goto(f"https://x.com/search?q={query}&src=typed_query&f=live")

        try:
            print("waiting")
            page.wait_for_selector("article", timeout=120000)
            print("waiting..")
            time.sleep(30)
        except:
            print("timeout")

        print(f"collected {len(tweets_data)} tweets.")
        return tweets_data

if __name__ == "__main__":
    data = scrape_tweets_about("mrbeast", max_tweets=10)
    pprint(data)

    with open("tweets_about_mrbeast.json", "w") as f:
        json.dump(data, f, indent=4)
    print("data saved")