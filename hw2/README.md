# Web Crawling

## Description
Construct a crawler, make it crawl one of the news websites below, and collect information.

| News Sites to Crawl | News Sites Name | Root URL                 |
|---------------------|-----------------|--------------------------|
| NY Times            | nytimes         | https://www.nytimes.com  |
| Wall Street Journal | wsj             | https://www.wsj.com      |
| Fox News            | foxnews         | https://www.foxnews.com  |
| USA Today           | usatoday        | https://www.usatoday.com |
| Los Angeles Times   | latimes         | https://www.latimes.com  |

## Usage
Run the command with a news site name argument, and it will store the results in the **outputs directory**.
```bash
$ python crawler.py -w <website> # e.g. python crawler.py -w usatoday
```

## Explanation
- **fetch_{website}.csv** is a two-column spreadsheet containing the URLs attempted to fetch and the HTTP/HTTPS status code received.
- **urls_{website}.csv** is a four-column spreadsheet containing the URLs successfully downloaded, the size of the downloaded file, the number of outlinks found, and the resulting content type.
- **visit_{website}.csv** is a two-column spreadsheet containing the encountered URL and an indicator of whether the URL is inside the website of not (OK and N_OK).
- **CrawlReport_{website}.txt** is a statistics report based on the crawler outputs.
