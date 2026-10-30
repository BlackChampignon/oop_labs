import argparse

from logger import Logger
from par_validator import ParenthesesValidator


TEST_CASES = (
    ("()", True),
    (")((()))", False),
    ("(", False),
    ("(())((()())())", True),
)


def interactive():
    print("Parentheses validator")

    # Test case select
    for number, case in enumerate(TEST_CASES):
        print(f"{number+1}. {case[0]}")

    custom_option = len(TEST_CASES) + 1
    print(f"{custom_option}. Enter your own string")

    try:
        choice = int(input(f"Choose a test [1-{custom_option}]: "))
    except ValueError:
        print("Please enter a number.")
        return

    if choice == custom_option:
        case = input("Parentheses: ")
    elif 1 <= choice < custom_option:
        case = TEST_CASES[choice - 1][0]
    else:
        print("Invalid test choice.")
        return

    # Setting LogLevel
    levels = list(Logger.priorities)

    for number, level in enumerate(levels):
        print(f"{number+1}. {level}")

    max_level = len(levels)
    try:
        choice = int(
            input(f"Minimum log level [1-{max_level}, default 2]: ").strip() or "2"
        )
    except ValueError:
        print("Please enter a number.")
        return

    if not (1 <= choice <= max_level):
        print("Invalid log level.")
        return

    Logger.set_level(levels[choice - 1])
    # Logger format setup
    print("Placeholders: %t time, %l level, %n name, %m message, %r random text")
    template = input(f"Format [Enter to keep {Logger.format}]: ")
    if template:
        Logger.set_format(template)

    #
    result = ParenthesesValidator().is_valid(case)
    print(f"Result: {str(result)}")


def main():
    parser = argparse.ArgumentParser(
        description="Lab 1: logger and parentheses validator"
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--input",
        help="String to validate; quote it, e.g. --input '(())'",
    )
    mode.add_argument(
        "--demo",
        action="store_true",
        help="Run the four required examples",
    )

    parser.add_argument(
        "--level",
        choices=list(Logger.priorities),
        default="INFO",
    )
    parser.add_argument(
        "--format",
        default=Logger.format,
        help="Log message format",
    )

    args = parser.parse_args()

    Logger.set_level(args.level)
    Logger.set_format(args.format)

    if args.demo:
        validator = ParenthesesValidator()

        for text, expected in TEST_CASES:
            result = validator.is_valid(text)
            print(
                f"Input: {text}; "
                f"expected: {str(expected)}; "
                f"result: {str(result)}"
            )

    elif args.input is not None:
        print(f"Result: {str(ParenthesesValidator().is_valid(args.input))}")

    else:
        interactive()


if __name__ == "__main__":
    main()