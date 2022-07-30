# Python program to generate WordCloud
# https://www.geeksforgeeks.org/generating-word-cloud-python/

# importing all necessary modules
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

with open("sortedCloud.txt", "r") as f:
	excludeWords_list = f.read().splitlines() 
excludeWords_set = set(excludeWords_list)

with open("sortedCloud2.txt", "r") as f:
	words_list = f.read().splitlines() 
words_string = ' '.join(words_list)

#print(words_string)

wordcloud = WordCloud(width = 800, height = 800,
				background_color ='white',
				stopwords = excludeWords_set,
                collocations=False,
                relative_scaling = 0.0,
                max_font_size = 40,
				min_font_size = 1).generate(words_string)

# plot the WordCloud image					
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()
