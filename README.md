# power-calculator

Power calculator is a command-line calculator that supports arithmetic, variables, and a stored answer (`ans`).

## Basic usage

Arithmetic commands take numbers or existing variables as arguments:

```text
add 4 3
subtract 10 2
multiply 5 6
divide 20 4
```

Arithmetic is performed sequentially. For example:

```text
subtract 20 5 3
```

means:

```text
20 - 5 - 3 = 12
```

### Using `ans`

The previous answer is automatically used as the starting value for arithmetic commands.

```text
> set 10
10

> add 5
15

> multiply 2
30
```

If there is no stored answer, an arithmetic command needs at least two arguments:

```text
> add 4 3
7
```

## Setting values

`set` changes the stored answer:

```text
set 10
```

You can also create a variable using the shorthand:

```text
10 x
```

This stores `10` in `x`.

Variables can then be used in calculations:

```text
> 10 x
> 5 y
> add x y
15
```

## Assigning a calculation to a variable

An arithmetic command can end with a variable name to store its result:

```text
add 4 3 x
```

This stores `7` in `x`.

If the variable already exists, its name is treated as an argument instead:

```text
add 4 x
```

This uses the existing value of `x` and stores the result in `ans`.

## Clearing the answer

```text
clear
```

removes the current value of `ans`.

```text
> set 10
10

> clear
ans cleared
```

## Viewing variables

```text
vars
```

displays the variables currently stored in PowerCalc.

`ans` is separate from the variables list.

## Exiting

```text
exit
```

closes PowerCalc.

## Commands

| Command    | Purpose                      |
| ---------- | ---------------------------- |
| `add`      | Add values sequentially      |
| `subtract` | Subtract values sequentially |
| `multiply` | Multiply values sequentially |
| `divide`   | Divide values sequentially   |
| `set`      | Set `ans` to a value         |
| `clear`    | Clear `ans`                  |
| `vars`     | Display stored variables     |
| `exit`     | Exit PowerCalc               |

More commands and features can be added as PowerCalc develops.
