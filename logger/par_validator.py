from logger import Logger


class ParenthesesValidator:
    def __init__(self):
        self.logger = Logger("Parentheses")

    def is_valid(self, text: str):
        balance = 0
        for pos, bracket in enumerate(text):
            # break for when not bracket
            if bracket not in "()":
                balance = -1
                break

            balance += 1 if bracket == '(' else -1
            if balance < 0: break
        return balance == 0