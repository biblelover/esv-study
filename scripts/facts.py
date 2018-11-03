import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import tomd

fact_url = "https://www.esv.org/partials/study-index/esv-global-study-bible/"

headers = {
    "Cookie": "csrftoken=q1IQJ4lPzJKJGoByUVsSugfRWrueHifC5hFL6l4VDxDMSi6to76RMaauXdP7bqfh; sessionid=tmgp2odapdywae2k4tai7k0zfvg2z71c",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

def get_data(url, headers=headers):
    r = requests.get(url, headers=headers)
    fact_urls = re.findall(r'data-slug="(facts-.*?)">(.*?)</a>', r.text)

    data = []

    for fact in fact_urls:
        book = "-".join(fact[0].split("-")[1:-1])

        data.append(
            [
                urljoin(url, fact[0]),
                fact[1],
                book
            ]
        )

    books = {}

    for fact in data:
        if not fact[2] in books:
            books[fact[2]] = []

        books[fact[2]].append({
            "url": fact[0].replace("/study-index/", "/study-resource/"),
            "title": fact[1]
        })

    return books
 
def get_text(url, headers=headers):
    r = requests.get(url, headers=headers)
    text = tomd.convert(r.text)
    return text

if __name__=="__main__":
    # Comment the next line to run program
    quit()
    #=====================================

    result = get_data(fact_url)

    index = 1
    for book, data in result.items():
        path = "global-study-bible/facts/books"
        

        if not os.path.exists(path):
            os.makedirs(path, )

        file_path = "%s/%s. %s.md" % (path, index, book)

        if os.path.exists(file_path):
            print(">>> %s already written" % book)

        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# %s Facts\n" % book.title())

                for item in data:
                    text = get_text(item["url"])
                    text = re.sub("## Fact:.*?\n", 
                        ("## " + item["title"].split(" Fact ", 1)[-1]), text)

                    text = re.sub("(/(.*?)/)", r"https://www.esv.org\1", text)
                    f.write("%s\n" % text)
                    f.flush()

                    print("Extracting %s" % item["title"])

        print("writing %s complete" % book)
        index += 1