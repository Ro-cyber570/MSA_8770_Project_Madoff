# financial_tool.py

import pandas as pd
from langchain_core.tools import tool

# Load the financial news data once
try:
    NEWS_DF = pd.read_csv("financial_news.csv")
    NEWS_DF['ticker'] = NEWS_DF['ticker'].str.upper()
    NEWS_DF.fillna('', inplace=True)
except FileNotFoundError:
    print("Error: financial_news.csv not found. Please ensure the file is in the same directory.")
    NEWS_DF = pd.DataFrame({'date': [], 'ticker': [], 'headline': [], 'link': []})


@tool
def get_financial_news(ticker_or_keyword: str) -> str:
    """
    Retrieves the 10 most recent financial news headlines for a given stock ticker 
    (e.g., 'MSFT', 'NVDA') or a general market keyword (e.g., 'AI', 'earnings').
    
    The agent MUST use this tool to gather information before formulating an investment strategy.
    """

    ticker = ticker_or_keyword.strip().upper()
    
    if ticker in NEWS_DF['ticker'].unique():

        recent_news = NEWS_DF[NEWS_DF['ticker'] == ticker].sort_values(
            by='date', ascending=False
        ).head(10)
        
        if not recent_news.empty:
            result_list = [
                f"[{row['date'].split(' ')[0]}] {row['headline']}"
                for index, row in recent_news.iterrows()
            ]
            return f"Recent headlines for {ticker}:\n" + "\n".join(result_list)
        else:
            return f"No recent news found specifically for the ticker {ticker}."
    

    else:

        keyword_filter = NEWS_DF['headline'].str.contains(
            ticker_or_keyword, case=False
        )
        
        keyword_news = NEWS_DF[keyword_filter].sort_values(
            by='date', ascending=False
        ).head(10)
        
        if not keyword_news.empty:
            result_list = [
                f"[{row['date'].split(' ')[0]}] {row['ticker']}: {row['headline']}"
                for index, row in keyword_news.iterrows()
            ]
            return f"Recent headlines containing '{ticker_or_keyword}' (up to 10):\n" + "\n".join(result_list)
        else:
            return f"No news found for the keyword '{ticker_or_keyword}'."

TOOLS = [get_financial_news]

if __name__ == "__main__":

    print(get_financial_news("MSFT"))
    print("\n" + "="*50 + "\n")

    print(get_financial_news("AI boom"))