# Fibonacci Cipher

A versatile Fibonacci-based encryption and password generation tool.

## Features

- **Five Fibonacci Algorithms**: Uses and compares performance of different Fibonacci calculation methods:
  - Naive Recursion
  - Memoized Recursion
  - Iterative
  - Matrix Exponentiation
  - Binet's Formula

- **Strong Password Generator**: Generate cryptographically strong passwords based on Fibonacci sequences

- **File Encryption/Decryption**: Encrypt and decrypt files using Fibonacci-based algorithms

- **Performance Benchmarking**: Compare the speed and memory usage of different Fibonacci algorithms

- **Multilingual Support**: Available in English and Turkish

## Requirements

- Python 3.6+
- Dependencies:
  - tabulate
  - colorama
  - pyfiglet
  - tqdm

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Fibonacci.git
cd Fibonacci

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install tabulate colorama pyfiglet tqdm
```

## Usage

Run the main program:

```bash
python fibonacci_cipher.py
```

Command-line options:

```
--benchmark      Run performance benchmark
--generate       Start password generator mode
--encrypt        Start file encryption mode
--optimal        Find optimal algorithm and generate passwords
--language, -l   Select language (en: English, tr: Turkish)
```

## How It Works

The tool uses Fibonacci sequences as the basis for encryption and password generation. The different Fibonacci calculation methods offer varying performance characteristics, allowing users to choose the best algorithm for their specific needs.

## License

MIT License 