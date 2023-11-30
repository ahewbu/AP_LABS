import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver


def make_dir(name: str) -> None:
    dirs = [f'{name}/{i}' for i in range(1, 6)]
    if not os.path.isdir(name):
        os.mkdir(name)
    for dir_name in dirs:
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)


def get_link_review(driver, links: str) -> str:
    driver.get("https://www.livelib.ru" + links.get("href"))
    sleep(2)
    soup_review = BeautifulSoup(driver.page_source, "lxml")
    try:
        soup_review = soup_review.find("div", {"id": "lenta-card__text-review-full"}).text.strip()
    except AttributeError:
        soup_review = None
    return soup_review


def write_review(number: int, title: str, links: str, rating: int, driver, name: str, rating_n: str) -> None:
    name_file = f'{name}/{rating}/{str(number).zfill(4)}.txt'
    with open(name_file, 'w', encoding="utf-8") as f:
        try:
            f.write(title.text.strip() + '\n' + rating_n + '\n' + get_link_review(driver, links)) #
        except TypeError:
            f.write(title.text.strip() + '\n' + rating_n + '\n' + " ")


def download_reviews(count: int, name: str) -> None:
    number_list = 2
    rating_review = [0] * 5
    driver = webdriver.Chrome() # Chrome можно поменять на Edge чтобы попытаться обойти защиту от DDos
    driver.maximize_window()
    while rating_review[4] < count or rating_review[3] < count or rating_review[2] < count or rating_review[1] < count or rating_review[0] < count:
        URL = f"https://www.livelib.ru/reviews/~{number_list}#reviews"
        driver.get(URL)
        sleep(1)
        number_list += 1
        soup = BeautifulSoup(driver.page_source, "lxml")

        rating = soup.find_all("span", {"class": "lenta-card__mymark"})
        title = soup.find_all("a", "lenta-card__book-title")
        links = soup.find_all("a", {"class": "footer-card__link"})
        for i in range(len(rating) - 1): 
            if float(rating[i].text) <= 5.0 and float(rating[i].text) >= 4.5 and rating_review[4] < count:
                rating_review[4] += 1
                write_review(rating_review[4], title[i], links[i], 5, driver, name, rating[i].text)
            elif float(rating[i].text) <= 4.4 and float(rating[i].text) >= 3.5 and rating_review[3] < count:
                rating_review[3] += 1
                write_review(rating_review[3], title[i], links[i], 4, driver, name, rating[i].text)
            elif float(rating[i].text) <= 3.4 and float(rating[i].text) >= 2.5 and rating_review[2] < count:
                rating_review[2] += 1
                write_review(rating_review[2], title[i], links[i], 3, driver, name, rating[i].text)
            elif float(rating[i].text) <= 2.4 and float(rating[i].text) >= 1.5 and rating_review[1] < count:
                rating_review[1] += 1
                write_review(rating_review[1], title[i], links[i], 2, driver, name, rating[i].text)
            elif float(rating[i].text) <= 1.4 and rating_review[0] < count:
                rating_review[0] += 1
                write_review(rating_review[0], title[i], links[i], 1, driver, name, rating[i].text)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    make_dir('data')
    download_reviews(1000, 'data')