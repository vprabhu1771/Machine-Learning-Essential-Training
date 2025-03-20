```python
import sys

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b


def main():
    print("Simple CLI Calculator")
    print("Available commands: add, subtract, multiply, divide, exit")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "exit":
            print("Exiting CLI Calculator. Goodbye!")
            sys.exit(0)

        if command not in ["add", "subtract", "multiply", "divide"]:
            print("Invalid command. Try again.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            operations = {
                "add": add,
                "subtract": subtract,
                "multiply": multiply,
                "divide": divide,
            }

            result = operations[command](num1, num2)
            print(f"Result: {result}")

        except ValueError:
            print("Invalid input. Please enter numeric values.")


if __name__ == "__main__":
    main()
```