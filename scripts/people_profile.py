import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import tomd

people_url = "https://www.esv.org/partials/study-index/esv-global-study-bible/"

headers = {
    "Cookie": "csrftoken=q1IQJ4lPzJKJGoByUVsSugfRWrueHifC5hFL6l4VDxDMSi6to76RMaauXdP7bqfh; sessionid=tmgp2odapdywae2k4tai7k0zfvg2z71c",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

def get_data(url, headers=headers):
    r = requests.get(url, headers=headers)
    people_urls = re.findall(r'data-slug="(profiles-.*?)">(.*?)</a>', r.text)

    data = []

    for people in people_urls:
        profile = "-".join(people[0].split("-")[1:-1])

        data.append(
            [
                urljoin(url, people[0]),
                people[1],
                profile[1]
            ]
        )

    profiles = {}

    for people in data:
        if not people[1] in profiles:
            profiles[people[1]] = []

        profiles[people[1]].append({
            "url": people[0].replace("/study-index/", "/study-resource/"),
            "title": people[1]
        })

    return profiles
 
def get_text(url, headers=headers):
    r = requests.get(url, headers=headers)
    text = tomd.convert(r.text)
    return text

if __name__=="__main__":
    # Comment the next line to run program
    #=====================================

    result = get_data(people_url)

    index = 1
    for profile, data in result.items():
        path = "global-study-bible/people/profiles"
        

        if not os.path.exists(path):
            os.makedirs(path, )

        file_path = "%s/%s.md" % (path, profile.lower())

        if os.path.exists(file_path):
            print(">>> %s already written" % profile)

        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# %s Profile\n" % profile.title())

                for item in data:
                    text = get_text(item["url"])
                    text = re.sub("## people:.*?\n", 
                        ("## " + item["title"].split(" people ", 1)[-1]), text)

                    text = re.sub("(/(.*?)/)", r"https://www.esv.org\1", text)
                    f.write("%s\n" % text)
                    f.flush()

                    print("Extracting %s" % item["title"])

        print("writing %s complete" % profile)
        index += 1


get_data(people_url)
