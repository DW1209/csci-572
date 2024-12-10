# Local Running of LLMs

## Description
- Invoke LLMs locally for chat and code generation.

## Usage
### Llama 3 and Gemma 2
#### Install Ollama
Download and install [Ollama](https://ollama.com/) to your desktop.
#### Download Llama 3 Model and Gemma 2 Model
Run these commands to download the Llama 3 model and the Gemma 2 Model.
```bash
$ ollama run llama3
$ ollama run gemma2:2b
```
#### Install Python Packages
Run the command to install the required Python packages.
```bash
$ pip install streamlit ollama litellm
```
#### Run LLMs
Run the command to run the program. It should pop up in your default browser, displaying the streamlit app. **prompt1.txt** in the **inputs directory** is the example prompt.
```bash
$ streamlit run invokeMultipleLLMs.py
```
### Qwen 2.5 Coder
#### Install Ollama
Download and install [Ollama](https://ollama.com/) to your desktop.
#### Download and Run Qwen 2.5 Coder Model
Run the command to download the Qwen 2.5 Coder model. Afterward, it should put up a console where you can enter text prompts that result in code generation. **prompt2.txt** in the **inputs directory** is the example prompt.
```bash
$ ollama run qwen2.5-coder:7b
```

## Explanation
- **q1-1.png**, **q1-2.png**, and **q1-3.png** in the **outputs directory** are the screenshots of the Llama3 and Gamma 2 models' results.
- **q2-1.png** and **q2-2.png** in the **outputs directory** are the screenshots of the Qwen 2.5 Coder model's results.
