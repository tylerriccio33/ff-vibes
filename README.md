
# Project Overview

This project takes commentary on fantasy football players and makes them accessible in a web UI for users.

# For Agents :)

#### Testing Conventions

- Use pytest
- Don't group by class, just functions
- Fixtures should be leveraged heavily, and they all live in conftest
- xfail if something isn't implemented

#### Coding Conventions

- Run `make lint` which runs the linter and type checker for everything
- Mini-comments are smell, do a long form comment on a section if it's complicated.
- Fail fast. No `get`, `except Exception: ...` or anything like that.
- No premature optimizations, ever.