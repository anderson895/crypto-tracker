from flask import Flask, jsonify
import requests, time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

meme_coins = [
    "dogecoin", "shiba-inu", "pepe", "floki", "bonk",
    "dogwifcoin", "baby-doge-coin", "book-of-meme", "catcoin", "mog-coin"
]

last_prices = {}
last_fetch_time = 0
cached_data = []

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def get_prices():
    global last_fetch_time, cached_data

    # Avoid calling API too often (wait 30 seconds between calls)
    if time.time() - last_fetch_time < 30:
        print("🕒 Using cached data (rate limit protection)")
        return cached_data

    ids = ",".join(meme_coins)
    params = {
        "vs_currency": "usd",
        "ids": ids,
        "order": "market_cap_desc",
        "per_page": len(meme_coins),
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(COINGECKO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Cache the result and update timestamp
        cached_data = data
        last_fetch_time = time.time()
        return data

    except requests.exceptions.HTTPError as e:
        print(f"❌ Error fetching prices: {e}")
        if response.status_code == 429:
            print("⚠️ Rate limited — using last cached data.")
            return cached_data
        return []

    except Exception as e:
        print(f"⚠️ Unknown error: {e}")
        return cached_data

@app.route("/api/prices")
def prices():
    global last_prices
    data = get_prices()
    results = []

    for coin_data in data:
        coin = coin_data["id"]
        price = coin_data.get("current_price", 0)
        change_24h = coin_data.get("price_change_percentage_24h", 0)
        image = coin_data.get("image", "")
        last_price = last_prices.get(coin)
        trend = "new"

        if last_price:
            if price > last_price:
                trend = "up"
            elif price < last_price:
                trend = "down"
            else:
                trend = "same"

        last_prices[coin] = price
        results.append({
            "name": coin,
            "price": price,
            "trend": trend,
            "change_24h": round(change_24h, 2),
            "icon": image
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
