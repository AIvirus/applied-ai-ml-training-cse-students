# Lesson 01 - Deep Learning and Neural Networks

**Time:** 40 minutes  |  **Notebook:** `notebooks/01_Neural_Networks.ipynb`

---

## Goal

By the end of this lesson you can explain:

- what a **neural network** is and how an **artificial neuron** works,
- **weights**, **bias**, **layers** and **activation functions**,
- **loss functions** and **optimisation**,
- **epochs** and **batches**,
- the basic idea of **CNNs** (for images) and **RNNs** (for sequences).

---

## Understand

### 1. What is Deep Learning?

**Deep Learning** is machine learning that uses **neural networks** with **many layers** ("deep" = many layers). It is the technology behind face unlock, voice assistants, Google Translate, self-driving features and chatbots like Gemini and ChatGPT.

Why is it so powerful? Classic ML (Day 1) needs **people** to design good features. Deep learning learns the features **by itself** from raw data like pixels, sound waves or text.

### 2. The artificial neuron

A neural network is built from tiny units called **neurons**. The idea comes loosely from brain cells, but an artificial neuron is just simple maths.

A neuron does 3 things:

```text
inputs        weights
 x1 --------- w1 ---\
 x2 --------- w2 ----+--> [ sum = x1*w1 + x2*w2 + x3*w3 + bias ] --> [ activation ] --> output
 x3 --------- w3 ---/
```

1. **Multiply** each input by a **weight**. The weight says how important that input is.
2. **Add** them all up, plus a **bias** (a number that shifts the result up or down, like a starting point).
3. Pass the sum through an **activation function**, which decides the final output.

**Daily life example - should I go out to play?**

| Input | Value | Weight (importance) |
|---|---|---|
| Is it sunny? | 1 (yes) | +3 |
| Is homework finished? | 0 (no) | +4 |
| Is it very hot? | 1 (yes) | -2 |

Sum = 1x3 + 0x4 + 1x(-2) + bias(-1) = 0. If the activation says "go if sum > 0", the answer is **no**.
**Learning** = finding the right weights and bias from examples.

### 3. Activation functions

Without activation functions, a network could only learn straight lines, no matter how many layers it has. Activations add "bends" so networks can learn complex patterns.

| Activation | What it does | Used for |
|---|---|---|
| **Sigmoid** | Squeezes any number into 0 to 1 | Output of yes/no problems (a probability) |
| **ReLU** | Negative numbers become 0, positive stay the same | Hidden layers - the most common choice today |
| **Tanh** | Squeezes into -1 to 1 | Some older networks, RNNs |
| **Softmax** | Turns many numbers into probabilities that add up to 1 | Output when there are many classes (digit 0 to 9) |

### 4. Layers

Neurons are arranged in **layers**:

```text
 INPUT LAYER        HIDDEN LAYERS            OUTPUT LAYER
 (the data)     (find patterns step by step)   (the answer)

   pixel 1 ---O---\      O         O
   pixel 2 ---O----+---- O ------- O ------\
   pixel 3 ---O----+---- O ------- O --------> O  "it is a 7" (probability 0.97)
     ...       ...       ...       ...
```

- **Input layer:** receives the data (for example 64 pixel values of a small image).
- **Hidden layers:** in the middle. Early layers learn simple things (edges), later layers combine them into complex things (shapes, faces).
- **Output layer:** gives the final answer.

### 5. How a network learns: loss and optimisation

The same idea as Day 1 Lesson 04:

1. **Forward pass:** data goes through the network and it makes a prediction.
2. **Loss function:** measures how wrong the prediction is. Common ones:
   - **Mean squared error** for numbers (regression).
   - **Cross-entropy** (log loss) for classes (classification).
3. **Backpropagation:** works out how much each weight caused the error, going backwards from the output to the input.
4. **Optimisation:** the **optimiser** (gradient descent, or improved versions like **Adam**) nudges every weight a little to reduce the loss.
5. Repeat.

### 6. Epochs and batches

- **Batch:** a small group of examples (for example 32) that the network looks at before it updates its weights once. Smaller pieces fit in memory and help learning.
- **Epoch:** one full pass over **all** the training data. If you have 3,200 examples and a batch size of 32, one epoch = 100 updates.
- Training usually runs for many epochs. We watch the loss go down and stop before overfitting.

### 7. CNN - Convolutional Neural Network (for images)

A **CNN** slides small **filters** (for example 3 x 3 pixels) across an image, like moving a magnifying glass. Each filter learns to detect one pattern - a vertical edge, a curve, an eye. Deeper layers combine these into bigger patterns.

```text
image -> [filters find edges] -> [filters find shapes] -> [filters find objects] -> "cat"
```

CNNs are used for photo tagging, medical scans, face detection and OCR. You will try a filter by hand in the Computer Vision notebook.

### 8. RNN - Recurrent Neural Network (for sequences)

Some data comes **in order**: words in a sentence, sounds in speech, stock prices over days. An **RNN** reads one item at a time and keeps a **memory** (hidden state) of what came before. An improved version is called **LSTM**.

Today, **Transformers** (Lesson 05) have replaced RNNs for most language tasks because they read all words at once and handle long text better.

### 9. Tools for deep learning

| Tool | Notes |
|---|---|
| **PyTorch** | Most popular in research and industry today |
| **TensorFlow / Keras** | Popular, Keras is very beginner-friendly |
| **scikit-learn MLPClassifier** | A small, simple neural network - perfect for learning (we use it today) |

Real deep learning often needs a **GPU** (a graphics chip that does many small calculations at once). Free GPUs are available in Google Colab. Today's examples are small enough for any laptop.

---

## Do it now

Open `notebooks/01_Neural_Networks.ipynb`, select the `.venv` kernel and run every cell. You will:

- build one neuron by hand with numpy,
- plot the activation functions,
- train a neuron with gradient descent and watch the loss fall,
- see why one neuron cannot solve the XOR problem, and how a hidden layer solves it,
- train a real neural network that reads handwritten digits.

---

## Check

- [ ] The "play outside" neuron prints a decision.
- [ ] You see a chart of sigmoid, ReLU and tanh.
- [ ] The single neuron learns AND but **fails** XOR; the network with a hidden layer **solves** XOR.
- [ ] The digit-reading network reaches about **95 percent** or higher test accuracy.

---

## What just happened?

- A neuron = weighted sum + bias + activation. That is all.
- Training = forward pass, loss, backpropagation, update - repeated over many epochs and batches.
- One neuron can only draw one straight line. **Hidden layers** let networks learn curved, complex patterns. More layers = "deeper".

---

## Try it yourself

1. In the XOR cell, change the number of hidden neurons from 4 to 2, then to 8. Does it still learn?
2. In the digits cell, change `hidden_layer_sizes=(64,)` to `(16,)` and to `(128, 64)`. What happens to accuracy and training time?
3. In your own words: what is the difference between an epoch and a batch?

---

## Optional: install PyTorch

Not needed for this course. If you want to explore later: go to https://pytorch.org/get-started/locally/, choose your system and **CPU**, and run the command it shows (it is large, about 200 MB to 2 GB).

---

## If it does not work

| Problem | Fix |
|---|---|
| `ConvergenceWarning: Stochastic Optimizer: Maximum iterations reached` | Only a warning: the network could learn more. Increase `max_iter`. |
| XOR result is not perfect | Neural networks start with random weights. Run the cell again or change `seed`. |
| Training is slow | Use fewer hidden neurons or fewer epochs. |

Next: **[Lesson 02 - Natural Language Processing](02_NLP.md)**
