
import atexit
import os
import uuid

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from posthog import Posthog

client = OpenAI()

_posthog = Posthog(
    os.environ.get("POSTHOG_PROJECT_TOKEN", ""),
    host=os.environ.get("POSTHOG_HOST", "https://us.i.posthog.com"),
    enable_exception_autocapture=True,
)
atexit.register(_posthog.shutdown)

_session_id = str(uuid.uuid4())

print("\n🏦 Broker Chatbot (Insurance Assistant)")
print("Type 'exit' anytime to stop\n")

_posthog.capture(distinct_id=_session_id, event="chat_session_started")

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

turn_count = 0

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye 👋")
        _posthog.capture(
            distinct_id=_session_id,
            event="chat_session_ended",
            properties={"total_turns": turn_count},
        )
        break

    turn_count += 1

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    _posthog.capture(
        distinct_id=_session_id,
        event="chat_message_sent",
        properties={
            "message_length": len(user_input),
            "turn_number": turn_count,
        },
    )

    try:
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
    except Exception as e:
        _posthog.capture_exception(e, distinct_id=_session_id)
        raise
