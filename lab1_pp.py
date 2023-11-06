import os
import re
import requests

header = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
'referer':'https://www.ya.ru/'
}
url = "https://www.livelib.ru/reviews/"
a = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=False)
a = a.content.decode('utf-8')

with open('t.txt', 'w', encoding="utf-8") as output:
    output.write(str(a))


with open("t.txt", "r", encoding="utf-8") as f:
    e = f.read()


lines = re.findall(r'<div class=\"lenta-card__rating\">\W{42}<span>\S{3}</span>\W{23}</div>', e)
reviews = re.findall(r'<div id=\"lenta-card__text-review-escaped\">([^а-я^А-Я]+)([а-яёА-ЯЁ0-9 ,.%\":?!-«»‹›–—“”]+)', e)
names = re.findall(r'<a class=\"lenta-card__book-title\" href=[\S]+>[a-zA-Zа-яёА-яЁ0-9 ,.?!\W\s]+\n', e)

result = {}
result_names = {}
count_names = 0
count_reviews = 0

for line in lines:
    temp = re.sub('<div class="lenta-card__rating">','', line)
    temp = re.sub('\W{42}<span>','', temp)
    temp = re.sub('</span>', '', temp)
    temp = re.sub('\W{23}</div>', '', temp)

    # print(temp)

for r in reviews:
    temp = re.sub('<div id=\"lenta-card__text-review-escaped\">', '', str(r))
    temp = re.sub('<p>', '', temp)
    temp = re.sub('<br>', '', temp)
    temp = re.sub('<br/>', '', temp)
    temp = re.sub('<blockquote>', '', temp)
    temp = re.sub('\'', '', temp)
    temp = re.sub(',', '', temp)


    result[r] = temp
    count_reviews += 1
    #print(f"\n {temp}")

print(f"{count_reviews}\n")

for n in names:
    temp = re.sub('<a class=\"lenta-card__book-title\" href=', '', n)
    temp = re.sub('[\S]+>', '', temp)

    result_names[n] = temp
    count_names += 1
    #print(temp)

print(count_names)

with open('data.txt', 'w', encoding="utf-8") as output:
    for key in result_names.keys():
        values_of_names = result_names[key]
        output.write(values_of_names + '\n' + '\n')
    for key in result.keys():
        values_of_reviews = result[key]
        output.write(values_of_reviews + '\n' + '\n')


# with open('names.txt', 'w', encoding="utf-8") as output:
#     for key in result_names.keys():
#         values_of_dict = result_names[key]
#         output.write(values_of_dict + '\n' + '\n')