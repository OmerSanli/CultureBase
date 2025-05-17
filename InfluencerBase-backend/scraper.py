from playwright.sync_api import sync_playwright
import re
import time

def scrape_instagram_profile(username, max_posts=10):
    data = {
        "total_likes": 0,
        "total_comments": 0,
        "total_views": 0,
        "post_count": 0,
        "reel_count": 0,
        "collaboration_count": 0,
        "posts": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = f"https://www.instagram.com/{username}/"
        page.goto(url, timeout=60000)
        page.wait_for_selector("article", timeout=10000)

        post_links = page.eval_on_selector_all(
            "article a",
            "els => els.map(e => e.href)"
        )
        post_links = list(dict.fromkeys(post_links))[:max_posts]  # remove duplicates

        for post_url in post_links:
            try:
                page.goto(post_url, timeout=60000)
                page.wait_for_selector("time", timeout=10000)
                time.sleep(1.5)

                is_video = "reel" in post_url or bool(page.query_selector("video"))
                caption = page.inner_text("div[role='dialog'] ul li span") if page.query_selector("div[role='dialog'] ul li span") else ""
                likes = 0
                comments = 0
                views = 0

                if is_video:
                    view_span = page.query_selector("span:has-text('Görüntüleme')")
                    if view_span:
                        views_text = view_span.inner_text().split()[0].replace(".", "").replace(",", "")
                        if views_text.isdigit():
                            views = int(views_text)
                else:
                    like_button = page.query_selector("section span")
                    if like_button:
                        like_text = like_button.inner_text().replace(".", "").replace(",", "")
                        if like_text.isdigit():
                            likes = int(like_text)

                comment_blocks = page.query_selector_all("ul > li")[1:]
                comments = len(comment_blocks)

                data["post_count"] += 0 if is_video else 1
                data["reel_count"] += 1 if is_video else 0
                data["total_likes"] += likes
                data["total_comments"] += comments
                data["total_views"] += views

                has_collab = "işbirliği" in caption.lower()
                mentions = re.findall(r"@\w+", caption)

                if has_collab:
                    data["collaboration_count"] += 1

                data["posts"].append({
                    "url": post_url,
                    "is_video": is_video,
                    "caption": caption,
                    "likes": likes,
                    "comments": comments,
                    "views": views,
                    "has_collaboration": has_collab,
                    "mentions": mentions
                })

            except Exception as e:
                print("Post hatası:", e)
                continue

        total_posts = max(1, data["post_count"] + data["reel_count"])
        data["avg_likes"] = data["total_likes"] // total_posts
        data["avg_comments"] = data["total_comments"] // total_posts
        data["avg_views"] = data["total_views"] // max(1, data["reel_count"])

        browser.close()

    return data