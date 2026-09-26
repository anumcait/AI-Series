import os
from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def classify_sentiment(review: str) -> str:
    prompt = f"""
Classify the following customer review as exactly one of:
Positive, Neutral, or Negative.

Also provide a short explanation.

Review:
{review}

Return the result in this format:

Sentiment: <Positive|Neutral|Negative>
Explanation: <short explanation>
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":
    review = "The product arrived quickly and works perfectly."

    response = classify_sentiment(review)

    print(response)
