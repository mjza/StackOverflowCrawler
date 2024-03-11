# StackOverflowCrawler
A project for extracting questions related different tags from StackOverflow

## Creating the Virtual Environment
First, navigate to your project's root directory in your terminal. Then, create a virtual environment named venv (or another name of your choice) by running:

```
python -m venv venv
```

This command creates a new directory named venv in your project directory, which contains a copy of the Python interpreter, the standard library, and various supporting files.

## Activating the Virtual Environment
Before you can start installing packages, you need to activate the virtual environment. 
Activation will ensure that the Python interpreter and tools within the virtual environment are used in preference to the system-wide Python installation.

1. **On macOS and Linux:**

```
source venv/bin/activate
```

2. **On Windows (cmd.exe):**

```
.\venv\Scripts\activate.bat
```

3. **On Windows (PowerShell) or VSC Terminal:**

```
.\venv\Scripts\Activate.ps1
```

Once activated, your terminal prompt must change to indicate that the virtual environment is active.

## Installing Dependencies
With the virtual environment activated, install the required packages. Ensure you have the following installed in your Python environment. If not, you can install them using pip:

```
pip install requests
pip install html2text
pip install bs4
pip install python-dotenv
pip install colored
```
## Run
Run the `main.py` file to run the program. 
```
python main.py
```