from Channel import Channel

file_name = 'madhya-pradesh-tourism-4.csv'
channel_name = 'Madhya Pradesh'

channel = Channel(file_name, channel_name)

freq = ''

channel.plot_over_time(freq=freq)

text_type = 'title'

channel.common_wordcloud(text_type = text_type)

text_type = 'description'

channel.common_wordcloud(text_type = text_type)