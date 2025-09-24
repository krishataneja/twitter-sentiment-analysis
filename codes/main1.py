from playwright.sync_api import sync_playwright
from pprint import pprint
import json
import time

def scrape_profile_info(url): 
    _xhr_calls = []

    def intercept_response(response):
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)  
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.on("response", intercept_response)

        print(" Opening profile page...")
        page.goto(url)

        try:
            page.wait_for_selector("[data-testid='primaryColumn']", timeout=15000)
            time.sleep(5)  
        except:
            print(" Timeout waiting for profile to load.")

        usercalls = [f for f in _xhr_calls if "UserBy" in f.url]

        if not usercalls:
            print(" No user info found — the page may not have loaded fully.")
            return None

        for uc in usercalls:
            try:
                data = uc.json()
                return data['data']['user']['result']
            except Exception as e:
                print(" Error parsing user info:", e)

        print("No profile info returned.")
        return None


if __name__ == "__main__":
    profile_data = scrape_profile_info("https://x.com/MrBeast")

    if profile_data:
        pprint(json.dumps(profile_data, indent=2))
    else:
        print("Failed to retrieve profile info.")
        
with open("mrbeast.json", "w") as f:
    json.dump(scrape_profile_info("https://x.com/MrBeast"), f, indent=4)