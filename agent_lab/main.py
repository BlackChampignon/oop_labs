import requests
from datetime import datetime
import random

class Agent():
    def __init__(self, memory_tier=1, think=False):
        name = "Gena"
        personality = "A grumpy pirate, who answers in short sentences"
        self.system_prompt = f"Your name is {name}, {personality}"
        self.system_prompt += " /think" if think else " /no_think"
        self.client = LMStudioClient()
        self.memory = Memory()
        match memory_tier:
            case 1:
                Memory.tier1()
            case 2:
                Memory.tier2()
            case 3:
                Memory.tier3()
        self.toolbox = Toolbox()

    def chat(self, content):
        self.memory.create_message(content, role="user")
        history = [{"role": "system", "content": self.system_prompt}] + self.memory.get_messages()
        response = self.client.send(history)
        # print(response)
        self.memory.create_message(response['choices'][0]["message"]["content"], "assistant")
        return response


class LMStudioClient():
    def __init__(self, model="qwen3-8b", base_url = "http://localhost:1234/v1/chat/completions", think=False):
        self.base_url = base_url
        self.model = model

    def send(self, history):
        response = requests.post(self.base_url, json={"model": self.model, "messages": history})
        return response.json()


class Message():
    def __init__(self, content, role="user"):
        self.content = content
        if role in ["system", "user", "assistant"]:
            self.role = role
        else:
            self.role = "user"
            print("No such role exists, role set to \"user\"")


class Memory():
    messages = []
    memory = 0
    @staticmethod
    def tier1():
        Memory.memory = 6
    @staticmethod
    def tier2():
        Memory.memory = 12
    @staticmethod
    def tier3():
        Memory.memory = 18
    def create_message(self, content, role="user"):
        if len(self.messages) > self.memory + 1:
            self.messages.pop(0)
        self.messages.append(Message(content, role))
    def get_messages(self):
        return [vars(message) for message in self.messages]


class Toolbox():
    toolbox = ["get_time", "calculator", "roll_dice", "get_date"]
    def run(self, tool, input):
        if tool not in self.toolbox:
            return "No such tool exists"

        match tool:
            case "get_time":
                pass
            case "calculator":
                pass
            case "roll_dice":
                pass
            case "get_date":
                pass


def main():
    AI = Agent()
    while (True):
        a = input()
        if a == "exit":
            break
        else:
            print(AI.chat(a)['choices'][0]["message"]["content"])
            # print(AI.chat(content=a))
            pass


if __name__ == '__main__':
    main()
