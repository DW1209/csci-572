# Web Search Engine Comparison

## Description
- Issue a set of queries and evaluate how closely the results of the two search engines, Google and Bing, are.
- Develop a script that could scrape the top 10 results from Bing.
- Compare the results between the JSON file generated from the script and the Google reference dataset.
- **100QuriesSet1.txt** in the **inputs directory** contains 100 queries, one query per line.
- **Google_Result1.json** in the **inputs directory** contains the Google results for each query in the dataset.

## Usage
### Scraping Results from Bing
Run the command, and it will store the results in the **outputs directory** called **hw1.json**.
```bash
$ python scrape.py
```
### Determining the Percent Overlap and Spearman Coefficient
Run the command, and it will store the results in the **outputs directory** called **hw1.csv**.
```bash
$ python compare.py
```
