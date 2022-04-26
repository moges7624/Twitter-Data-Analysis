import json
import pandas as pd
from textblob import TextBlob
import zipfile

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [(x.get('user', {})).get('statuses_count', 0) for x in self.tweets_list]
        
        return statuses_count
    
    def find_full_text(self)->list:
        text = [x.get('retweeted_status',{}).get('text', '') for x in self.tweets_list]
        
        return text
    
    def find_sentiments(self, text)->list:
        
        polarity = []
        subjectivity = []
        
        for txt in text:
            if(txt):
                sentiment = TextBlob(str(txt)).sentiment
                polarity.append(sentiment.polarity)
                subjectivity.append(sentiment.subjectivity)
        
        return polarity, subjectivity

    def find_created_time(self)->list:
        
        created_at = [tweet['created_at'] for tweet in self.tweets_list]
        
        return created_at

    def find_source(self)->list:
        
        source = [tweet['source'] for tweet in self.tweets_list]

        return source

    def find_screen_name(self)->list:
        screen_name = [tweet['user']['screen_name'] for tweet in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [tweet['user']['followers_count'] for tweet in self.tweets_list]
        
        return followers_count
    
    def find_friends_count(self)->list:
        friends_count = [tweet['user']['friends_count'] for tweet in self.tweets_list] 
        
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = [x.get('possibly_sensitive', None) for x in self.tweets_list]

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = [tweet['user']['favourites_count'] for tweet in self.tweets_list] 

        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = [(x.get('retweeted_status', {})).get('retweet_count', None) for x in self.tweets_list]

        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [tweet['entities']['hashtags'] for tweet in self.tweets_list] 

        return hashtags

    def find_mentions(self)->list:
        mentions = []
        for i in range(len(self.tweets_list)):
            values = []
            for lists in self.tweets_list[i]['entities']['user_mentions']:
                values.append(lists['screen_name'])
                mentions.append(values)

        return mentions

    def find_location(self)->list:
        try:
            location = [x.get('user', {}).get('location', None) for x in self.tweets_list]
        except TypeError:
            location = ''
        
        return location
        
    def find_lang(self) -> list:
        lang = [self.tweets_list[i]['lang'] for i in range(len(self.tweets_list))]

        return lang
        
    def get_tweet_df(self, save=True)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        favorite_count = self.find_favourite_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        lang = self.find_lang()
        data = zip(created_at, source, text,polarity,subjectivity, lang, favorite_count, retweet_count, 
            screen_name, follower_count,friends_count,sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    json_data = []
    data = None  
    with zipfile.ZipFile("./data/Economic_Twitter_Data.zip", "r") as z:
       for filename in z.namelist():  
          with z.open(filename) as f:
            if f.name == 'Economic_Twitter_Data.json':
                # print(f)
                # data = f.read()  
                # d = json.loads(data) 
                for ele in f:
                    json_data.append(json.loads(ele))

    tweet_list = json_data
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    