# File: calculator.py

class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers and return the result."""
        return a + b

    def subtract(self, a, b):
        """Subtract the second number from the first and return the result."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers and return the result."""
        return a * b

    def divide(self, a, b):
        """
        Divide the first number by the second and return the result.
        Raises ValueError if attempting to divide by zero.
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

def get_number(prompt):
    """
    ask the user to enter a number and return it as a float.
    Continuously prompts until a valid number is entered.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to run the interactive calculator program."""
    calc = Calculator()
    
    # Dictionary mapping user choices to operations
    operations = {
        '1': ('Addition', calc.add),
        '2': ('Subtraction', calc.subtract),
        '3': ('Multiplication', calc.multiply),
        '4': ('Division', calc.divide)
    }

    while True:
        # Display menu
        print("\nCalculator Operations:")
        for key, (name, _) in operations.items():
            print(f"{key}. {name}")
        print("5. Exit")

        # Get user choice
        choice = input("Enter your choice (1-5): ")

        # Exit condition
        if choice == '5':
            print("Thank you for using the calculator. Goodbye!")
            break

        # Validate user choice
        if choice not in operations:
            print("Invalid choice. Please try again.")
            continue

        # Get operation details
        operation_name, operation = operations[choice]

        # Get user inputs
        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")

        # Perform calculation and handle potential errors
        try:
            result = operation(num1, num2)
            print(f"\nResult of {operation_name}: {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()