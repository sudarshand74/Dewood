#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) >= 3:
        try:
            a = float(sys.argv[1])
            b = float(sys.argv[2])
        except ValueError:
            print("Error: inputs must be numbers")
            sys.exit(1)
    else:
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Error: inputs must be numbers")
            sys.exit(1)

    s = a + b
    p = a - b
    # Print as int if whole number, otherwise as float
    if float(s).is_integer():
        print(int(s))
        print(int(p))
    else:
        print(s)

if __name__ == "__main__":
    main()
