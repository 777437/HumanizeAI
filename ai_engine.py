import ollama


MODEL_NAME = "qwen2.5:3b"


# =========================
# AI HUMANIZER
# =========================

def humanize_text(text, tone="Natural"):

    prompt = f"""
You are an expert human writing assistant.

Rewrite the following text so it sounds naturally written by
a real person while preserving the original meaning and facts.

Writing style: {tone}

IMPORTANT WRITING RULES:

1. Preserve the original meaning and important information.
2. Do not invent facts, examples, statistics, or sources.
3. Use natural vocabulary instead of unnecessarily complicated words.
4. Vary sentence length and sentence structure naturally.
5. Avoid repetitive sentence patterns.
6. Avoid excessive formal or academic filler.
7. Avoid unnecessary transition words such as:
   "Furthermore", "Moreover", "Additionally", "Consequently",
   and "Therefore" unless they genuinely fit the context.
8. Do not overuse semicolons.
9. Avoid unnecessary em dashes (—).
10. Avoid en dashes (–) when a comma or normal sentence structure
    would sound more natural.
11. Avoid double hyphens (--) used as a substitute for an em dash.
12. Prefer commas, periods, or separate sentences when appropriate.
13. Do not make every sentence sound perfectly structured.
14. Keep the writing clear, natural, and easy to read.
15. If the original text contains technical terms, preserve them.
16. Do not add an introduction or explanation.
17. Return ONLY the rewritten text.

Example:

Original:
Artificial intelligence is becoming a crucial part of modern
technology—it helps people complete tasks more efficiently.

Better:
Artificial intelligence is becoming a crucial part of modern
technology. It helps people complete tasks more efficiently.

Now rewrite this text:

{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# =========================
# AI TEXT CHECK
# =========================

def check_ai_text(text):

    prompt = f"""
Analyze the following text for characteristics commonly associated
with AI-generated writing.

This is only an AI-likeness estimate. Do not claim that you can
determine with certainty whether the text was written by a human
or an AI.

Look for patterns such as:

- predictable sentence structures
- repetitive wording
- excessive formal language
- generic explanations
- repetitive transition words
- unusually consistent sentence patterns
- unnecessary em dashes
- excessive semicolon usage
- lack of natural variation

Return ONLY valid JSON.

Use exactly this format:

{{
    "ai_score": 0,
    "human_score": 0,
    "analysis": "Short explanation"
}}

The ai_score and human_score must add up to 100.

Text to analyze:

{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()