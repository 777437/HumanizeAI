from ai_engine import humanize_text


text = """
Precision agriculture uses sensors and IoT technology
to collect information about soil moisture, temperature,
humidity and rainfall. This information can help farmers
make better decisions about irrigation and crop management.
"""


result = humanize_text(
    text,
    tone="Student"
)


print("\n===== HUMANIZED TEXT =====\n")
print(result)
print("\n===========================\n")