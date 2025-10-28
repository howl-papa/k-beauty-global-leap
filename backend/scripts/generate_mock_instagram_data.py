"""
Generate Mock Instagram Data for Testing

Creates realistic mock data for Instagram posts, hashtags, and influencers
across different markets (Germany, France, Japan).
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict

# Mock data constants
MARKETS = ["germany", "france", "japan"]

K_BEAUTY_HASHTAGS = {
    "germany": [
        "kbeauty", "koreanbeauty", "kbeautydeutschland", "koreanischekosmetik",
        "glassskin", "10stepskincare", "koreanskincare", "kpop", "kbeautyhaul",
        "skincareroutine", "hautpflege", "beautyblogger_de", "skincaregermany"
    ],
    "france": [
        "kbeauty", "beautecoréenne", "kbeautyfrance", "soinscoréens",
        "peauparfaite", "routinesoin", "beautéblogueuse", "kbeautyhaul",
        "koreanskincare", "glassskin", "skincarefrance", "beauténaturelle"
    ],
    "japan": [
        "kbeauty", "韓国コスメ", "韓国美容", "オルチャン", "美肌",
        "スキンケア", "韓国スキンケア", "韓流", "コスメ好きさんと繋がりたい",
        "美容好きな人と繋がりたい", "韓国コスメ好き", "kビューティー"
    ]
}

INFLUENCER_USERNAMES = {
    "germany": [
        "beautyblogger_de", "skincare_sarah_de", "german_kbeauty_lover",
        "berlin_beauty_guru", "deutschland_glow", "hamburg_skincare",
        "munich_beauty_tips", "german_glassskin", "kbeauty_deutschland",
        "deutsche_hautpflege", "skincare_enthusiast_de", "beauty_anna_de"
    ],
    "france": [
        "beauteblogueuse_fr", "paris_skincare", "french_kbeauty",
        "beaute_marie", "glassskin_france", "lyon_beauty_tips",
        "french_skincare_addict", "paris_beauty_guru", "beaute_coréenne_fr",
        "french_glow", "soins_naturels_fr", "beaute_sophie"
    ],
    "japan": [
        "japanese_beauty_lover", "tokyo_skincare", "osaka_beauty",
        "japanese_kbeauty", "nihon_beauty", "kyoto_glassskin",
        "japan_skincare_tips", "tokyo_beauty_guru", "japanese_glow",
        "nihon_kbeauty", "osaka_skincare", "japanese_beauty_addict"
    ]
}

CAPTIONS_TEMPLATES = {
    "germany": [
        "Meine neue K-Beauty Routine! 🇰🇷✨ Diese Produkte haben mein Leben verändert. #kbeauty #skincare",
        "Glass Skin ist endlich möglich! 😍 Meine Top 5 koreanische Hautpflegeprodukte. #glassskin #koreanskincare",
        "10-Schritte-Routine Tag {day}! Seht ihr schon einen Unterschied? 🌟 #10stepskincare #kbeautyroutine",
        "Haul Alert! 🛍️ Neue K-Beauty Produkte sind angekommen. Was soll ich zuerst testen? #kbeautyhaul",
        "Morgenroutine mit meinen Lieblings-K-Beauty-Produkten ☀️ #morningroutine #kbeauty"
    ],
    "france": [
        "Ma nouvelle routine beauté coréenne! 🇰🇷✨ Ces produits ont changé ma vie. #beautecoréenne #skincare",
        "Glass Skin enfin possible! 😍 Mes 5 produits coréens préférés. #glassskin #soinscoréens",
        "Routine en 10 étapes Jour {day}! Vous voyez une différence? 🌟 #routinesoin #kbeauty",
        "Haul du jour! 🛍️ Nouveaux produits K-Beauty sont arrivés. Lequel essayer en premier? #kbeautyhaul",
        "Routine matinale avec mes produits K-Beauty favoris ☀️ #routinematinale #beautecoréenne"
    ],
    "japan": [
        "新しい韓国コスメルーティン! 🇰🇷✨ 人生が変わりました。 #韓国コスメ #スキンケア",
        "ガラス肌ついに実現! 😍 私のトップ5韓国スキンケア製品。 #美肌 #韓国スキンケア",
        "10ステップルーティン{day}日目! 違いがわかりますか? 🌟 #スキンケアルーティン #韓国コスメ",
        "購入品紹介! 🛍️ 新しい韓国コスメが届きました。どれから試そう? #韓国コスメ購入品",
        "朝のルーティン お気に入りの韓国コスメと一緒に ☀️ #朝のルーティン #韓国コスメ"
    ]
}

PRODUCT_NAMES = [
    "Cleanser", "Toner", "Essence", "Serum", "Sheet Mask", "Cream", 
    "Sun Cream", "Sleeping Mask", "Eye Cream", "Ampoule"
]

BRAND_NAMES = [
    "COSRX", "Innisfree", "Laneige", "Sulwhasoo", "Etude House",
    "The Face Shop", "Tony Moly", "Missha", "Dr. Jart+", "Klairs"
]


def generate_instagram_posts(market: str, count: int = 50) -> List[Dict]:
    """Generate mock Instagram posts for a specific market"""
    posts = []
    hashtags = K_BEAUTY_HASHTAGS[market]
    
    for i in range(count):
        # Random timestamp within last 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
        
        # Random username from market-specific list
        username = random.choice(INFLUENCER_USERNAMES[market])
        
        # Random caption
        caption_template = random.choice(CAPTIONS_TEMPLATES[market])
        caption = caption_template.format(day=random.randint(1, 30))
        
        # Random hashtags (5-10 per post)
        post_hashtags = random.sample(hashtags, min(random.randint(5, 10), len(hashtags)))
        
        # Random engagement metrics
        followers = random.randint(10000, 100000)
        likes = random.randint(int(followers * 0.02), int(followers * 0.08))
        comments = random.randint(int(likes * 0.01), int(likes * 0.05))
        
        # Random products/brands mentioned
        num_products = random.randint(1, 3)
        detected_products = random.sample(PRODUCT_NAMES, num_products)
        detected_brands = random.sample(BRAND_NAMES, random.randint(1, 2))
        
        post = {
            "external_id": f"instagram_{market}_{i+1}_{random.randint(10000, 99999)}",
            "caption": caption,
            "media_type": random.choice(["IMAGE", "VIDEO", "CAROUSEL_ALBUM"]),
            "media_url": f"https://example.com/media/{market}_{i+1}.jpg",
            "permalink": f"https://instagram.com/p/{market}_{i+1}",
            "username": username,
            "user_id": f"user_{username}_{random.randint(1000, 9999)}",
            "timestamp": timestamp.isoformat(),
            "location": None,
            "like_count": likes,
            "comment_count": comments,
            "engagement_rate": round((likes + comments) / followers * 100, 2),
            "hashtags": post_hashtags,
            "mentions": [],
            "market": market,
            "category": random.choice(["skincare", "makeup", "haircare"]),
            "sentiment_score": round(random.uniform(0.5, 1.0), 2),
            "sentiment_label": "positive",
            "detected_products": detected_products,
            "detected_brands": detected_brands,
            "is_sponsored": random.random() < 0.1,  # 10% are sponsored
            "is_verified_account": random.random() < 0.2,  # 20% are verified
        }
        
        posts.append(post)
    
    return posts


def generate_instagram_hashtags(market: str) -> List[Dict]:
    """Generate mock hashtag trend data for a specific market"""
    hashtags_data = []
    hashtags = K_BEAUTY_HASHTAGS[market]
    
    for idx, hashtag_name in enumerate(hashtags):
        # Random metrics
        post_count = random.randint(5000, 500000)
        avg_likes = random.uniform(200, 5000)
        avg_comments = random.uniform(10, 200)
        avg_engagement = random.uniform(2.0, 8.0)
        
        # Growth rate (-10% to +50%)
        growth_rate = round(random.uniform(-10, 50), 2)
        
        # Velocity (posts per hour)
        velocity = round(random.uniform(1, 100), 2)
        
        # Trend score calculation
        trend_score = round((
            min(abs(growth_rate), 100) * 0.4 +
            min(velocity / 10, 100) * 0.3 +
            min(avg_engagement, 100) * 0.2 +
            min(post_count / 1000, 100) * 0.1
        ), 2)
        
        hashtag = {
            "external_id": f"hashtag_{market}_{hashtag_name}_{random.randint(10000, 99999)}",
            "name": hashtag_name,
            "display_name": f"#{hashtag_name}",
            "market": market,
            "category": "beauty",
            "post_count": post_count,
            "avg_likes": round(avg_likes, 2),
            "avg_comments": round(avg_comments, 2),
            "avg_engagement": round(avg_engagement, 2),
            "growth_rate": growth_rate,
            "velocity": velocity,
            "is_trending": trend_score >= 60.0,
            "trend_score": trend_score,
            "competition_level": "high" if post_count > 100000 else "medium" if post_count > 50000 else "low",
            "difficulty_score": round(min(post_count / 5000, 100), 2),
            "tracked_at": datetime.utcnow().isoformat(),
            "data_source": "mock"
        }
        
        hashtags_data.append(hashtag)
    
    return hashtags_data


def generate_instagram_influencers(market: str, count: int = 20) -> List[Dict]:
    """Generate mock influencer profiles for a specific market"""
    influencers = []
    usernames = INFLUENCER_USERNAMES[market]
    
    for username in usernames[:count]:
        # Random follower count (micro to mid-tier influencers)
        followers = random.randint(10000, 500000)
        following = random.randint(500, 2000)
        media_count = random.randint(200, 2000)
        
        # Engagement metrics
        avg_likes = random.uniform(followers * 0.02, followers * 0.08)
        avg_comments = random.uniform(avg_likes * 0.01, avg_likes * 0.05)
        engagement_rate = round((avg_likes + avg_comments) / followers * 100, 2)
        
        # Quality scores
        authenticity_score = round(random.uniform(70, 95), 1)
        brand_affinity_score = round(random.uniform(60, 90), 1)
        content_quality_score = round(random.uniform(65, 95), 1)
        
        # Cost estimation
        base_cost_per_1k = 15
        follower_thousands = followers / 1000
        engagement_multiplier = 1.5 if engagement_rate > 5.0 else 1.0 if engagement_rate > 3.0 else 0.7
        post_cost = round(follower_thousands * base_cost_per_1k * engagement_multiplier, 2)
        
        influencer = {
            "external_id": f"influencer_{market}_{username}_{random.randint(10000, 99999)}",
            "username": username,
            "full_name": username.replace("_", " ").title(),
            "biography": f"K-Beauty enthusiast 🇰🇷 | Skincare addict | {market.title()}",
            "profile_picture_url": f"https://example.com/profile/{username}.jpg",
            "website": f"https://{username}.com" if random.random() < 0.3 else None,
            "is_verified": followers > 100000,
            "is_business_account": random.random() < 0.6,
            "is_private": False,
            "followers_count": followers,
            "following_count": following,
            "media_count": media_count,
            "avg_likes": round(avg_likes, 2),
            "avg_comments": round(avg_comments, 2),
            "engagement_rate": engagement_rate,
            "posts_per_week": round(random.uniform(2, 7), 1),
            "best_posting_times": ["18:00", "20:00", "21:00"],
            "content_types": {"IMAGE": 0.6, "VIDEO": 0.3, "CAROUSEL": 0.1},
            "category": "beauty",
            "sub_categories": ["kbeauty", "skincare", random.choice(["antiaging", "acne", "hydration"])],
            "market": market,
            "languages": [market[:2], "en"],
            "audience_country_top": market.title(),
            "audience_gender_split": {"male": round(random.uniform(0.1, 0.4), 2), "female": round(random.uniform(0.6, 0.9), 2)},
            "audience_age_range": random.choice(["18-24", "25-34", "35-44"]),
            "authenticity_score": authenticity_score,
            "brand_affinity_score": brand_affinity_score,
            "content_quality_score": content_quality_score,
            "collaboration_score": round((authenticity_score + brand_affinity_score + content_quality_score) / 3, 1),
            "estimated_post_cost": post_cost,
            "estimated_story_cost": round(post_cost * 0.5, 2),
            "partnership_tier": "micro" if followers < 100000 else "mid",
            "has_branded_content": random.random() < 0.5,
            "status": "discovered",
            "last_scraped_at": datetime.utcnow().isoformat(),
            "data_source": "mock"
        }
        
        influencers.append(influencer)
    
    return influencers


def main():
    """Generate all mock data and save to JSON files"""
    print("🎬 Generating Mock Instagram Data...")
    print("=" * 60)
    
    all_data = {
        "posts": [],
        "hashtags": [],
        "influencers": []
    }
    
    for market in MARKETS:
        print(f"\n📍 Generating data for {market.upper()}...")
        
        # Generate posts
        posts = generate_instagram_posts(market, count=50)
        all_data["posts"].extend(posts)
        print(f"  ✅ Generated {len(posts)} posts")
        
        # Generate hashtags
        hashtags = generate_instagram_hashtags(market)
        all_data["hashtags"].extend(hashtags)
        print(f"  ✅ Generated {len(hashtags)} hashtags")
        
        # Generate influencers
        influencers = generate_instagram_influencers(market, count=12)
        all_data["influencers"].extend(influencers)
        print(f"  ✅ Generated {len(influencers)} influencers")
    
    # Save to JSON file
    output_file = "backend/scripts/mock_instagram_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"✨ Mock data generated successfully!")
    print(f"📁 Saved to: {output_file}")
    print(f"\n📊 Summary:")
    print(f"  • Total Posts: {len(all_data['posts'])}")
    print(f"  • Total Hashtags: {len(all_data['hashtags'])}")
    print(f"  • Total Influencers: {len(all_data['influencers'])}")
    print(f"  • Markets: {', '.join(MARKETS)}")
    print("\n🚀 Ready to use for testing!")


if __name__ == "__main__":
    main()
