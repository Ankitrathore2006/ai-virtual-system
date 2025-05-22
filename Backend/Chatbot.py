from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import dotenv_values

# Load environment variables from .env
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Create Groq client
client = Groq(api_key=GroqAPIKey)

# Define system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Ensure the Data folder and ChatLog file exist
os.makedirs("Data", exist_ok=True)
if not os.path.exists("Data/ChatLog.json"):
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        "Please use this real-time information if needed.\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds.\n"
    )

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def ChatBot(query):
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
        )

        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})

        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(answer)

    except Exception as e:
        print(f"Error: {e}")
        with open("Data/ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(query)

# CLI entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ChatBot(user_input)
        print(response)
