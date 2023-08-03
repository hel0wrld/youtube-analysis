import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

class Channel:

    """
    Initialise a channel object to call its various functions

    1. plot_over_time()
    2. common_wordcloud()
    """

    def __init__(self, file_name: str, channel_name: str):

        self.file_name = file_name
        self.channel_name = channel_name
        self.df = pd.read_csv(self.file_name)
        print("Read file successfully!", flush=True)

    def plot_over_time(self, **kwargs):
        
        '''
        Plot the frequency of upload using a seaborn dark theme
        Parameters:
        frequency : string for resampling. e.g. 3W for 3 weeks
                        '3W' by default
        '''

        self.df['publishedAt'] = pd.to_datetime(self.df['publishedAt'])

        sns.set_style('dark')

        freq = ''
        if 'frequency' in list(kwargs.keys()):
            freq = kwargs['frequency']
        else:
            freq = '3W'

        print("Read frequency successfully!")
        df_resample = self.df.resample(freq, on='publishedAt').count()

        print("Setting up plot...")
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(df_resample.index, df_resample['title'])
        ax.set_title(f'[{self.channel_name}] Frequency of popular videos over time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Video count')
        ax.grid(True)

        print('Waiting for closing command...')
        plt.show()
        print('Exiting...')

    def common_wordcloud(self, **kwargs):

        """
        Create a wordcloud for title or description.
        Parameters:
        type : string for "title" or "description"
                "title" by default
        """

        nltk.download('stopwords')
        nltk.download('punkt')
        print("Downloaded NLTK requirements!")

        text_type = ''
        if 'text_type' in list(kwargs.keys()):
            text_type = kwargs['text_type']
        else:
            text_type = 'title'

        print(f"Combined the {text_type} for the database successfully!")
        all_title = self.df[text_type].str.cat(sep='__')

        all_title = all_title.lower()
        all_title = ''.join(c for c in all_title if c.isalnum() or c.isspace())

        words = word_tokenize(all_title)
        english_stopwords = set(stopwords.words('english'))

        common_words = ['check', 'use', 'amazon', 'main', 'store',
                        'camera', 'equipment', 'details', 'gorillapod',
                        'support', 'mic', 'pro', 'links', 'free', 'link',
                        'video', 'youtube', 'instagram', 'facebook',
                        'series', 'playlist', 'videos', 'channel',
                        'location', 'rs', 'google', 'episode', 'address',
                        'go', 'gb', 'hdd', 'memory', 'card', 'ssd', 'adaptor',
                        'battery', 'watch', 'accessories', 'charger', 'bag',
                        'also', 'drone', 'dslr', 'product', '128', 'cards', 'tb',
                        'storefront', 'leave', 'whole', 'vlog', 'tripod', 'x', 'get',
                        'download', 'subscribe', 'latest', 'updates', 'android', 'apps',
                        'follow', 'visit', 'like', 'twitter', 'us', 'view',
                        'website', 'music', 'social', 'media']
        
        english_stopwords.update(common_words)
        filtered_words = [word for word in words 
                          if word not in english_stopwords and 
                          not word.startswith('http')]
        # filtered_words = [word for word in words if word not in description_common_words]

        filtered_text = ' '.join(filtered_words)
        filtered_text_list = filtered_text.split(' ')

        print("Filtered out common words successfully!")
        freq_words = Counter(filtered_text_list).most_common()

        # print("Printing the most frequent terms...")
        # print(freq_words[:10])

        freq_dict = {}
        for key, val in freq_words:
            freq_dict[key] = val

        print("Creating a wordcloud...")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dict)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(label=f'[{self.channel_name}] Most common words in {text_type}')

        print('Waiting for closing command...')
        plt.show()
        print('Exiting...')

