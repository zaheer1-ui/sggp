importai
openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful examiner."},
        {"role": "user", "content": "Evaluate this answer: ..."},
    ]
)

print(response.choices[0].message["content"])
