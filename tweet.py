import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class newtc(object): 

    def __init__(self): 

        #enter your own key and token
        key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
        secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accesstoken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accesstoken_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
  
        # try to authenticate 
        try: 
            
            self.auth = OAuthHandler(key, secret) 
            
            self.auth.set_access_token(accesstoken, accesstoken_secret) 
            
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean(self, tweet): 
        #Regex cleaning
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) 
                                    |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 

        # create TextBlob object
        analysis = TextBlob(self.clean(tweet)) 
        
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def tget(self, query, count = 10):
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched = self.api.search(q = query, count = count) 
            for tweet in fetched: 
                # empty dictionary
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            
            return tweets 
  
        except tweepy.TweepError as e: 
            
            print("Error : " + str(e)) 
  
def main(): 
    
    api = newtc() 
    
    tweets = api.tget(query = 'Donald Trump', count = 200) 
  
    
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
     
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
     
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    
    print("Neutral tweets percentage: {} % \ 
        ".format(100*len(tweets - ntweets - ptweets)/len(tweets))) 
  
    # printing first few positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 
  
    # printing first few negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
  
if __name__ == "__main__": 
    main()
