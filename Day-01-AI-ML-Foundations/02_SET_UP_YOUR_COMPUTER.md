# Lesson 02 - Set Up Your Computer

**Time:** 40 minutes  |  **You need:** internet, permission to install software

You do this **one time** for the whole course. Days 2, 3 and 4 use the same setup.

---

## Goal

By the end of this lesson:

- Python 3.12 and VS Code are installed,
- you have a **virtual environment** for this course,
- all the packages (numpy, pandas, scikit-learn and others) are installed,
- you can open a **Jupyter notebook** and run code in it.

---

## Understand

### What is Python?

Python is the programming language we use. Almost all AI and Machine Learning work in the world is done in Python, because it is easy to read and has ready-made packages for AI.

### What is VS Code?

VS Code (Visual Studio Code) is a free **editor** - a program where you read and write code. It also has a **terminal** and can run **notebooks**.

### What is a terminal?

A **terminal** is a window where you type commands instead of clicking. VS Code has one built in.

### What is a package, and what is `pip`?

A **package** is code written by other people that we can reuse. For example, `pandas` is a package for working with tables.
`pip` is Python's **app store**. It downloads and installs packages.

### What is a virtual environment (`.venv`)?

Imagine each school subject has its own bag. Your maths bag has maths books; your science bag has science books. They never get mixed up.

A **virtual environment** is a separate "bag" of Python packages for **one** project. The packages for this course live inside a folder called `.venv` and never mix with other projects on your computer.

### What is `requirements.txt`?

It is a **shopping list** of packages. Instead of installing 16 packages one by one, you give pip the whole list in one command. It is in the **main course folder**.

### What is a Jupyter notebook?

A notebook (`.ipynb` file) is a page made of **cells**:

- **Text cells** explain things.
- **Code cells** contain Python. You run a code cell with **Shift + Enter**, and the answer appears right under it.

It is perfect for learning because you see the result of every small step.

---

## Do it now

### Step 1 - Install Python 3.12

1. Go to https://www.python.org/downloads/
2. Download **Python 3.12** (if the big button shows 3.13 or 3.14, scroll down to "Looking for a specific release?" and pick the newest **3.12.x**). 3.11 and 3.13 also work, but 3.12 is the safest for all our packages.
3. Run the installer.
   - **Windows:** on the first screen, tick **"Add python.exe to PATH"**. This is very important. Then click **Install Now**.
   - **macOS:** open the downloaded `.pkg` file and click Continue until it finishes.
   - **Linux (Ubuntu):** Python is usually already installed. Run `sudo apt install python3 python3-venv python3-pip` in a terminal.

### Step 2 - Install VS Code and two extensions

1. Download VS Code from https://code.visualstudio.com/ and install it (keep all default options).
2. Open VS Code.
3. Click the **Extensions** icon on the left side (it looks like four small squares).
4. Search **Python** and install the one by **Microsoft**.
5. Search **Jupyter** and install the one by **Microsoft**.

### Step 3 - Open the course folder in VS Code

1. In VS Code: **File -> Open Folder...**
2. Select the **main course folder** `Applied_AI_ML_Training_Proposal_CSE_Students` (the one that contains `00_START_HERE.md` and `requirements.txt`). Do **not** select the `Day-01` folder.
3. Click **Select Folder**. If VS Code asks "Do you trust the authors?", click **Yes, I trust the authors**.

### Step 4 - Open a terminal

In VS Code: **Terminal -> New Terminal**. A panel opens at the bottom.

The line should end with the course folder name, for example:

```text
PS D:\Applied_AI_ML_Training_Proposal_CSE_Students>
```

### Step 5 - Check Python

Type this and press **Enter**:

```powershell
python --version
```

You should see something like `Python 3.12.8`.

If you see an error or a different version:

- **Windows:** try `py -3.12 --version`. If that works, use `py -3.12` instead of `python` in Step 6 only.
- **macOS / Linux:** try `python3 --version` and use `python3` instead of `python` in Step 6 only.

### Step 6 - Create the virtual environment

```powershell
python -m venv .venv
```

Wait about 10 seconds. A new folder called **`.venv`** appears in the Explorer on the left.

### Step 7 - Switch the virtual environment ON (activate it)

Pick the command for **your** computer:

**Windows - PowerShell** (the VS Code default on Windows):

```powershell
.venv\Scripts\Activate.ps1
```

**Windows - Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

You should now see **`(.venv)`** at the start of the line:

```text
(.venv) PS D:\Applied_AI_ML_Training_Proposal_CSE_Students>
```

**Every time you open a new terminal, you must activate `.venv` again.** If you do not see `(.venv)`, run the activate command again.

### Step 8 - Install all the packages

Make sure the line starts with `(.venv)`. Then run these two commands, one after the other:

```powershell
python -m pip install --upgrade pip
```

```powershell
pip install -r requirements.txt
```

This downloads about 500 MB. It can take 3 to 10 minutes depending on your internet. At the end you should see a line that starts with `Successfully installed ...`.

### Step 9 - Open your first notebook

1. In the Explorer on the left, open **Day-01-AI-ML-Foundations -> notebooks -> 00_Check_Your_Setup.ipynb**.
2. At the top right of the notebook, click **Select Kernel** (a "kernel" is the Python that runs the notebook).
3. Choose **Python Environments...** and then the one that shows **`.venv`** (for example `.venv (Python 3.12.8)`).
4. Click the first code cell, then press **Shift + Enter**. Keep pressing **Shift + Enter** to run each cell from top to bottom.
   - Or click **Run All** at the top to run every cell at once.

---

## Check

All of these must be true:

- [ ] The terminal line starts with **`(.venv)`**.
- [ ] `pip install -r requirements.txt` ended with `Successfully installed`.
- [ ] In `00_Check_Your_Setup.ipynb`, the last cell prints **`ALL GOOD - you are ready for Day 1.`**
- [ ] The notebook shows a small line chart.

---

## What just happened?

- You installed **Python** (the language) and **VS Code** (the editor).
- `python -m venv .venv` created a private package "bag" called `.venv`.
- Activating it told the terminal: "use the Python **inside** `.venv`".
- `pip install -r requirements.txt` read the shopping list and installed every package for all 4 days into `.venv`.
- Selecting the `.venv` kernel told the notebook to use that same Python, so the notebook can see the packages.

The most important packages for today:

| Package | What it does for us | Short name in code |
|---|---|---|
| `numpy` | Fast maths on lists of numbers | `np` |
| `pandas` | Tables of data (rows and columns), like Excel in Python | `pd` |
| `matplotlib` | Charts | `plt` |
| `scikit-learn` | Ready-made machine learning algorithms | `sklearn` |

---

## Try it yourself

1. Close the terminal (click the bin icon on the terminal panel).
2. Open a **new** terminal (**Terminal -> New Terminal**).
3. Is `(.venv)` there? (Usually VS Code activates it for you. If not, run the Step 7 command.)
4. In the notebook, add a new code cell (click **+ Code**), type `print(2 + 3)` and press **Shift + Enter**.

---

## No permission to install? Use Google Colab (plan B)

If you cannot install software (for example on a locked college computer), you can run the notebooks in your web browser for free with **Google Colab**:

1. Go to https://colab.research.google.com/ and sign in with a Google account.
2. Click **File -> Upload notebook** and choose a notebook from the `notebooks` folder.
3. On the left side, click the **folder icon**, then the **upload icon**, and upload the CSV file the notebook needs (from the `data` folder). It goes into the current folder of Colab.
4. Run the cells with **Shift + Enter**. Colab already has numpy, pandas, matplotlib and scikit-learn installed.

Our notebooks look for the data in `../data` first and in the current folder second, so they work in both places.
Note: Days 3 and 4 (building and deploying an app) need a real computer.

---

## If it does not work

| Problem | Fix |
|---|---|
| `python` is not recognized | Python is not on PATH. Run the installer again, choose **Modify**, tick **Add Python to environment variables**, then **close and reopen VS Code**. Or use `py -3.12` instead of `python`. |
| PowerShell says **"running scripts is disabled on this system"** | Run this once: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` and type `Y`. Then activate again. Or switch the terminal to **Command Prompt** (down-arrow next to **+** in the terminal panel) and use `.venv\Scripts\activate.bat`. |
| `pip install` fails with a long red error about building a package | You probably have a very new Python (for example 3.14) that some packages do not support yet. Install Python 3.12, delete the `.venv` folder, and repeat from Step 6 using `py -3.12 -m venv .venv`. |
| `pip install` stops with a timeout or network error | Your internet dropped. Run the same command again. pip continues where it stopped. |
| The notebook says **"Select Kernel"** and `.venv` is not in the list | Click **Select Another Kernel... -> Python Environments**. If still missing, close VS Code, open it again, and make sure you opened the **main course folder**. |
| The notebook asks to **install ipykernel** | Click **Install**. Or in the activated terminal run `pip install ipykernel`. |
| `ModuleNotFoundError: No module named 'pandas'` in the notebook | The notebook uses the wrong Python. Click the kernel name at the top right and choose the `.venv` one. |
| Mac says `command not found: python` | Use `python3` instead of `python`. |

Next: **[Lesson 03 - How machines learn](03_HOW_MACHINES_LEARN.md)**
