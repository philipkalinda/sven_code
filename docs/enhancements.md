Objectives
---

1. Implement Twitter Sentiment analysis
    Steps:
    - Get the API working with keyword extraction
    - Determine how many tweets to focus on
    - Determine the recency / popularity of tweets (perhaps factor both - most popular in the last X, Y and Z days)
    - Determine the number of days to look back and how to aggregate scores

2. Youtube API integration
    Steps:
    -  test youtube credentials pulling in information regarding

3. Integrate Sentiment Analysis of new articles
    Steps:
    - Features include n_mentions, sentiment, recency etc

4. Google search term implementation
    Steps:
    - n_searches within multiple time periods and fitting a linear model to determine trend
    - experiment with closing price increase prediction
    
5. Implementation of new features
    Steps:
    - linear model to determine the general trend of the stock from t - 1year and t - 5years (our max data capture) 
    and maybe even 3 month movement (for analysis to inform). This will require additional analysis to decide on which
    gradients are acceptable to place with a signal of 1 
    - (quick win) MACD/RSI combination feature (if MACD==1 and (rsi_5_day == 1 or rsi_14_day == 1) : then 1 else 0) 
    - linear model applied to long Moving average and short moving average and assess the error between the model fit
    and the curves in order to determine their volatility.

6. Use Sentiment Analysis results to feed into predictive model for "closing price increase likelihood"  
    Steps:
    - Completion of sentiment analysis of twitter and perhaps news articles
    - experiment with modeling approach 
    - perhaps a model trained and stored for each stock then refreshed every month or however many based on the twitter 
    api allowances
    
7. Host on AWS servers  
    Steps:
    - Research monthly and annual costs
    - reproductive code
    - look at new way of hosting results for analysis (refresh the page with the top 30 on a web page)
    - look at hosting in flask application
    - secure login to view results
    - start with basic flask application then expand with template

8. expose results in Flask application
    Steps:
    - look at hosting in flask application
    - costs of hosting a flask application on aws
    - secure login to view results
    - start with basic flask application then expand with template

9. 
    Steps:
    - N/A
    
10. 
    Steps:
    - N/A
    
11. 
    Steps:
    - N/A
    
12. 
    Steps:
    - N/A 
---