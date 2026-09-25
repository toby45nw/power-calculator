from powerCalc import PowerCalc

# Run the calculator in the command line
def run_cli():
    # Power caculator object
    calc = PowerCalc()

    # Main run loop
    while True:
        line = input("> ")

        if line == "exit":
            break

        # Get the caculator result
        result = calc.execute(line)

        # Process error
        if result.error:
            print(result.error)
        # Result is a message
        elif result.message:
            print(result.message)
        # The result target is ans
        elif result.target == "ans":
            print(result.value)

if __name__ == "__main__":
    run_cli()