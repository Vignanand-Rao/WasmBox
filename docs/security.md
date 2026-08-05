These explanations are perfect for your **project documentation**, **PPT**, or **viva**.

-----

# 1. What `blocked.py` Does

### Purpose

`blocked.py` contains a list of **dangerous Python modules and functions** that are not allowed to execute in the online Python compiler.

### Why is it needed?

When users submit Python code, some modules and functions can:

* Access the operating system
* Delete or modify files
* Execute system commands
* Open network connections
* Consume excessive system resources

To prevent these risks, `blocked.py` maintains a blacklist.

### Example

Blocked modules:

```python
os
socket
subprocess
shutil
pathlib
ctypes
multiprocessing
```

Blocked functions:

```python
eval()
exec()
compile()
open()
__import__()
```

### Output Example

User code:

```python
import os
```

Output:

```
Blocked Module: os
```

---

# 2. What `validator.py` Does

### Purpose

`validator.py` is the **main security component** of the project.

It analyzes the user's Python code **before execution** and checks whether it contains any blocked modules or dangerous functions.

### How it works

1. Receives Python code from the backend.
2. Converts the code into an **Abstract Syntax Tree (AST)**.
3. Scans every import statement and function call.
4. Compares them against the blocked lists.
5. Returns:

   * **Safe** if no violations are found.
   * A list of security errors if unsafe code is detected.

### Why use AST?

Instead of executing the code, AST allows the validator to inspect the code safely.

### Example

User code:

```python
import socket
```

Validator output:

```
Blocked Module: socket
```

---

# 3. What `timeout.py` Does

### Purpose

`timeout.py` prevents Python programs from running indefinitely.

### Why is it needed?

A malicious user can submit:

```python
while True:
    pass
```

Without a timeout, the program would run forever, consuming CPU resources and making the service unavailable.

### How it works

1. Starts executing the Python program.
2. Monitors the execution time.
3. If the program exceeds the configured limit (for example, 5 seconds), it automatically terminates the process.
4. Returns:

```
Execution Timeout
```

### Benefit

This protects the server from:

* Infinite loops
* CPU exhaustion
* Resource abuse

---

# 4. What Kinds of Attacks Your Module Blocks

Your security module helps protect against several common attacks and misuse scenarios.

### 1. Operating System Access

Example:

```python
import os
os.remove("important.txt")
```

Blocked because it could delete or modify server files.

---

### 2. Command Execution

Example:

```python
import subprocess
subprocess.run("rm -rf /")
```

Blocked because it can execute operating system commands.

---

### 3. Network Access

Example:

```python
import socket
```

Blocked because users should not create network connections from the execution environment.

---

### 4. Arbitrary Code Execution

Example:

```python
eval(user_input)
```

or

```python
exec(user_code)
```

Blocked because they execute dynamically generated Python code.

---

### 5. Unauthorized File Access

Example:

```python
open("secret.txt")
```

Blocked because users should not read or write server files.

---

### 6. Infinite Loop Attack

Example:

```python
while True:
    pass
```

Blocked by the timeout mechanism.

---

### 7. Resource Exhaustion

Example:

```python
from multiprocessing import Process
```

Blocked because it can create many processes and consume excessive CPU and memory.

---

# 5. How Another Team Member Should Use Your Module

Your module is designed to sit **between the backend and the Python execution engine**.

### Integration Flow

```text
User
   │
   ▼
Frontend (Member 1)
   │
   ▼
Backend API (Member 2)
   │
   ▼
Security Module (Member 4)
   │
   ├── Validate code
   ├── Check blocked modules
   ├── Check blocked functions
   ├── Apply timeout
   │
   ▼
Python Runtime (Member 3)
   │
   ▼
Execution Result
   │
   ▼
Backend
   │
   ▼
Frontend
```
