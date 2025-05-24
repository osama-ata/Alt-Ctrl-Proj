---
applyTo: "**/*.py"
---

# Copilot Instructions: Typing for Getters and Side-effect Functions

## Context

This project requires all functions and methods to have explicit return type annotations.

Many functions are named following standard patterns, such as:

-   **Setters / Mutators / Side-effect methods**: `add`, `append`, `set_*`, `update_*`
-   **Getters**: `get_tsv`, `count`, `to_list`, `to_dict`, `as_*`, etc.

## Instructions

1. **For all public and private methods:**

    - If the function only mutates, sets, or appends data (for example, named `add`, `append`, `set_*`, or `update_*`), annotate the return type as `-> None`.
    - If the function is a getter:
        - Use `-> int` for methods named `count`, `get_count`, etc. that return a count or similar integer value.
        - Use `-> list[...]` for methods returning a list (e.g., `get_tsv`, `to_list`). If the element type is not clear, use `-> list`.
        - Use `-> dict[...]` for methods returning a dict (e.g., `to_dict`, `as_dict`). If the type is not clear, use `-> dict`.
        - Use `-> str` for methods returning string representations.
    - If a function returns nothing and only performs a side-effect, use `-> None`.

2. **Never use `Any` unless absolutely necessary. Prefer concrete types.**

3. **If the return type is unclear from the function body, leave a TODO comment:**

    ```python
    # TODO: Add correct return type annotation
    ```

4. **Do not change the function logic or arguments. Only add return type annotations.**

## Examples

### Before

```python
def add(self, params):
    ...
def get_tsv(self):
    ...
def count(self):
    ...
def set_status(self, value):
    ...
def as_dict(self):
    ...
```

After

```python
def add(self, params) -> None:
    ...
def get_tsv(self) -> list:
    ...
def count(self) -> int:
    ...
def set_status(self, value) -> None:
    ...
def as_dict(self) -> dict:
    ...

```

Apply these conventions throughout the codebase.

to verify that all the above was addressed correctly, Run:

```bash
ruff check --select=ANN .
```
