import requests

class LMStudioClient():
    messages = []
    def __init__(self, model="qwen3-8b", system_prompt="You are a pirate", think=False):
        self.model = model
        system_prompt += " /think" if think else " /no_think"
        self.messages.append(Message(system_prompt, "system"))

    def send(self, input_message, role="user"):
        self.messages.append(Message(input_message, role))
        response = requests.post("http://localhost:1234/v1/chat/completions", json={"model": self.model, "messages": [vars(message) for message in self.messages]})
        self.messages.append(Message(response.json()['choices'][0]["message"]["content"], "assistant"))
        return response.json()


class Message():
    def __init__(self, content, role="user"):
        self.content = content
        if role in ["system", "user", "assistant"]:
            self.role = role
        else:
            self.role = "user"
            print("No such role exists, role set to \"user\"")


def main():
    AI = LMStudioClient()
    while (True):
        a = input()
        if a == "exit":
            break
        else:
            print(AI.send(a)['choices'][0]["message"]["content"])
            pass


if __name__ == '__main__':
    main()
