# Lesson 08 - Embeddings, Semantic Search and RAG

**Time:** 40 minutes  |  **Notebook:** `notebooks/07_Embeddings_and_RAG.ipynb`

This is the most important lesson for Day 3, because our project (Study Buddy) is built on exactly these ideas.

---

## Goal

By the end of this lesson you can explain and build:

- **embeddings** and **similarity**,
- **semantic search**,
- what a **vector database** is,
- **document chunking**,
- **Retrieval-Augmented Generation (RAG)**,
- **retrieval** and **reranking**.

---

## Understand

### 1. The problem RAG solves

An LLM only knows what was in its training data. It does **not** know:

- your college's library rules,
- your company's private documents,
- news from after its training ended.

If you ask, it may **guess** and give a confident wrong answer (hallucination). We need a way to give the model **the right information at the moment you ask**. That is RAG.

### 2. Embeddings - meaning as numbers

An **embedding** is a list of numbers (a vector, often 768 or more numbers) that represents the **meaning** of a piece of text. An embedding model is trained so that **texts with similar meaning get similar vectors** - even if they use different words.

```text
"How much is the fine for late books?"   -> [0.12, -0.80, 0.33, ...]
"Late return penalty for library items"  -> [0.10, -0.78, 0.35, ...]   very similar
"Jupiter has a giant storm"              -> [-0.65, 0.21, -0.04, ...]  very different
```

### 3. Similarity - how close are two vectors?

We use **cosine similarity**: it measures the angle between two vectors.

- **1.0** = same direction = same meaning
- **0** = unrelated
- (negative = opposite, rare for text)

### 4. Semantic search

**Keyword search** finds documents containing **the same words**. **Semantic search** finds documents with **the same meaning**.

| Query | Keyword search | Semantic search |
|---|---|---|
| "penalty for returning books late" | Misses a document that says "fine of 5 rupees per day" (no word "penalty") | Finds it - the meaning matches |

How it works:

1. Turn every document into an embedding once, and store them.
2. Turn the user's question into an embedding.
3. Find the stored vectors **most similar** to the question vector.

### 5. Vector databases

When you have millions of vectors, you need a database built to find similar vectors **fast**. That is a **vector database** (or vector store). It stores: the vector, the original text, and **metadata** (source file, page number, date).

Examples: **Chroma**, **FAISS** (a library from Meta), **Qdrant**, **Pinecone**, **Weaviate**, and **pgvector** (PostgreSQL extension). In our notebook, a numpy array plus a list is our tiny vector store - the idea is identical.

### 6. Document chunking

Documents can be long. We split them into **chunks** (small pieces, for example a paragraph or 500 characters) before embedding. Why?

- A whole book as one vector would be a blurry average of everything.
- Small chunks let us find **the exact part** that answers the question.
- We send only a few relevant chunks to the LLM, which saves tokens and money.

Good practice: chunk by paragraphs or headings, keep chunks a few hundred words, and add a small **overlap** between chunks so a sentence cut in half is not lost.

### 7. RAG - Retrieval-Augmented Generation

**RAG = Retrieve the right chunks, then let the LLM Generate an answer using them.**

```text
                         INDEXING (once)
documents --> split into chunks --> embed each chunk --> store in vector DB

                         ANSWERING (every question)
question --> embed --> RETRIEVE top-k similar chunks --> (RERANK) -->
         --> PROMPT:  "Answer ONLY from this context: <chunks>. Question: <question>"
         --> LLM GENERATES the answer --> show answer + SOURCES
```

Like an **open-book exam**: the student (LLM) does not need to memorise the book; they look up the right page and write the answer.

Benefits:

- Answers are **grounded** in your documents, so fewer hallucinations.
- Can **cite sources** ("from library_rules.txt").
- Update knowledge by just adding documents - no re-training.
- Private data stays in your control.

### 8. Retrieval and reranking

- **Retrieval** = the first fast search that picks maybe the top 10 to 20 chunks by vector similarity. It is quick but rough.
- **Reranking** = a second, more careful step that **re-orders** those candidates and keeps the best 3 to 5. Rerankers are slower but more accurate (special reranker models, or an LLM asked "how relevant is this chunk?"). In the notebook we use a simple keyword-overlap reranker to show the idea.
- **Hybrid search** = combine keyword search and semantic search scores. Very common in real systems.

### 9. A good RAG prompt

```text
You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say: "I could not find this in the documents."
Mention the source file for each fact.

CONTEXT:
[1] (library_rules.txt) If a book is returned late, the fine is 5 rupees per day...
[2] (library_rules.txt) Each student can borrow up to 4 books...

QUESTION: What is the fine for returning a book 3 days late?
```

The "**ONLY**" and "**say you could not find it**" rules are what stop the model from inventing answers.

---

## Do it now

Open `notebooks/07_Embeddings_and_RAG.ipynb`, select the `.venv` kernel and run every cell. You will:

1. create embeddings and compare sentence similarity,
2. do semantic search,
3. chunk the 3 documents in `data/documents/`,
4. build and save a tiny vector store,
5. retrieve and rerank chunks for a question,
6. build a full RAG answer with sources,
7. compare RAG vs no-RAG answers.

In MOCK MODE, embeddings are replaced by simple word-count vectors (they match **words**, not deeper meaning), and the "LLM answer" is the best matching chunk. Everything still runs.

---

## Check

- [ ] The similarity table shows the two library-fine sentences as the most similar pair.
- [ ] The 3 documents are split into about 17 chunks.
- [ ] For "What is the fine for a late book?", the top chunk comes from `college_library_rules.txt`.
- [ ] The RAG answer mentions 5 rupees per day and names the source file.
- [ ] For a question not in the documents, the answer says it could not find it.

---

## What just happened?

You built a complete RAG system in about 60 lines - the same design used by "chat with your PDF" tools and company knowledge assistants. Tomorrow, Study Buddy uses this exact pipeline inside a web app.

---

## Try it yourself

1. Add your own `.txt` file to `data/documents/` (for example notes from a subject) and ask questions about it.
2. Change `top_k` from 3 to 1. Do answers get worse for questions that need two facts?
3. Change `chunk_size` from 400 to 150 characters. What happens to the retrieved chunks?

---

## If it does not work

| Problem | Fix |
|---|---|
| `404 ... embedding model not found` | Check the current embedding model name at https://ai.google.dev/gemini-api/docs/embeddings and set `GEMINI_EMBEDDING_MODEL` in `.env`. Restart the kernel. |
| `ValueError: shapes ... not aligned` | Some vectors came from Gemini and some from mock mode. Restart the kernel and run all cells again. |
| Wrong chunk is retrieved | In mock mode, search matches exact words. Use words that appear in the document, or use a real key. |

Next: **[Lesson 09 - Agentic AI](09_AGENTIC_AI.md)**
