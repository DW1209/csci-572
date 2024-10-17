# Inverted-index Creation

## Description
- Construct a program to create an inverted index from multiple text files.
- Replace all the occurrences of special (punctuation) characters and numerals with the space character, and convert all the words to lowercase.

## Usage
### Compile
Run the command to compile the **unigram.cpp** and **bigram.cpp** program.
```bash
$ make
```
### Unigram Index
Run the command, and it will store the result in the **outputs directory** called **unigram_index.txt**.
```bash
$ ./unigram
```
### Bigram Index
Run the command, and it will store the result in the **outputs directory** called **selected_bigram_index.txt**.
```bash
$ ./bigram
```

## Explanation
- **unigram_index.txt** in the **outputs directory** contains words from files in the **fulldata directory**.
- **selected_bigram_index.txt** in the **outputs directory** contains the inverted index for just these five bigrams--_computer science_, _information retrieval_, _power politics_, _los angeles_, _bruce willis_--using files in the **devdata directory**.
