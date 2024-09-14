import os
import csv
import json


class FileEditor:
    @staticmethod
    def read(filename):
        with open(filename, "r") as f:
            content = json.load(f)
        return content
    
    @staticmethod
    def write(dir, filename, fieldnames, content):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir, filename), 'w', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(content)


class CompareTool:
    @staticmethod
    def compare(fieldnames):
        cnt, sum, record = 0, 0, dict()
        bing_urls = list(CompareTool.transform(bing[query]))
        google_urls = list(CompareTool.transform(google[query]))
        for bidx, burl in enumerate(bing_urls):
            try:
                gidx = google_urls.index(burl)
                sum += (bidx - gidx) * (bidx - gidx)
                cnt += 1
            except ValueError:
                continue
        try:
            rho = round(1.0 - ((6.0 * sum) / (cnt * (cnt * cnt - 1.0))), 2)
        except ZeroDivisionError:
            rho = 1.0 if cnt == 1 and sum == 0 else 0.0
        record[fieldnames[0]] = f"Query {idx + 1}"
        record[fieldnames[1]] = cnt
        record[fieldnames[2]] = cnt * 10.0
        record[fieldnames[3]] = rho
        return record
    
    @staticmethod
    def calculate(result, fieldnames):
        nor, pco, rho = 0, 0, 0
        for data in result:
            nor += data[fieldnames[1]]
            pco += data[fieldnames[2]]
            rho += data[fieldnames[3]]
        record = dict()
        record[fieldnames[0]] = "Averages"
        record[fieldnames[1]] = nor / 100.0
        record[fieldnames[2]] = pco / 100.0
        record[fieldnames[3]] = round(rho / 100.0, 2)
        result.append(record)

    @staticmethod
    def transform(urls):
        for idx, url in enumerate(urls):
            if url[0:5] != "https":
                url = url[0:4] + "s" + url[4:]
            if url[-1] == "/":
                url = url[:-1]
            urls[idx] = url
        return urls


if __name__ == "__main__":
    result = list()
    bing = FileEditor.read(os.path.join("outputs", "hw1.json"))
    google = FileEditor.read(os.path.join("inputs", "Google_Result1.json"))
    fieldnames = [
        "Queries", "Number of Overlapping Results", 
        "Percent Overlap", "Spearman Coefficient"
    ]
    for idx, query in enumerate(bing):
        record = CompareTool.compare(fieldnames)
        result.append(record)
    CompareTool.calculate(result=result, fieldnames=fieldnames)
    FileEditor.write(dir="outputs", filename="hw1.csv", fieldnames=fieldnames, content=result)
