import os
import time
import json
import requests

from random import randint
from bs4 import BeautifulSoup


class SearchEngine:
    @staticmethod
    def search(query, headers, sleep=True):
        if sleep:
            time.sleep(randint(10, 100))
        str = '+'.join(query.split())
        url = "http://www.bing.com/search?q=" + str + "&count=30"
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        results = SearchEngine.scrape_search_result(soup)
        return results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("li", class_="b_algo")
        results = list()
        for result in raw_results:
            if result.find("a", href=True):
                link = result.find("a", href=True)["href"]
                results.append(link)
        return list(set(results))[:10]


class FileEditor:
    @staticmethod
    def read(filename):
        content = open(filename, "r").read()
        queries = content.split(" \n")
        queries.pop()
        return queries

    @staticmethod
    def write(dir, filename, content):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir, filename), "w") as f:
            json.dump(content, f, indent=2)


if __name__ == "__main__":
    queries = FileEditor.read(os.path.join("inputs", "100QueriesSet1.txt"))
    results = dict()
    headers = {
        'User-Agent': \
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/61.0.3163100 Safari/537.36'
    }
    for query in queries:
        urls = SearchEngine.search(query=query, headers=headers)
        results[query] = urls
    FileEditor.write(dir="outputs", filename="hw1.json", content=results)
