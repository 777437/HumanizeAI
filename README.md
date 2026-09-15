# HumanizeAI

### A free, open-source AI humanizer that runs locally on your computer.

**HumanizeAI by Ramzan Ali**

HumanizeAI uses local AI models through **Ollama** to rewrite text in a more natural and readable way.

No paid API.
No API key.
No cloud AI required.

Your computer runs the AI.

---

## What is HumanizeAI?

HumanizeAI is a simple web application that allows you to:

- Rewrite AI-generated text
- Make writing sound more natural
- Choose different writing styles
- Check AI-like writing patterns
- Run everything locally
- Use different Qwen models depending on your computer

The goal is to make it easy for anyone to create their own local AI humanizer.

---

## Features

| Feature | Available |
|---|---|
| AI Humanizer | Yes |
| Local AI processing | Yes |
| Ollama support | Yes |
| Qwen models | Yes |
| AI-likeness checker | Yes |
| Natural writing style | Yes |
| Student style | Yes |
| Professional style | Yes |
| Casual style | Yes |
| Academic style | Yes |
| Simple style | Yes |
| Word counter | Yes |
| Character counter | Yes |
| Copy result | Yes |
| 1000-word limit | Yes |
| Paid API required | No |

---

# How HumanizeAI Works

```text
             YOUR COMPUTER
                   |
                   v
        +---------------------+
        |    HumanizeAI UI    |
        |     Flask Website   |
        +----------+----------+
                   |
                   v
        +---------------------+
        |     Flask Backend   |
        +----------+----------+
                   |
                   v
        +---------------------+
        |       Ollama        |
        +----------+----------+
                   |
                   v
        +---------------------+
        |      Qwen Model     |
        +----------+----------+
                   |
                   v
           Humanized Text