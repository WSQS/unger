# Python Implementation of Unger's Parsing Method

## Input

- Grammar
- Sentence(Tokens)

### Grammar

One line defines one rule. Example:

```plain
S -> A B
A -> a
B -> b
```

First arrow sign `->` separates left side and right side of rule. Left side of rule just contains one non terminal. The symbol which first character is uppercase is non terminal. The left side of the first rule is the start symbol. An $\epsilon$ rule can be defined with empty right side.

### Sentence(Tokens)

This program using a simple tokenizer, each token is split by any whitespace character.

## Todo

- Avoid positive Substring

## Changelog

### 0.1.0

- Implement a naive Unger's method
- $\epsilon$ rule support
- Using substring stack to avoid Loop
- Avoid Negative substring recursive check
