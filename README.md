# local-llm-lab

small scripts for learning ai/llm basics, all local with ollama (no api key needed).

## setup

1. install [ollama](https://ollama.com)
2. pull models:
   ```
   ollama pull qwen2.5:7b
   ollama pull nomic-embed-text
   ollama pull llava
   ```
3. install dependencies:
   ```
   pip install -r requirements.txt
   ```

## rag/

- `basicAPIUse.py` – simplest chat call to a local model
- `embedding.py` – turn text into a vector (embeddings)
- `cosineSimilarity.py` – how similar are two texts, measured with cosine similarity
- `firstChain.py` – first langchain pipeline (prompt -> model -> parser), with streaming
- `interactiveCLI.py` – chat loop with conversation history
- `fullRAG.py` – complete RAG example: split text into chunks, embed them, store in chromadb, find the matching chunk for a question and give it to the model as context

best read in the order above, they build on each other roughly.

## vision/

- `scanImage.py` – chat loop with a vision model (llava): load an image by path, then ask questions about it
- `renameImages.py` – pipeline that reads a folder full of images, has llava describe each image, compresses the description into a short filename with qwen2.5, and renames the file accordingly

## known limitations

- `fullRAG.py` only fetches the single most similar chunk (n_results=1), no reranking
- history in `interactiveCLI.py` is not saved (lost after closing)
- everything designed for german prompts, not tested with other languages
- `vision/scanImage.py` still has a few loose ends (commented-out code, a debug print)
