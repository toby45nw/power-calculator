from powerCalc import PowerCalc

def run_cli():
    calc = PowerCalc()


    while True:
        line = input("What would you like to enter? ")
        if line == "exit":
            break

        result = calc.execute(line)

        if result.error:
            print(result.error)
        elif result.message:
            print(result.message)
        elif result.target == "ans":
            print(result.value)

if __name__ == "__main__":
    run_cli()