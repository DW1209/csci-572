#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <dirent.h>
#include <filesystem>
#include <unordered_map>

std::unordered_map<std::string, std::string> readfile(const std::filesystem::path &dirname) {
    std::vector<std::filesystem::path> pathnames;
    DIR *dir = opendir(dirname.string().c_str());

    if (dir == NULL) {
        std::cerr << "Failed to open " << dirname << " directory..." << std::endl;
        return std::unordered_map<std::string, std::string>();
    }

    struct dirent *d;
    while ((d = readdir(dir))) {
        std::string filename = d->d_name;
        if (filename != "." && filename != "..") {
            std::filesystem::path pathname = dirname / filename;
            pathnames.push_back(pathname);
        }
    }
    closedir(dir);

    std::unordered_map<std::string, std::string> contents;
    for (const std::filesystem::path &pathname: pathnames) {
        std::ifstream file(pathname);
        if (!file.is_open()) {
            std::cerr << "Failed to open " << pathname << " file..." << std::endl;
            continue;
        }

        std::string str;
        while (std::getline(file, str)) {
            size_t idx = str.find('\t');
            if (idx != std::string::npos) {
                std::string id = str.substr(0, idx);
                std::string content = str.substr(idx + 1);
                contents[id] = content;
            }
        }
    }

    return contents;
}

void writefile(const std::map<std::string, std::map<std::string, int>> &res) {
    std::filesystem::path output = "outputs";
    if (!std::filesystem::exists(output)) {
        if (!std::filesystem::create_directory(output)) {
            std::cerr << "Failed to create " << output << " directory..." << std::endl;
            return;
        }
    }

    std::filesystem::path filename = output / "selected_bigram_index.txt";
    std::ofstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Failed to open " << filename << " file..." << std::endl;
        return;
    }

    for (const auto &[word, m]: res) {
        file << word << "\t";
        for (const auto &[id, cnt]: m) {
            file << id << ":" << cnt << " ";
        }
        file << std::endl;
    }
    file.close();
}

std::string cleantext(const std::string &text) {
    std::string str;
    for (char c: text) {
        if (std::isalpha(c) || std::isspace(c)) {
            str += std::tolower(c);
        } else {
            str += ' ';
        }
    }

    return str;
}

std::vector<std::string> tokenize(const std::string &text) {
    std::string str;
    std::vector<std::string> tokens;
    std::istringstream stream(text);

    while (stream >> str) {
        tokens.push_back(str);
    }

    return tokens;
}

std::map<std::string, std::map<std::string, int>> createidx(const std::unordered_map<std::string, std::string> &contents) {
    std::map<std::string, std::map<std::string, int>> res;
    std::vector<std::string> bigrams = {
        "computer science", "information retrieval", "power politics",
        "los angeles", "bruce willis"
    };

    for (const auto &[id, content]: contents) {
        std::string cleaned = cleantext(content);
        std::vector<std::string> words = tokenize(cleaned);
        for (size_t i = 0; i < words.size() - 1; i++) {
            std::string word = words[i] + " " + words[i + 1];
            if (std::find(bigrams.begin(), bigrams.end(), word) != bigrams.end()) {
                res[word][id]++;
            }
        }
    }

    return res;
}

int main(void) {
    std::filesystem::path input = "inputs/devdata";
    std::unordered_map<std::string, std::string> contents = readfile(input);
    std::map<std::string, std::map<std::string, int>> res = createidx(contents);
    writefile(res);
    return 0;
}
