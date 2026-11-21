# Lesson 05 - Generative AI and Large Language Models

**Time:** 40 minutes  |  **Notebook:** `notebooks/05_How_Generative_AI_Works.ipynb`

---

## Goal

By the end of this lesson you can explain:

- **generative** vs **discriminative** AI,
- what a **Large Language Model (LLM)** is,
- the **Transformer** architecture and **attention**,
- **tokens** and **tokenisation**, **context windows** and **parameters**,
- **pre-training**, **fine-tuning** and **inference**,
- **multimodal** models.

---

## Understand

### 1. Generative vs discriminative

| | Discriminative AI | Generative AI |
|---|---|---|
| Job | **Decides or labels** | **Creates new content** |
| Question | "Is this email spam?" | "Write an email to my teacher." |
| Output | A label or a number | Text, images, audio, video, code |
| Examples | Day 1 models, spam filter, face unlock | Gemini, ChatGPT, Claude, image generators, music generators |

A simple way to remember: discriminative models draw a **line between** things; generative models learn **what the things look like** so well that they can make new ones.

Generative AI types: **text** (LLMs), **images** (Imagen, Midjourney, Stable Diffusion), **audio and music**, **video** (Veo, Sora), **code** (Copilot, Claude Code).

### 2. What is a Large Language Model?

An **LLM** is a very big neural network trained on a huge amount of text (books, websites, code) to do one simple job:

> **Predict the next token.**

```text
Input:  "The capital of India is"
Model:  next token probabilities ->  " New" 0.92,  " Delhi" 0.03,  " a" 0.01 ...
Pick " New", add it, repeat:  "The capital of India is New" -> " Delhi" ...
```

By repeating "predict the next token" again and again, it writes whole answers. Because it saw so much text, predicting well forces it to learn grammar, facts, reasoning patterns and even coding.

- **Large** = billions of parameters and trillions of words of training text.
- Examples: Gemini (Google), GPT (OpenAI), Claude (Anthropic), Llama (Meta), Mistral, and many open models.

**Important:** an LLM predicts **likely** text, not **verified** truth. That is why it can confidently say wrong things (**hallucinations**, Lesson 10).

### 3. Tokens and tokenisation

LLMs do not read whole words; they read **tokens** - pieces of words.

```text
"unbelievable"  ->  "un" + "believ" + "able"      (3 tokens)
"Hello world!"  ->  "Hello" + " world" + "!"      (3 tokens)
```

- Rough rule in English: **1 token is about 3/4 of a word** (100 tokens are about 75 words).
- Other languages and code often use more tokens per word.
- **Why care?** API **prices** and **limits** are counted in tokens.

### 4. Context window

The **context window** is how many tokens the model can "see" at one time - your question, any documents you include, the chat history **and** its answer together.

- Older models: about 4,000 tokens (a few pages).
- Modern models: hundreds of thousands to over a million tokens (whole books).
- If you go over the limit, older text is cut off or you get an error. The model has **no memory** outside this window; chat apps "remember" by sending the earlier messages again each time.

### 5. Parameters

**Parameters** are the **weights and biases** inside the network (Lesson 01) - the numbers learned in training. Small models have a few billion; the largest have hundreds of billions or more. More parameters can mean more knowledge and skill, but also more cost and slower answers.

### 6. The Transformer and attention

In 2017 Google researchers published the **Transformer**. Almost every modern LLM is built on it (the "T" in GPT stands for Transformer).

The key idea is **attention**: when the model processes a word, it **looks at all the other words** and decides **which ones matter most** for understanding it.

```text
"The animal did not cross the street because IT was too tired."
                                              ^
When reading "it", attention puts most weight on "animal" (not "street").
Change "tired" to "wide" and attention moves to "street".
```

Why Transformers won:

- They read **all words at once** (in parallel), not one by one like RNNs, so they train fast on GPUs.
- Attention connects words that are **far apart**, so they handle long text well.
- They grow better and better as you make them bigger and give more data.

A Transformer stacks many layers of **attention + small neural networks**, often dozens of layers.

### 7. The life of an LLM: pre-training, fine-tuning, inference

| Stage | What happens | Analogy |
|---|---|---|
| **Pre-training** | Learns to predict the next token on a huge amount of general text. Takes months and huge numbers of GPUs. Result: a "base model". | Reading the whole library |
| **Fine-tuning** | Extra training on smaller, focused data - for example question-answer examples, to follow instructions and chat helpfully. Often with **RLHF** (people rate answers). Companies can also fine-tune for their own field (legal, medical). | Training for a specific job |
| **Inference** | **Using** the trained model to answer prompts. This is what happens every time you send a message. | Doing the job |

You will mostly do **inference** through an **API**. Instead of fine-tuning, most apps use **prompting** and **RAG** (Lesson 08) because they are cheaper and faster.

### 8. Temperature

When picking the next token, the model can be **safe** or **creative**:

- **Low temperature (0 to 0.3):** almost always picks the most likely token. Focused, repeatable. Good for facts, code, data extraction.
- **High temperature (0.8 to 1.5):** sometimes picks less likely tokens. More creative and varied. Good for stories and brainstorming.

### 9. Multimodal models

**Multimodal** = understands (and sometimes produces) **more than one type** of data: text, images, audio, video, PDFs.

Examples: upload a photo of a plant and ask what disease it has; give a chart and ask for a summary; talk by voice; read a handwritten note (like OCR). Gemini, GPT and Claude are all multimodal.

---

## Do it now

Open `notebooks/05_How_Generative_AI_Works.ipynb`, select the `.venv` kernel and run every cell. No API key needed. You will:

- build a tiny **generative model** that writes new sentences by predicting the next word,
- see **tokenisation** and count tokens,
- see how **temperature** changes probabilities,
- calculate **attention** weights with numpy.

---

## Check

- [ ] The tiny language model generates new sentences that sound like the training text.
- [ ] Low temperature gives almost the same output each time; high temperature gives varied output.
- [ ] The attention table shows "it" paying most attention to "animal".

---

## What just happened?

You built, in about 30 lines, the same basic loop that real LLMs use: **look at the context -> get next-token probabilities -> pick one (with temperature) -> repeat**. Real LLMs replace our simple word counts with a giant Transformer that uses attention over thousands of tokens.

---

## Try it yourself

1. Train the tiny model on `healthy_study_habits.txt` instead. What kind of sentences does it make?
2. Explain in your own words why an LLM can "hallucinate".
3. Why do longer chats cost more tokens? (Hint: what is sent again with each message?)

---

## If it does not work

| Problem | Fix |
|---|---|
| Generated text is very short | The model reached a word that never had a next word. Run the cell again or increase `max_words`. |
| `FileNotFoundError` for documents | Open the notebook from inside `notebooks/`, so `../data/documents` exists. |

Next: lunch break, then **[Lesson 06 - Get your free AI key](06_GET_YOUR_FREE_AI_KEY.md)**
