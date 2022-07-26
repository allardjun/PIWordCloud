from wordcloud import WordCloud
import matplotlib.pyplot as plt

import pprint

from collections import Counter
from itertools import chain

from piwc_PIWordCloud import PI

def make_wordcloud(keyphrases, PIName):
    '''Takes keyphrases list and makes an image with those, processed with excludeWords, saves as the name of the PI'''

    with open("excludeWords.txt", "r") as f:
        excludeWords_list = f.read().splitlines() 

    #print(words_list)

    words_dict = Counter(keyphrases)

    for excludeWord in excludeWords_list:
        try:
            words_dict.pop(excludeWord)
        except:
            pass
            #print("exclude: " + excludeWord + " not found\n")

    with open("wordFrequencies.txt","w") as f:
        pprint.pprint(words_dict,stream=f)

    wordcloud = WordCloud(width = 1200, height = 1200,
                    background_color ='white',
                    collocations=False,
                    relative_scaling = 0.0,
                    max_font_size = 40,
                    min_font_size = 1).generate_from_frequencies(words_dict)

    # plot the WordCloud image					
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    plt.savefig(PIName + '.png')


if __name__ == "__main__":

    # To run stand-along, give it an extant list of phrases in a text file
    with open("sortedCloud2.txt", "r") as f: 
        words_list = f.read().splitlines()

    make_wordcloud(words_list, "new_faces_recent_takers")

