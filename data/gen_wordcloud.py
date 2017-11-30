from os import path, getcwd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

## shameless ripoff of http://amueller.github.io/word_cloud/auto_examples/masked.html

from wordcloud.wordcloud import WordCloud
from wordcloud import STOPWORDS

d = path.dirname(getcwd()) + '/data'

# Read the whole text.
text = open(path.join(d, 'locations_redundant.txt')).read()

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
masked_back = np.array(Image.open(path.join(d, "india-map.png")))

stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=masked_back,
               stopwords=stopwords)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "tweets.png"))

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(masked_back, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()