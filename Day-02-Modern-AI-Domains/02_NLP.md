# Lesson 02 - Natural Language Processing (NLP)

**Time:** 40 minutes  |  **Notebook:** `notebooks/02_NLP_Text_Processing.ipynb`

---

## Goal

By the end of this lesson you can explain and try:

- text processing and **tokenisation**,
- **stop words**, **stemming** and **lemmatisation**,
- **n-grams**,
- **Bag of Words** and **TF-IDF**,
- **word embeddings** and the **Word2Vec** idea,
- **named entity recognition (NER)**,
- **sentiment analysis**, **text classification** and **summarisation**.

---

## Understand

### 1. What is NLP?

**Natural Language Processing** is the part of AI that helps computers **understand and produce human language** - English, Hindi, Tamil and others.

Examples: Google Translate, spam filters, autocorrect, voice assistants, chatbots, searching inside documents, reading customer reviews.

**The big problem:** computers only understand numbers. NLP is mostly about **turning text into numbers** in a smart way, then using ML on those numbers.

### 2. Cleaning and tokenisation

**Tokenisation** = splitting text into small pieces called **tokens** (usually words, sometimes parts of words).

```text
"AI is changing the world!"  ->  ["AI", "is", "changing", "the", "world", "!"]
```

There is also **sentence tokenisation** (split a paragraph into sentences). Before tokenising we often **clean**: make lowercase, remove extra spaces, sometimes remove punctuation.

### 3. Stop words

**Stop words** are very common words that carry little meaning on their own: *the, is, a, an, of, to, and*. For tasks like topic detection we often remove them so the important words stand out.

```text
"the movie is very good"  ->  ["movie", "good"]
```

Careful: sometimes stop words matter. "not good" becomes "good" if you remove "not". For sentiment, keep negation words.

### 4. Stemming and lemmatisation

Both reduce a word to a **base form**, so "play", "plays", "playing" and "played" are treated as the same word.

| | Stemming | Lemmatisation |
|---|---|---|
| How | Chops off word endings with simple rules | Uses a dictionary and grammar |
| "studies" | "studi" (not a real word) | "study" |
| "better" | "better" | "good" (when told it is an adjective) |
| Speed | Very fast | Slower |
| Quality | Rough | Accurate, real words |

### 5. N-grams

An **n-gram** is a group of **n** words in a row.

```text
"I do not like it"
1-grams (unigrams): I | do | not | like | it
2-grams (bigrams):  I do | do not | not like | like it
3-grams (trigrams): I do not | do not like | not like it
```

Bigrams keep a little word order, so "not like" is captured - very useful for sentiment.

### 6. Bag of Words (BoW)

Turns each text into a vector of **word counts**. Word order is lost - like putting all words into a bag and shaking it.

| text | good | movie | bad | very |
|---|---|---|---|---|
| "very good movie" | 1 | 1 | 0 | 1 |
| "bad movie" | 0 | 1 | 1 | 0 |

### 7. TF-IDF

A smarter count. **TF-IDF** = **Term Frequency x Inverse Document Frequency**.

- **TF:** how often a word appears **in this document** (more = more important here).
- **IDF:** how **rare** the word is **across all documents** (rare = more special).

So a word like "the" (everywhere) gets a low score, while "Jupiter" (only in one document) gets a high score. TF-IDF is still widely used for search and text classification.

### 8. Word embeddings and Word2Vec

BoW and TF-IDF do not know that "good" and "great" mean similar things. **Word embeddings** fix this: every word becomes a list of numbers (a vector, for example 300 numbers) so that **words with similar meaning have similar vectors**.

**Word2Vec** (Google, 2013) learns these vectors by reading lots of text and predicting which words appear near each other. The idea: *"You shall know a word by the company it keeps."* Words used in similar places ("tea" and "coffee" both appear near "drink", "cup", "hot") get similar vectors.

Famous result: `vector("king") - vector("man") + vector("woman")` is very close to `vector("queen")`.

Today's LLMs use embeddings too, and you will create real ones in Lesson 08.

### 9. Named Entity Recognition (NER)

**NER** finds and labels **names of things** in text:

```text
"Sundar Pichai visited Bengaluru on Monday to meet Infosys."
 [PERSON]              [LOCATION] [DATE]          [ORGANISATION]
```

Used to pull facts out of documents, resumes, news and invoices.

### 10. Sentiment analysis and text classification

- **Text classification** = putting text into categories: spam / not spam, sports / politics / business, urgent / not urgent.
- **Sentiment analysis** is one kind of text classification: **positive, negative or neutral** feeling. Companies use it to read thousands of reviews automatically.

Two ways to do it:
1. **Rule/lexicon based:** a list of words with scores ("great" +3, "awful" -3). NLTK's **VADER** works like this.
2. **Machine learning:** turn texts into TF-IDF vectors and train a classifier (like Day 1) on labelled examples.

### 11. Summarisation

Making a long text short.

- **Extractive** summarisation picks the most important **existing sentences** (for example, sentences with the most frequent important words).
- **Abstractive** summarisation writes **new sentences**, like a human would. LLMs do this (Lesson 07).

### The classic NLP pipeline

```text
raw text -> clean -> tokenise -> remove stop words -> stem/lemmatise -> vectors (BoW / TF-IDF / embeddings) -> ML model -> answer
```

---

## Do it now

Open `notebooks/02_NLP_Text_Processing.ipynb`, select the `.venv` kernel and run every cell. The first code cell downloads some small NLTK language files - this needs internet **once** and takes about a minute.

---

## Check

- [ ] The download cell ends with `NLTK data ready.`
- [ ] You see tokens, stop-word removal, stems and lemmas for the same sentence.
- [ ] The TF-IDF table shows `jupiter` with a high score only in the solar system document.
- [ ] Your sentiment classifier is trained on `reviews.csv` and correctly labels new sentences that you type.
- [ ] An extractive summary of the solar system notes is printed.

---

## What just happened?

You built a complete classic NLP pipeline with **NLTK** (a teaching and research toolkit) and **scikit-learn**. You turned text into numbers in three ways (counts, TF-IDF, and the idea of embeddings) and trained a real sentiment classifier.

---

## Try it yourself

1. Type 3 reviews of your own (including a tricky one like "not bad at all") and test both the VADER and the ML sentiment models.
2. Change `ngram_range=(1, 1)` to `(1, 2)` in the classifier. Does it handle "not good" better?
3. Run the summariser on `healthy_study_habits.txt` with 2 sentences.

---

## If it does not work

| Problem | Fix |
|---|---|
| `LookupError: Resource punkt_tab not found` | The download cell did not finish. Check your internet and run the download cell again. |
| Download is blocked (college firewall) | Use a mobile hotspot once, or skip the NER cell - the rest still works. |
| `SSL: CERTIFICATE_VERIFY_FAILED` on Mac | Open Finder -> Applications -> Python 3.12 -> double-click `Install Certificates.command`, then try again. |
| NER cell prints an error | NER needs extra files. It is optional. Continue with the next cell. |

Next: **[Lesson 03 - Computer Vision](03_COMPUTER_VISION.md)**
