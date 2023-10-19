![](playcode.png)

# PlayCode: A Playful Programming Language

PlayCode is procedural because knowing-how is more important than knowing-that, i.e. [street smarts](https://en.wikipedia.org/wiki/Procedural_knowledge). It will most likely be dynamically typed because no one have time for types anyway? There will be numbers, maybe strings, probably arrays, if-statements, while-loops, variables, and comments.

Currently experimenting with the following features:

- **Tags** `@<tag>` followed by some statement to define and tag `@<tag>` followed by nothing to call, so that basically every line can be called from anywhere in the program and return itself once. It's like a macro or lightweight function.

- **Swaps** `swap <a> <b>` to swap the values of two variables, which is useful for example when sorting. What else could be swapped? AST branch?

Below are examples of valid programs.

```
print 42
```

```
x = 2

if x > 0 {
    print True
} else {
    print False
}
```

```
-- swap
x = 2 * 2
y = 2

swap x y

print 1 + (x * y) - (6 / x) -> "6"
```

```
x = 0

@inc x = x + 1
@inc

print x -> "1"
```

```
-- this is a comment
```

```
-- this is an assert without output
x -> "2"
```

```
-- and this is assert with output
print x -> "2"
```

## Current status

Working to replace handwritten lexer and parser with [Lark](https://github.com/lark-parser/lark).

### Example: bubble sort

```
-- bubble sort
x = [5, 3, 8, 4, 2]
n = 5
i = 0
@init_j j = 0
while i < (n - 1) {
    @init_j
    while j < (n - 1) {
        if x[j] > x[j + 1] {
            swap x[j] x[j + 1]
        }
        j = j + 1
    }
    i = i + 1
}
x -> "[2, 3, 4, 5, 8]"
```

```
{'x': [2, 3, 4, 5, 8], 'n': 5, 'i': 4, 'j': 4}
```

