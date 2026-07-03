
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

print("\n🏦 Broker Chatbot (Insurance Assistant)")
print("Type 'exit' anytime to stop\n")

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a senior commercial insurance broker with expertise in "
            "General Liability, Workers Compensation, Commercial Auto, "
            "Commercial Property, and Professional Liability. "
            "You help insurance agents and business owners understand "
            "coverage, exclusions, underwriting requirements, and "
            "real-world examples. "
            "Always explain concepts in simple, practical language and "
            "give examples whenever possible."
        )
    }
]
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye 👋")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=conversation_history
    )

    answer = response.output_text

    print("\nBot:", answer, "\n")

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })