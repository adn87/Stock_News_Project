import requests
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "[put your stock API here]"
NEWS_API_KEY = "[put your news api here]"

MY_EMAIL = "[put your email here]"
MY_PASSWORD = "[put your password here]"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}


# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]
# print(yesterday_close)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_close = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_close)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
difference = float(yesterday_close) - float(day_before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "⬆"
else:
    up_down = "↓"

# Work out the percentage difference in price between closing price yesterday and closing price the day before
# yesterday.
percentage_difference = round((difference / float(yesterday_close)) * 100)
# print(percentage_difference)

# If percentage is greater than 5 then print("Get News").
if abs(percentage_difference) < 5:
    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    # Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]


    # Create a new list of the first 3 article headline and description using list comprehension.
    formatted_articles = [(f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in three_articles]

    # Send each article as a separate message via email.

    for article in formatted_articles:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(msg=f"Subject: {article.encode('ascii','ignore').decode('ascii')}",
                                from_addr=MY_EMAIL,
                                to_addrs="[recipient email here]")

# Optional Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
