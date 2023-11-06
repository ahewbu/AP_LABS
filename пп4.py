import os
import argparse
import requests
import multiprocessing
from PIL import Image



def save_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = os.path.basename(url)
        image = Image.open(response.raw)
        image.save(filename)
        print(f"Image saved: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel Image Saver")
    parser.add_argument("urls", type=str, nargs="+", help="List of image URLs")
    args = parser.parse_args()
    urls = args.urls

processes = []
for url in urls:
    process = multiprocessing.Process(target=save_image, args=(url,))
    processes.append(process)
    process.start()

    for process in processes:
        process.join()

