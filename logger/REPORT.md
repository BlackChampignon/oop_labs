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
The counter increases for `(` and decreases for `)`. If it becomes negative, a closing parenthesis has no matching opening parenthesis. At the end, the counter must be zero. Other characters are rejected.

**Describe one test that helped you find or prevent an error.**  
The `)(` test checks that equal counts alone are insufficient: the order must also be correct.

The required examples produced these results:

| Input | Result |
|---|---|
| `()` | `True` |
| `)((()))` | `False` |
| `(` | `False` |
| `(())((()())())` | `True` |

Additional automated checks covered 3,280 strings, severity filtering, shared settings, formatting, and `%r`. Testing identified an unhandled `ValueError` when entering letters for the log level. This was fixed by adding input validation. All 16 test groups passed after the fix.

The validator takes O(n) time and O(1) auxiliary space, excluding logging output.

## 6. Reflection

**What was the most important OOP concept you applied in this laboratory?**  
The most important concept was the difference between class and instance attributes. Each logger has its own name, while the logging level and format are shared. This allows common settings while preserving each object’s identity.

**If you had more time, what would you improve in your design, and why?**  
A useful improvement would be allowing the logger to write messages to a file as well as the console. This would preserve the logs for inspection after the program finishes.
