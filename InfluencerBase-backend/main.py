from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from scraper import scrape_instagram_profile

app = Flask(__name__)
CORS(app)  # Netlify'den gelen frontend erişimi için gerekli


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True) or {}
    username = data.get('username', 'bilinmeyen')

    try:
        profile_data = scrape_instagram_profile(username, max_posts=12)

        total_interactions = profile_data['total_likes'] + profile_data[
            'total_comments']
        follower_count = 10000

        engagement_rate = round(
            (total_interactions /
             (follower_count * len(profile_data['posts']))) * 100, 2)

        collaboration_brands = []
        for post in profile_data['posts']:
            if post['has_collaboration']:
                collaboration_brands.extend(post['mentions'])

        response = {
            "username": username,
            "follower_count": follower_count,
            "average_likes": profile_data["avg_likes"],
            "average_comments": profile_data["avg_comments"],
            "average_views": profile_data["avg_views"],
            "post_count": profile_data["post_count"],
            "reel_count": profile_data["reel_count"],
            "engagement_rate": engagement_rate,
            "last_collaborations": list(set(collaboration_brands)),
            "collaboration_count": profile_data["collaboration_count"]
        }

        return jsonify(response)

    except Exception as e:
        print("HATA:", e)
        return jsonify({"error": str(e)}), 500


# Uygulama çalıştığında Replit'e uygun şekilde port 3000'den başlat
app.run(host='0.0.0.0', port=3000)
