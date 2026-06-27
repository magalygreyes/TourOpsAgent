import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "In one sentence, greet me as a tour ops assistant."}
    ],
)

print(msg.content[0].text)
