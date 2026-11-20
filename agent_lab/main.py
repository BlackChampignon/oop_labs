import requests

class LMStudioClient():
    def __init__(self, model="qwen3-8b", system_prompt="You are a pirate"):
        self.model = model
        self.system_prompt = system_prompt

    def message(self, input_message):
        response = requests.post(
            "http://localhost:1234/api/v1/chat",
            json={
                "model": self.model,
                "system_prompt": self.system_prompt,
                "input": input_message,
                "reasoning": "off"
            }
        )
        return response.json()


def main():
    AI = LMStudioClient()
    while (True):
        a = input()
        if a == "exit":
            break
        else:
            print(AI.message(a))


if __name__ == '__main__':
    main()
