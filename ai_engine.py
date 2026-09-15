import ollama


DEFAULT_MODEL = "qwen2.5:3b"


def get_installed_models():
    """
    Return a list of Ollama models installed on this computer.
    """

    try:

        response = ollama.list()

        models = []

        for model in response.models:

            if model.model:
                models.append(model.model)

        return models

    except Exception as error:

        print("OLLAMA MODEL ERROR:", error)

        return []


def humanize_text(text, tone="Natural", model=None):

    if not model:
        model = DEFAULT_MODEL

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
9. Avoid unnecessary em dashes.
10. Avoid unnecessary en dashes.
11. Avoid double hyphens used as a substitute for an em dash.
12. Prefer commas, periods, or separate sentences when appropriate.
13. Do not make every sentence sound perfectly structured.
14. Keep the writing clear, natural, and easy to read.
15. Preserve technical terms when necessary.
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
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()