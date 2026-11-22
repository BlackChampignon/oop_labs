import requests
from datetime import datetime
import random
from logger import Logger
import json
import time

class Agent():
    def __init__(self, memory_tier=1, think=False):
        name = "Gena"
        personality = "A grumpy pirate, who answers in short sentences"
        self.system_prompt = f"Your name is {name}, {personality}"
        self.system_prompt += " /think" if think else " /no_think"
        self.logger = Logger("agent")
        self.client = LMStudioClient(self.logger)
        self.memory = Memory(self.logger)
        match memory_tier:
            case 1:
                Memory.tier1()
            case 2:
                Memory.tier2()
            case 3:
                Memory.tier3()
        self.toolbox = Toolbox(self.logger)
        self.system_prompt += ("""If you need a tool, answer ONLY with a JSON object, like: { "tool": "calculator", "input": "12 * 7" }""" +
                               f"Available tools: {", ".join(self.toolbox.toolbox)}" +
                               """If you do not need a tool, answer normally (NOT JSON).""")

    def check_tool(self, answer):
        result = ""
        start = answer.find("{")
        end = answer.rfind("}")

        tool_call = None
        if start != -1 and end > start:
            try:
                tool_call = json.loads(answer[start:end + 1])
            except json.JSONDecodeError:
                tool_call = None
        if isinstance(tool_call, dict) and "tool" in tool_call:
            tool = tool_call["tool"]
            tool_input = tool_call.get("input", "")
            self.logger.trace(f"Tool call:{tool} with input {tool_input}")
            result = self.toolbox.run(tool, tool_input)
            # add "Tool calculator returned: 84" to the conversation,
            # and ask the model again
            if result:
                self.chat(f"Tool {tool} returned: {result}")
        return result


    def chat(self, content):
        self.memory.create_message(content, role="user")
        history = [{"role": "system", "content": self.system_prompt}] + self.memory.get_messages()

        self.logger.trace(f"A request is sent (messages {len(history)-1}); a message \"{content}\" is added to memory")
        start_time = time.perf_counter()
        response = self.client.send(history)
        delta_time = time.perf_counter() - start_time
        # print(response)
        if response:
            self.logger.info(f"Prompt tokens: {response["usage"]["prompt_tokens"]}, Completion tokens: {response["usage"]["completion_tokens"]}, tks: {response["usage"]["completion_tokens"] / delta_time}")
            self.memory.create_message(response['choices'][0]["message"]["content"], "assistant")

            # ADD check if tool, => self.chat(tool_response), if not => return response['choices'][0]["message"]["content"]
            result = self.check_tool(response['choices'][0]["message"]["content"])
            if not result:
                print(response['choices'][0]["message"]["content"])

            return response['choices'][0]["message"]["content"]


class LMStudioClient():
    def __init__(self, logger,  model="qwen3-8b", base_url = "http://localhost:1234/v1/chat/completions", think=False):
        self.base_url = base_url
        self.model = model
        self.logger = logger

    def send(self, history):
        try:
            response = requests.post(self.base_url, json={"model": self.model, "messages": history})
            # print(response)
            return response.json()
        except requests.exceptions.ConnectionError:
            self.logger.error("LM Studio is not running; the answer cannot be read; a tool fails")
        return ""


class Message():
    def __init__(self, content, role="user"):
        self.content = content
        if role in ["system", "user", "assistant"]:
            self.role = role
        else:
            self.role = "user"
            print("No such role exists, role set to \"user\"")


class Memory():
    def __init__(self, logger):
        self.logger = logger
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
            self.logger.warn("Memory is full and an old message is dropped")
            self.messages.pop(0)
        self.messages.append(Message(content, role))
    def get_messages(self):
        return [vars(message) for message in self.messages]


class Toolbox():
    toolbox = ["get_time", "calculator", "roll_dice", "get_date"]

    def __init__(self, logger):
        self.logger = logger

    def run(self, tool, input):
        if tool not in self.toolbox:
            self.logger.error(f"Unknown tool: {tool}")
            return "No such tool exists"
        try:
            match tool:
                case "get_time":
                    return datetime.now().strftime("%H:%M:%S")
                case "calculator":
                    return eval(input)
                case "roll_dice":
                    return random.randint(1, int(input) if input else 6)
                case "get_date":
                    return datetime.now().strftime("%Y-%m-%d")
        except Exception as e:
            self.logger.error(f"Tool {tool} failed: {e}")
            return f"Tool execution failed: {e}"


def main():
    AI = Agent()
    while (True):
        a = input()
        if a == "exit":
            break
        else:
            AI.chat(a)
            # print(AI.chat(content=a))
            pass


if __name__ == '__main__':
    main()
