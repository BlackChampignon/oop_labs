# Laboratory Report - Formatters, Sinks, and Track 2 - Local AI Agent

**Student: Vladislav Serchiziuc FAF-253**

**Programming language: Python**

**Track: 2** Local AI Agent

^# 1. The logger, split in three
- What is the single responsibility of Logger, Formatter, and ConsoleSink?

Logger filters messages by log level. Formatter turns a log entry into text using a template. And the ConsoleSink, which probably refers to printing the text into console, does just that
- What happens in your formatter if the message itself contains "%n"?

%n inside the message stays literal. re.sub() scans the format template once. It inserts the message at %m without scanning the inserted text again.
- Which console prints did you remove, and where do they live now?
Didn't quite remove any of them. They are still being printed based on the current Log level

^# 2. Composition and aggregation

So, the composition is when an object creates its own "insides" and is responsible for them, the aggregation is when upon the creation, the object uses a pointer to an already existing object/data/thing
- Find one more example of each in your track. Include snippets.

Aggregation example:
```python
self.logger = Logger("agent")
self.memory = Memory(self.logger)
```
here, the Agent creates his own components, such as Logger and Memory

Aggregation example:
```python
def __init__(self, logger):
    self.logger = logger
```
and here (the same code from Memory, LMStudioClient and Toolbox classes) the object stores a pointer to an already existing Logger instance

- Track 2: what would happen if two agents shared one Memory object?
Then the two agents would share the same memory. An interesting notice is that even if it is done, there won't be an issue of exceeding the size of the memory, because of the check:
```python
    def create_message(self, content, role="user"):
        if len(self.messages) > self.memory + 1:
            self.logger.warn("Memory is full and an old message is dropped")
            self.messages.pop(0)
        self.messages.append(Message(content, role))
```
this code checks whether the memory is full before storing the message. So in foresight it would still work okay, until the number of active agents exceeds the {size of memory} / 2 (has to store both the question and answer to the agent)

^# 3. Static vs shared objects
- In Lab 1 the format was static. Now it is an object that can be
shared. What did you gain? What did you lose?

In my agent, Agent, Memory, LMStudioClient, and Toolbox share one Logger. With a Formatter object, I could give each agent its own log format or let several agents share the same formatter. I lose the ability to easily change every logger’s format through a single class attribute.
- Why is the level still static? Would you change that?

So while working with just one agent, I would leave the level static. But if running with some other programs or scripts, I would have to change it - because debugging one would imply me debugging every one. It can be avoided by working in different repositories with their own logger.py-s, however this would just complicate stuff.
^# 4. Your track
- Track 2: how does the tool protocol work, step by step?
Include your measurements (tokens, tokens per second, memory tiers).
1) The Agent is initialized and everything is set up (presumably successfully)
2) The Agent sends the request in Agent.chat(), which forwards the request to client.send() which (presumably successfully) connects to the running LLM
3) The returned request is parsed with json and is sent back to the instance of an Agent
4) Here comes the tool check, which checks if there is the "tool" keyword inside and parses the json to dictionary if there is one.
5) If tool exists => Toolbox is called with run("tool name", "input").
   6) Here inside there is a match->case, which checks the tool against the existing ones and returns the tool result
7) The result of the tool is then sent back to check_tool, which calls self.chat() to send the tool response back to the agent
8) The agent uses the response and its response is printed in the last Agent.chat() call

^# 5. Reflection
- Where did you stare at an empty method the longest?
What finally unblocked you?

1) First biggest setback was splitting the LMStudioClient() functionality into Agent and Memory, because I tried building it without looking into the documentation (laboratory requirements)
2) The second one was the toolbox, which was left like:
```python
match tool:
    case "get_time":
        pass
    case "calculator":
        pass
    case "roll_dice":
        pass
    case "get_date":
        pass
```
for a very long time (a day or so). Until it finally came to me that I just have to send the tool response back to the Agent and not try to find the thing in the response and re.sub() it with the tool response
3) And the biggest one yet was configuring the check_tool(). I placed it inside Toolbox() in the beginning, but quickly understood that I don't want to bear with the consequences of checking if the tool was checked inside the Agent and calling itself (Agent.send) to send the tool response (P.S. It would just be meaningless). Hence I placed it inside the Agent class, but it was still a nightmare to configure it right, and I'm not that really satisfied with how it looks like. 

- If you had more time, what would you improve, and why?

The whole laboratory turned out quite good. There's just one thing that still bothers me - the check_tool(). It doesn't just check if the tool is called but also send the response back to LLM. Just renaming it wouldn't suffice me, if I wanted to perfect it, I would try to distinguish the check_tool and chat methods as much as possible, because therer's a infinite loop of calling the tool and sending response.

- Tables:
1) The link to the main one with the prompts and all calculations: https://docs.google.com/spreadsheets/d/1IPeizg0LwH9XtPCT6MkBA-WCVQaWeYrwqzaiW9Laof0/edit?usp=sharing
2) And a brief one:

| Memory tier | Avg. prompt tokens | Avg. completion tokens | Avg. tok/s |
|---|---:|---:|---:|
| Tier 1 | 540.11 | 88.44 | 19.04 |
| Tier 2 | 707.78 | 88.78 | 19.35 |
| Tier 3 | 767.56 | 106.33 | 21.72 |