from wordcloud import WordCloud
from math import log2
from json import load
from cv2 import imread

CONFIGS = load(open("configs.json")).get("cloud_configs", {})
OUTPUT_SIZE = CONFIGS.get("output_size", 1000)
IGNORE_WORDS = CONFIGS.get("ignore_words", [])
IGNORE_CNT = CONFIGS.get("ignore_cnt", 10000)
FILTER = eval(CONFIGS.get("filter", "lambda x:True"))

wc = None
if "mask" in CONFIGS:
   wc = WordCloud(mask=imread(CONFIGS["mask"]), scale=CONFIGS.get("scale", 1))
else:
   wc = WordCloud(width=1000, height=1000)

words = {i[0]: log2(i[1]*2)
         for i in load(open("data.json")) 
            if i[0] not in IGNORE_WORDS and i[1]<=IGNORE_CNT and FILTER(i)}

wc.generate_from_frequencies(words)
wc.background_color = CONFIGS.get("background_color", "white")
wc.to_file(CONFIGS.get("output_file", "wordcloud.png"))
