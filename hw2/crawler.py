import os
import csv
import http
import time
import queue
import random
import argparse
import requests
import threading

from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse


class Crawler:
    def __init__(self, website, num_threads=7, mxpage=20000, mxdepth=16):
        self.visited_urls = set()
        self.lock = threading.Lock()
        self.urls_queue = queue.Queue()
        self.num_threads = num_threads
        self.mxpage, self.mxdepth = mxpage, mxdepth
        self.website, self.baseurl = website, f"https://www.{website}.com"
        self.fetch_data, self.urls_data, self.visited_data = list(), list(), list()
        self.status_codes, self.content_types, self.filesizes = defaultdict(int), defaultdict(int), defaultdict(int)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)
    
    def is_same_domain(self, url):
        return urlparse(self.baseurl).netloc == urlparse(url).netloc

    def get_filesize_range(self, filesize):
        if filesize < 1024:
            return "< 1KB"
        elif filesize < 10 * 1024:
            return "1KB ~ <10KB"
        elif filesize < 100 * 1024:
            return "10KB ~ <100KB"
        elif filesize < 1024 * 1024:
            return "100KB ~ <1MB"
        else:
            return ">= 1MB"

    def worker(self):
        while True:
            url, depth = self.urls_queue.get()
            if url == None:
                break
            self.crawl(url, depth)
            self.urls_queue.task_done()
    
    def crawl(self, url, depth=0):
        with self.lock:
            if depth >= self.mxdepth or len(self.visited_urls) >= self.mxpage:
                return
            if url in self.visited_urls:
                return
            self.visited_urls.add(url)
        try:
            time.sleep(random.uniform(1, 2))
            response = requests.get(url, timeout=30)
            status_code = response.status_code
            if status_code == 429:
                with self.lock:
                    self.visited_urls.remove(url)
                return
            with self.lock:
                self.status_codes[status_code] += 1
                self.fetch_data.append([url, status_code])
            if status_code == 200:
                content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
                filesize = len(response.content)
                with self.lock:
                    self.content_types[content_type] += 1
                    self.filesizes[self.get_filesize_range(filesize)] += 1
                if content_type == "text/html":
                    soup = BeautifulSoup(response.text, "html.parser")
                    outlinks = set()
                    for link in soup.find_all("a", href=True):
                        newurl = urljoin(url, link["href"])
                        if self.is_valid_url(newurl):
                            outlinks.add(newurl)
                            with self.lock:
                                self.urls_data.append([newurl, "OK" if self.is_same_domain(newurl) else "N_OK"])
                    for img in soup.find_all("img", src=True):
                        newurl = urljoin(url, img["src"])
                        if self.is_valid_url(newurl):
                            outlinks.add(newurl)
                            with self.lock:
                                self.urls_data.append([newurl, "OK" if self.is_same_domain(newurl) else "N_OK"])
                    with self.lock:
                        self.visited_data.append([url, filesize, len(outlinks), content_type])
                    for link in outlinks:
                        if self.is_same_domain(link):
                            self.urls_queue.put((link, depth + 1))
        except Exception as e:
            print(f"Error Crawling {url}: {str(e)}")
            with self.lock:
                self.visited_urls.remove(url)

    def save(self, dir="outputs"):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir, f"fetch_{self.website}.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Status"])
            writer.writerows(self.fetch_data)
        with open(os.path.join(dir, f"visit_{self.website}.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Size (bytes), # of Outlinks, Content Type"])
            writer.writerows(self.visited_data)
        with open(os.path.join(dir, f"urls_{self.website}.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Indicator"])
            writer.writerows(self.urls_data)

    def report(self, dir="outputs"):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir, f"CrawlReport_{self.website}.txt"), "w") as f:
            f.write(f"Name: Wei-Cheng Wang\n")
            f.write(f"USC ID: 3351037624\n")
            f.write(f"News site crawled: {self.website}.com\n")
            f.write(f"Number of threads: {self.num_threads}\n")
            f.write(f"\n")
            f.write(f"Fetch statistics:\n")
            f.write(f"================\n")
            f.write(f"# fetches attempted: {len(self.fetch_data)}\n")
            f.write(f"# fetched succeeded: {self.status_codes[200]}\n")
            f.write(f"# fetches failed or aborted: {len(self.fetch_data) - self.status_codes[200]}\n")
            f.write(f"\n")
            f.write(f"Outgoing URLs:\n")
            f.write(f"================\n")
            f.write(f"Total URLs extracted: {len(self.urls_data)}\n")
            f.write(f"# unique URLs extracted: {len(set(url for url, _ in self.urls_data))}\n")
            f.write(f"# unique URLs within News Site: {len(set(url for url, status in self.urls_data if status == 'OK'))}\n")
            f.write(f"# unique URLs outside News Site: {len(set(url for url, status in self.urls_data if status == 'N_OK'))}\n")
            f.write(f"\n")
            f.write(f"Status Codes:\n")
            f.write(f"================\n")
            for status_code, cnt in sorted(self.status_codes.items()):
                status_name = http.client.responses.get(status_code, "Unknown")
                f.write(f"{status_code} {status_name}: {cnt}\n")
            f.write(f"\n")
            f.write(f"File Sizes:\n")
            f.write(f"================\n")
            f.write(f"< 1KB: {self.filesizes['< 1KB']}\n")
            f.write(f"1KB ~ <10KB: {self.filesizes['1KB ~ <10KB']}\n")
            f.write(f"10KB ~ <100KB: {self.filesizes['10KB ~ <100KB']}\n")
            f.write(f"100KB ~ <1MB: {self.filesizes['100KB ~ <1MB']}\n")
            f.write(f">= 1MB: {self.filesizes['>= 1MB']}\n")
            f.write(f"\n")
            f.write(f"Content Types:\n")
            f.write(f"================\n")
            for content_type, cnt in sorted(self.content_types.items()):
                f.write(f"{content_type}: {cnt}\n")
            f.write(f"\n")
            f.write(f"Change Reason:\n")
            f.write(f"================\n")
            f.write(f"I switch to USA Today instead of Wall Street Journal\n")
            f.write(f"because I am unable to retrieve content from the website\n")
            f.write(f"and keep receiving a 403 Forbidden error.")

    def start(self):
        threads = list()
        self.urls_queue.put((self.baseurl, 0))
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        self.urls_queue.join()
        for i in range(self.num_threads):
            self.urls_queue.put((None, None))
        for t in threads:
            t.join()
        self.save()
        self.report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple web crawler")
    parser.add_argument("-w", "--website", type=str, help="Website Name", required=True)
    args, _ = parser.parse_known_args()
    crawler = Crawler(args.website)
    crawler.start()
