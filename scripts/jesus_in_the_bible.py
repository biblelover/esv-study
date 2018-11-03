# import requests
# from bs4 import BeautifulSoup
# import re
# import os
# from urllib.parse import urljoin
# import tomd

# book_info_url = "https://www.esv.org/partials/study-index/esv-global-study-bible/"

# headers = {
#     "Cookie": "csrftoken=q1IQJ4lPzJKJGoByUVsSugfRWrueHifC5hFL6l4VDxDMSi6to76RMaauXdP7bqfh; sessionid=tmgp2odapdywae2k4tai7k0zfvg2z71c",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
# }

# def get_data(url, headers=headers):
#     r = requests.get(url, headers=headers)
#     book_info_urls = re.findall(r'data-slug="(introduction-to-.*?)">(.*?)</a>', r.text)

#     data = []

#     for book_info in book_info_urls:
#         book = "-".join(book_info[0].split("-")[1:-1])

#         data.append(
#             [
#                 urljoin(url, book_info[0]),
#                 book_info[1],
#                 book[1]
#             ]
#         )

#     books = {}

#     for book_info in data:
#         if not book_info[1] in books:
#             books[book_info[1]] = []

#         books[book_info[1]].append({
#             "url": book_info[0].replace("/study-index/", "/study-resource/"),
#             "title": book_info[1]
#         })

#     return books
 
# def get_text(url, headers=headers):
#     # https://www.esv.org/partials/study-content/Deuteronomy%2014/esv-gospel-transformation-bible/
#     r = requests.get(url, headers=headers)

#     print(r.text)
#     quit()
#     text = tomd.convert(r.text)
#     return text

# if __name__=="__main__":
#     # Comment the next line to run program
#     #=====================================

#     result = get_data(book_info_url)

#     index = 1
#     for book, data in result.items():
#         path = "global-study-bible/introduction/books"

#         if not os.path.exists(path):
#             os.makedirs(path, )

#         file_path = "%s/%s.md" % (path, book.lower())

#         if os.path.exists(file_path):
#             print(">>> %s already written" % book)

#         # else:
#             with open(file_path, "w", encoding="utf-8") as f:
#                 for item in data:
#                     text = get_text(item["url"])
#                     text = re.sub("## book_info:.*?\n", 
#                         ("## " + item["title"].split(" book_info ", 1)[-1]), text)

#                     text = re.sub("(/(.*?)/)", r"https://www.esv.org\1", text)
#                     f.write("%s\n" % text)
#                     f.flush()

#                     print("Extracting %s" % item["title"])

#         print("writing %s complete" % book)
#         index += 1


# get_data(book_info_url)
