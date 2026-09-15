# HumanizeAI

### Make AI Text Sound Human

**HumanizeAI by Ramzan Ali** is an open-source, locally running AI writing assistant that rewrites AI-generated text to make it clearer, more natural, and easier to read.

It runs locally using **Ollama + Qwen**, so your text does not need to be sent to a paid online AI-humanizer service.

---

## What is HumanizeAI?

HumanizeAI takes text like:

> Artificial intelligence has significantly transformed various aspects of modern society.

and rewrites it into a more natural style, for example:

> AI has changed many parts of everyday life and the way people work.

You can choose different writing styles:

- Natural
- Student
- Professional
- Casual
- Academic
- Simple

---

# Features

- Local AI processing
- Powered by Ollama
- Supports Qwen models
- Multiple writing styles
- Up to 1000 words per request
- Automatic Ollama model detection
- Select installed AI models from the interface
- AI-likeness writing-pattern analysis
- Copy humanized text
- Clear input/output
- Beginner-friendly setup
- Open source
- No paid API required

---

# How It Works

```text
Your Text
    ↓
HumanizeAI Web Interface
    ↓
Flask Backend
    ↓
Ollama
    ↓
Qwen Model
    ↓
Humanized Text
    ↓
Your Browser
Requirements

Before installing HumanizeAI, make sure you have:

Windows, Linux, or macOS
Python 3.10+
Ollama
Internet connection for the initial model download
Enough RAM for the Qwen model you choose
Step 1 — Install Python

Download Python from:

https://www.python.org/downloads/

During installation on Windows, make sure you enable:

Add Python to PATH

Check your installation:

python --version

You should see something similar to:

Python 3.x.x
Step 2 — Install Ollama

Download Ollama from:

https://ollama.com/download

Install Ollama normally.

After installation, check:

ollama --version

If Ollama is installed correctly, you should see its version.

Step 3 — Download HumanizeAI

Clone the repository:

git clone https://github.com/777437/HumanizeAI.git

Move into the project:

cd HumanizeAI
Step 4 — Create a Virtual Environment

Create the Python virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

You should now see:

(venv)

at the beginning of your terminal.

Step 5 — Install Python Dependencies

Run:

pip install -r requirements.txt

Wait until the installation finishes.

Step 6 — Choose a Qwen Model

HumanizeAI uses Qwen through Ollama.

The recommended model depends mainly on your computer's available RAM.

Recommended Models
RAM	Recommended Model	Approx. Size	Recommendation
8 GB	qwen2.5:3b	~2 GB	Best for low-RAM laptops
16 GB	qwen2.5:7b	~5 GB	Better quality
32 GB	qwen2.5:14b	~9 GB	Higher quality
64 GB+	Larger Qwen models	Varies	For powerful PCs
8 GB RAM

Install:

ollama pull qwen2.5:3b
16 GB RAM

Install:

ollama pull qwen2.5:7b
32 GB RAM

Install:

ollama pull qwen2.5:14b

You don't need to install every model.

Start with the model suitable for your computer.

Step 7 — Check Your Installed Models

Run:

ollama list

Example:

NAME          SIZE
qwen2.5:3b    1.9 GB

HumanizeAI automatically detects the models installed in Ollama.

You can then select the model from the AI Model dropdown.

Step 8 — Start Ollama

Make sure Ollama is running.

You can test it with:

ollama list

If your model appears, Ollama is ready.

You can also test Qwen directly:

ollama run qwen2.5:3b

Type a simple question.

If Qwen responds, your local AI setup is working.

To exit:

/bye
Step 9 — Start HumanizeAI

Make sure your virtual environment is active:

venv\Scripts\activate

Then run:

python app.py

You should see something similar to:

Running on http://127.0.0.1:5000
Step 10 — Open HumanizeAI

Open your browser and visit:

http://127.0.0.1:5000

You should now see the HumanizeAI interface.

How To Use HumanizeAI
1. Paste your text

Paste your AI-generated text into:

Original Text

Maximum:

1000 words
2. Select your AI model

Choose one of your installed Qwen models.

For example:

qwen2.5:3b
3. Choose a writing style

Select:

Natural

or another available style.

4. Click Humanize Text

HumanizeAI sends your text to your locally running Qwen model through Ollama.

Wait for the result.

5. Copy the result

Click:

Copy

to copy the humanized text.

AI Check

HumanizeAI also includes an experimental AI-likeness checker.

It examines writing patterns such as:

Sentence-length variation
Sentence structure
Writing consistency
Other simple textual patterns

The result is an estimate, not a definitive determination of whether text was written by AI.

For example:

AI-like       20%
Human-like    80%

Do not interpret this as a scientifically validated probability.

Different external AI-detection systems may produce different results.

Why Local AI?

HumanizeAI is designed around local AI processing.

Instead of:

Your Text
   ↓
Online API
   ↓
Remote Server
   ↓
Result

HumanizeAI uses:

Your Text
   ↓
Your Computer
   ↓
Ollama
   ↓
Qwen
   ↓
Result

This makes the project useful for people who want to experiment with AI locally without depending on a paid AI API.

Choosing Between Qwen Models

A larger model does not automatically mean a better experience on every computer.

Lower RAM

Use:

qwen2.5:3b

Advantages:

Lower memory usage
Faster startup
Suitable for normal laptops
Medium RAM

Use:

qwen2.5:7b

Advantages:

Better rewriting quality
Requires more RAM
Can be slower on weaker CPUs
Higher RAM

Use:

qwen2.5:14b

Advantages:

More capable model
Better for complex rewriting
Requires substantially more memory

Choose the largest model your computer can comfortably run.

Installing Another Model

You can install another Qwen model at any time.

For example:

ollama pull qwen2.5:7b

Then check:

ollama list

Refresh HumanizeAI.

The new model should appear automatically in the AI Model dropdown.

Troubleshooting
"No Ollama models were found"

Run:

ollama list

If no models appear, install one:

ollama pull qwen2.5:3b
"AI processing failed"

Make sure Ollama is running.

Test:

ollama list

Then test the model:

ollama run qwen2.5:3b
Model does not appear in HumanizeAI

Run:

ollama list

Confirm the model is installed.

Then restart Flask:

Ctrl + C
python app.py

Refresh the browser.

Port 5000 is already in use

Stop the previous Flask process or change the port in:

app.py

For example:

app.run(
    host="127.0.0.1",
    port=5001,
    debug=True
)

Then open:

http://127.0.0.1:5001
Project Structure
HumanizeAI/
│
├── app.py
├── ai_engine.py
├── requirements.txt
├── test_ai.py
├── test_engine.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── script.js
│   └── style.css
│
└── README.md
Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
Local AI
Ollama
Qwen
Testing
Python test scripts
Open Source

HumanizeAI is an open-source project.

You are welcome to:

Study the code
Modify the project
Experiment with different models
Improve the prompts
Add new writing styles
Improve the UI
Add new features
Submit improvements
Important Note

HumanizeAI is an experimental/open-source project.

The AI Check feature is a lightweight writing-pattern analyzer and not a guaranteed AI detector.

AI detection technology can produce false positives and false negatives.

The project should therefore be used for experimentation, writing improvement, and learning rather than as definitive proof of authorship.

Creator
HumanizeAI by Ramzan Ali

Created by Ramzan Ali.

LinkedIn:

https://www.linkedin.com/in/ramzanali-27544a284/

If you find the project useful, consider giving the repository a ⭐ on GitHub.

Contributing

Want to improve HumanizeAI?

Fork the repository.
Create a new branch.
Make your changes.
Test the project.
Commit your changes.
Create a pull request.

Example:

git checkout -b feature/my-feature

Then:

git add .
git commit -m "Add my feature"
git push origin feature/my-feature
License

This project is open source.

See the repository for the applicable license and usage terms.

HumanizeAI

Local AI. Open source. Simple.

Built with Flask, Ollama and Qwen.

HumanizeAI by Ramzan Ali