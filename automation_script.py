import sqlite3
import requests
from datetime import datetime

# API Key and Endpoint
API_KEY = "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"  # Replace with your Perplexity API key
API_URL = "https://api.perplexity.ai/chat/completions"  # Confirmed endpoint

def fetch_ai_news():
    # JSON payload for the POST request
    payload = {
        "model": "llama-3.1-sonar-huge-128k-online",  # Example model
        "messages": [
            {
                "role": "system",
                "content": "Provide concise summaries of the latest AI news focusing on ethics and regulation."
            },
            {
                "role": "user",
                "content": "Give me 5 recent news updates on AI ethics and regulation."
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer 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",
        "accept": "application/json",
        "content-type": "application/json"
    }

    # Debugging information
    print(f"Making POST request to: https://api.perplexity.ai/chat/completions")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")

    try:
        # Make the POST request
        response = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=payload)

        # Debugging the response
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            data = response.json()

            # Connect to SQLite database
            conn = sqlite3.connect("ai_daily_bot.db")
            cursor = conn.cursor()

            # Process the response and store results
            for choice in data.get("choices", []):
                message_content = choice.get("message", {}).get("content", "")
                if message_content:
                    # For demonstration, we'll treat each paragraph as a news entry
                    for summary in message_content.split("\n\n"):
                        cursor.execute("""
                        INSERT INTO news (title, url, summary, date) 
                        VALUES (?, ?, ?, ?)
                        """, (summary[:50], None, summary, datetime.now().strftime("%Y-%m-%d")))

            conn.commit()
            conn.close()
            print("News updated successfully!")
        else:
            print(f"Error fetching news: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_ai_news()