# Group Project Setup Guide: TensorFlow & Keras OCR

Welcome to the team project! To ensure everyone runs the exact same software versions and to avoid "Frankenstein environment" dependency conflicts, please follow this setup guide carefully. 

> ⚠️ **CRITICAL:** Do **NOT** upload your `venv/` folder or `__pycache__/` folders to GitHub. They are local to your machine. The `.gitignore` file will handle this automatically, but please make sure you don't force-add them.

---

## 🚀 Step-by-Step Setup

### 1. Clone the Project & Open it
Open your terminal (or Git Bash) and clone the repository:
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Open the VS Code Terminal
Press Ctrl + ` (or go to Terminal > New Terminal at the top menu). Ensure your terminal is pointing at your project root directory.

### 3. Build a Fresh, Isolated Virtual Environment
Run the following command to build a clean local environment room:
```bash
python -m venv venv
```

### 4.Activate the Environment
You must turn on the virtual environment engine before installing packages.
# Windows:
```bash
.\venv\Scripts\Activate
```
# MacOS:
```bash
source venv/bin/activate
```
You will see a green (venv) at the beginning of the terminal.

# Common Activation Fixes (Windows Only)
If you get an "Execution Policy" Red Error: Windows might block script execution. Bypass it for this VS Code session by running:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 5.Install Dependencies in One Shot
Do not manually install individual libraries. Tell pip to read our shared configuration blueprint file by running:
```bash
pip install -r requirements.txt
```

### Testing Before Starting
Once everything is successfully installed and your environment is activated, run this in terminal:
```bash
python text_extractor.py
```

### Must Do Before Coding
Ensure your Python scripts start exactly like this:
```bash
import sys
import tf_keras

sys.modules['tensorflow.keras'] = tf_keras
sys.modules['keras'] = tf_keras

import keras_ocr
import math

# Your project logic starts below...
```

