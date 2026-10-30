from logger import Logger


class ParenthesesValidator:
    def __init__(self):
        self.logger = Logger("Parentheses")

    def is_valid(self, text: str) -> bool:
        status = 0
        reason = ""

        for pos, bracket in enumerate(text):
            if bracket not in "()":
                status = -1
                reason = f"Unexpected character {bracket!r} at position {pos}"
                break

            status += 1 if bracket == "(" else -1

            if status < 0:
                reason = f"')' at position {pos} has no matching '('"
                self.logger.warn(reason)
                break

            if bracket == "(":
                self.logger.trace(f"Found '(' at position {pos}")
            else:
                self.logger.info(f"Matching pair found: ')' at position {pos}")

        if not reason and status > 0:
            reason = f"{status} opening parentheses remain unmatched"

        valid = (status == 0)
        self.logger.info(
            f"Validation result for {text}: {'valid' if valid else 'invalid'}"
        )

        if not valid:
            self.logger.error(f"Invalid input {text}: {reason}")

        return valid