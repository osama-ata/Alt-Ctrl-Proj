---
applyTo: "**/*.py"
---

Prompt to Fix Special Methods' Return Type Annotations

You are a code assistant working on a Python codebase that uses Ruff for linting and enforces type annotations.

Your task is to scan all Python files in the repo and add missing return type annotations to special methods (`__init__`, `__len__`, `__iter__`, etc.) according to these conventions:

All `def **init**(...)` must have `-> None`

All `def **len**(...)` must have `-> int`

All def **iter**(self) should have `-> Self` if returning self, or `-> Iterator[ClassName]` if yielding

Do not change the function logic or arguments—add only the return type annotation.

If a method already has a return type annotation, skip it.

If you are unsure about a dunder’s return type, leave a comment `# TODO: Add correct return type annotation`.

For example, transform:

```python
class Foo:
    def __init__(self, a, b):
        ...
    def __len__(self):
        ...
    def __iter__(self):
        ...
```

Into:

```python
class Foo:
    def __init__(self, a, b) -> None:
        ...
    def __len__(self) -> int:
        ...
    def __iter__(self) -> "Foo":
        ...
```

Output only the modified code. Do not explain your changes.

Apply this pattern across the repo for all such methods.

Run

```bash
ruff check --select=ANN .
```

to verify that all special methods have the correct return type annotations.
