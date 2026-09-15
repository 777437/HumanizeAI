import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Rewrite this sentence naturally: Artificial intelligence has significantly transformed modern society."
        }
    ]
)

print(response["message"]["content"])