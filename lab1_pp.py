import os
import re
import requests

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.ya.ru/'
}
url = "https://www.livelib.ru/reviews/~2#reviews"
a = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True)
output = open('t.txt', 'w')
output.write(str(a.content))
output.close()

with open("t.txt", "r") as f:
    e = f.read()


lines = re.findall(r'<div class=\"lenta-card__rating\">.{45}<span>.{3}</span>.{24}</div>', e)
result = {}
for line in lines:
    temp = re.sub('<div class="lenta-card__rating">','', line)
    temp = re.sub('.{45}<span>','', temp)
    temp = re.sub('</span>', '', temp)
    temp = re.sub('.{24}</div>', '', temp)

    print(temp)

