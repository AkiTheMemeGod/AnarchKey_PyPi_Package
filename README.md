# WarBorne

A simple hashing library that generates hashes based on vowel counting.

## Installation
```bash
pip install warborne
```
## Usage

```python
from warborne import WarBorne

# Create a WarBorne instance
wb = WarBorne()

# Hash a string
hash_value = wb.hash("Hello, World!")
print(hash_value)

# Hash a file
file_hash = wb.hash_file("path/to/file.txt")
print(file_hash)
```

## License MIT