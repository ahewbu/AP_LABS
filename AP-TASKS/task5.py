"""Задание 5. Используя пакет multiprocessing, распараллельте на процессы процедуру
загрузки изображений из списка URL. Написанное приложение должно быть консольным.
Аргументы командной строки - список URL-адресов"""
import os
import argparse
import requests
import multiprocessing
import cv2


def save_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        AP_LABS = os.path.basename(url)
    image = cv2.imread(response.raw)
    cv2.imwrite(AP_LABS, image)
    print(f"Image saved: {AP_LABS}")

  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel Image Saver")
    parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="List of image URLs")
    args = parser.parse_args()
    urls = args.urls


def main(processes):    
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=save_image, args=(url,))
        processes.append(process)
        process.start()
        
        for process in processes:
            process.join()

