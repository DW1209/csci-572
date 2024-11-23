# LLMs, Vectors, RAG

## Description
- Use [Weaviate](https://weaviate.io/), which is a vector DB - stores data as vectors after vectorizing, and computes a search query by vectorizing it and does similarity search with existing vectors.
- Use [lightning.ai](https://lightning.ai/) to run RAG on lightning's GPU - accelerated cloud VM platform.
- Use [HuggingFace](https://huggingface.co/) to run a RAG application and describe its components.

## Usage
### Weaviate
#### Download Docker Desktop
Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/) to your desktop.
#### Install Weaviate and a Vectorizer Module
Run this command to pull in two images: the **weaviate** and a text2vec transformer called **t2v-transformers**.
```bash
$ docker-compose up -d
```
#### Loading Data to Search
Run the command to submit the **data.json** in the **inputs directory** to create a schema called _"SimSearch"_. You can load your own data by modifying the contents of **data.json** in the **inputs directory**. Also, you have to modify **weave-loadData.py** to put in your keys (instead of _"MusicGenre"_, _"SongTitle"_, _"Artist"_) if you are using your own data.
```bash
$ python weave-loadData.py
```
#### Querying Vectorized Data
Run the command to query the vectorized data. You can modify the query keywords in the **weave-doQuery.sh** in line 9 if you are using your own data. Also, be sure to modify toe keys (instead of _"musicGenre"_, _"songTitle"_, _"artist"_) in this shell script.
```bash
$ ./weave-doQuery.sh
```
### lightning.ai
Go to [lightning.ai](https://lightning.ai/) and sign up for a free account. Then, create this [Studio](https://lightning.ai/lightning-ai/studios/document-search-and-retrieval-using/rag). Afterward, upload the **cooking.pdf** in the **inputs directory** or your own PDF and modify the `files` variable in the **run.ipynb** to point to the PDF. Modify the `query` and `queries` variables to each contain a question on which you would like to do RAG. **query1.txt** and **query2.txt** in the **inputs directory** are the examples. Eventually, run the code and you will see the two answers printed out!
### Hugging Face
Go to [RAG PDF Chatbot](https://huggingface.co/spaces/MuntasirHossain/RAG-PDF-Chatbot) in [HuggingFace](https://huggingface.co/spaces) and run the app according to the instruction. You can choose another RAG app [here](https://huggingface.co/spaces?sort=trending&search=RAG).

## Explanation
- **q1.png** in the **outputs directory** is the screenshot of the Weaviate result. 
- **q2_pdf.png** in the **outputs directory** is the screenshot of the file structure after uploading the PDF to the [Studio](https://lightning.ai/lightning-ai/studios/document-search-and-retrieval-using/rag).
- **q2_query1.png**, **q2_query2_1.png**, and **q2_query2_2.png** in the ***outputs directory** are the screenshots of the querying results aftering running the code on the [Studio](https://lightning.ai/lightning-ai/studios/document-search-and-retrieval-using/rag).
- **q2_query1.txt** and **q2_query2.txt** in the **outputs directory** are the querying results aftering running the code on the [Studio](https://lightning.ai/lightning-ai/studios/document-search-and-retrieval-using/rag).
- **q3.png** in the **outputs directory** is the screenshot of [RAG PDF Chatbot's](https://huggingface.co/spaces/MuntasirHossain/RAG-PDF-Chatbot) result.
- **q3.txt** in the **outputs directory** describes the RAG steps involved in the Python calls and explains how the UI works of the [RAG PDF Chatbot](https://huggingface.co/spaces/MuntasirHossain/RAG-PDF-Chatbot) in [HuggingFace](https://huggingface.co/spaces) on [HuggingFace](https://huggingface.co/) works.
