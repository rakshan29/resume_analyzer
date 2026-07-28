#api = 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
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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",
)

try:
    # We'll use Llama 3.3 70B, which is excellent for technical tasks
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello Groq! Give me a 1-sentence explanation of why eBPF is useful for DDoS mitigation.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    # Print the response
    print("--- Groq Response ---")
    print(chat_completion.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")