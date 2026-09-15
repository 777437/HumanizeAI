import ollama


DEFAULT_MODEL = "qwen2.5:3b"


def get_installed_models():
    """Return Ollama models installed on this computer."""

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
You are a rewriting engine.

Your ONLY job is to rewrite the user's text.

DO NOT return the original text unchanged.

You MUST change the wording and sentence structure while keeping
the exact meaning and important information.

Writing style: {tone}

STRICT RULES:

- Rewrite EVERY sentence.
- Change sentence structure.
- Replace some words with natural alternatives.
- Make the writing sound like a real person wrote it.
- Keep the same meaning.
- Keep important facts, names, numbers, and technical terms.
- Do not add new information.
- Do not remove important information.
- Do not explain what you changed.
- Do not mention AI.
- Do not say "Here is the rewritten text".
- Do not use quotation marks around the answer.
- Return ONLY the rewritten version.

IMPORTANT:

Even if the original sentence already sounds natural,
you MUST rewrite it using different wording.

For example:

Original:
"Artificial intelligence is becoming an important part of modern technology."

Rewrite:
"AI is becoming a major part of today's technology."

Another example:

Original:
"Students can use this system to improve their writing."

Rewrite:
"This system allows students to make their writing better."

Another example:

Original:
"The system collects sensor data and sends it to the cloud."

Rewrite:
"Sensor readings are collected by the system and then sent to the cloud."

Now rewrite the following text:

{text}
"""

    try:

        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a text rewriting assistant. "
                        "Always rewrite the input. "
                        "Never return the input unchanged."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.8,
                "top_p": 0.9
            }
        )

        result = response["message"]["content"].strip()

        # Remove accidental prefixes
        prefixes = [
            "Here is the rewritten text:",
            "Here is the rewritten version:",
            "Rewritten text:",
            "Rewritten version:"
        ]

        for prefix in prefixes:
            if result.lower().startswith(prefix.lower()):
                result = result[len(prefix):].strip()

        return result

    except Exception as error:

        print("OLLAMA HUMANIZATION ERROR:", error)

        raise