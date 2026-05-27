def add(a: int, b: int) -> int:
    """
    Adds two numbers together.
    first number: a
    second number: b
    """
    return a + b 

def subtract(a: int, b: int) -> int:    
    """
    Subtracts the second number from the first number.
    first number: a
    second number: b
    """
    return a - b

def multiply(a: int, b: int) -> int:
    """
    Multiplies two numbers together.
    first number: a
    second number: b
    """
    return a * b

def divide(a: int, b: int) -> int:
    """
    Divides the first number by the second number.
    first number: a
    second number: b
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
