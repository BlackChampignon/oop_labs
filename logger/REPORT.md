# Laboratory Report — Logger and Parentheses Validator

**Student:** Vladislav Serchiziuc, FAF-253  
**Programming language:** Python 3

## 1. Program Structure

**What is the responsibility of `Logger`?**  
`Logger` filters messages by severity, replaces format placeholders, and prints messages. It stores the four logging priorities in a dictionary.

**What is the responsibility of `ParenthesesValidator`?**  
`ParenthesesValidator`, defined in `par_validator.py`, checks whether round parentheses are balanced and correctly ordered.

**How do the two classes collaborate?**  
The validator holds a `Logger("Parentheses")` object and calls its methods to report validation events. This is composition: the validator uses a logger without inheriting from it.

## 2. Classes and Objects

**What is a class in your implementation?**  
`Logger` defines the attributes and methods used by individual logger objects.

**Give an example of an object created from a class.**
```python
first = Logger("First")
second = Logger("Second")
```

**What state does each object store?**  
Each logger stores its own `name`. Each validator stores a reference to its logger. The validation counter is local to each `is_valid()` call.

## 3. Static and Instance Members

**Which members of `Logger` are static, and why?**  
`level`, `format`, `priorities`, and `RANDOM_MESSAGES` are class attributes shared by all logger objects. They provide common configuration and formatting data.

**Which member belongs to an individual logger instance?**  
`self.name` stores the individual logger’s name.

**What happens when the logging level is changed? Does it affect every logger instance? Explain why. Include snippets.**  
Every logger uses the updated level because `log()` reads the shared `Logger.level`.

```python
first = Logger("First")
second = Logger("Second")

Logger.set_level("ERROR")
first.info("Hidden")
second.error("Visible")
```

The settings are shared, but each object keeps its own name.

## 4. Methods and Responsibilities

**What is the responsibility of the `log` method?**  
It compares numeric priorities, filters messages, substitutes placeholders, and prints the result. The optional `%r` placeholder selects a random phrase associated with the message’s severity.

**Why does `ParenthesesValidator` use a logger instead of implementing logging itself?**  
This separates the validation algorithm from message formatting and filtering.

**Identify one example of a method call between objects or classes in your program.**  
The validator calls `self.logger.trace(...)` when it finds an opening parenthesis.

## 5. Testing and Correctness

**Give one valid and one invalid input for the parentheses validator.**  
`()` is valid, while `)(` is invalid.

**Explain how the program determines whether the input is valid.**  
The counter increases for `(` and decreases for `)`. If it becomes negative, a closing parenthesis has no matching opening parenthesis. At the end, the counter must be zero (which means that all parentheses have their own pairs). Other characters are rejected.

**Describe one test that helped you find or prevent an error.**  
The `)(` test checks that equal counts alone are insufficient: the order must also be correct.

## 6. Reflection

**What was the most important OOP concept you applied in this laboratory?**  
The most important concept was the difference between class and instance attributes. Each logger has its own name, while the logging level and format are shared. This allows common settings while preserving each object’s identity.

**If you had more time, what would you improve in your design, and why?**  
To be honest, I wanted to try to do this laboratory in C++, because I use Python too much, and wanted to learn something new. So if I had more time, I would really like to recreate this laboratory in C++.
