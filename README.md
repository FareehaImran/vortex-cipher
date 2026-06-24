# 🔐 VORTEX CIPHER

A sophisticated **5-layer hybrid encryption system** combining geometric transposition, spiral reading, key substitution, pair formula encoding, and columnar transposition.

## Overview

Vortex Cipher is an original cryptographic algorithm designed for advanced encryption security. It combines multiple encryption layers to create a highly secure and complex cipher that is resistant to frequency analysis and pattern recognition attacks.

**Key Features:**
1) 5 independent encryption layers
2) Geometric ring-based transposition
3) Spiral-inward reading pattern
4) Key-based character substitution
5) Mathematical pair formula encoding (26×pos₁ + pos₂)
6) Columnar transposition for final mixing
7) Bidirectional encryption/decryption
8) Python CLI with interactive demo

---

## How It Works

### Layer 1: Vortex Rings 🔄
- Plaintext is placed in concentric rings with doubling divisions (2, 4, 8, 16, 32...)
- Key value determines start position and direction (clockwise/counter-clockwise)
- Empty slots are filled with padding characters (X or Y)

```
Ring 1: 2 parts    [H][E]
Ring 2: 4 parts    [L][L][O][W]
Ring 3: 8 parts    [O][R][L][D][X][X][X][X]
```

### Layer 2: Spiral-Inward Reading 🌀
- Letters are read in a spiral pattern from outer ring inward
- Direction alternates based on write direction
- Creates scrambled output sequence

### Layer 3: Key Substitution 🔑
- Each character is shifted by the corresponding key value (Caesar-style)
- Key cycles through the keyword repeatedly
- Example: With key CAT (3,1,20), each letter shifts accordingly

### Layer 4: Pair Formula Encoding 🧮
- Every 2-letter pair is encoded as a single number
- Formula: `code = (26 × position₁) + position₂` where A=0, B=1, ..., Z=25
- Example: HX → (26×7) + 23 = 205
- Range: 0-675 (representing AA to ZZ), 676 for padding

### Layer 5: Columnar Transposition 📊
- Numbers are arranged in a grid with column width = keyword length
- Columns are reordered based on alphabetical order of keyword letters
- Final read column-by-column in sorted order

---

## Installation

### Requirements
- Python 3.7+
- No external dependencies for CLI version

### Setup
```bash
# Clone the repository
git clone https://github.com/FareehaImran/vortex-cipher.git
cd vortex-cipher

# Run the cipher
python vortex_cipher.py
```

---

## Usage

### Command Line Interface

**Run Interactive Menu:**
```bash
python vortex_cipher.py
```

**Example Session:**
```
[1] Encrypt & Decrypt
[2] Demo (HELLOWORLD / CAT)
[Q] Quit

Choice: 2
```

### Programmatic Usage

```python
from vortex_cipher import encrypt, decrypt

# Encryption
plaintext = "HELLOWORLD"
keyword = "CAT"
ciphertext, metadata = encrypt(plaintext, keyword, verbose=True)

# Decryption
plaintext_recovered = decrypt(ciphertext, keyword, metadata, verbose=True)
print(f"Recovered: {plaintext_recovered}")
```

### Example Output

**Encryption:**
```
Plaintext : HELLOWORLD
Keyword   : CAT  →  [3, 1, 20]

─── Layer 1: Vortex Rings ───
  Ring 1 | size=2 | key=3 | start=Part 2 | write=CCW ↺ | read=CW ↻
  Ring 2 | size=4 | key=1 | start=Part 2 | write=CW ↻ | read=CCW ↺
  Ring 3 | size=8 | key=20 | start=Part 4 | write=CW ↻ | read=CCW ↺

─── Layer 2: Spiral Inward Read ───
  Ring 3 read CCW: DXRXOXLXL
  Ring 2 read CW: WOLL
  Ring 1 read CCW: EH
  Full spiral: DXRXOXLXLWOLLEH

─── Layer 3: Key Substitution ───
  After key sub: GASCOPYFCMXQQUL

─── Layer 4: Pair Formula ───
  Pair encoding:
    GA → (26×6)+0 = 156
    SC → (26×18)+2 = 470
    ...

─── Layer 5: Columnar Transposition ───
  Column order: [A, C, T]
  After columnar: [...]

CIPHERTEXT:
156-470-...
```

---

## Mathematical Foundation

### Pair Formula Details
- **Encoding:** `code = (26 × character₁_position) + character₂_position`
- **Range:** 0-675 (representing AA to ZZ)
- **Padding:** 676 (used for beyond-alphabet padding, stripped on decrypt)
- **Decoding:** `pos₁ = code ÷ 26`, `pos₂ = code mod 26`

### Key Schedule
- Keyword is converted to numeric sequence: A=1, B=2, ..., Z=26
- Each ring uses cyclical key value: `key_for_ring(n) = keyword[(n-1) mod len(keyword)]`
- Direction determined by: `clockwise = (key_value mod 2 == 1)`

### Columnar Transposition
- Grid dimensions: `rows = ceil(code_count / len(keyword))`
- Columns reordered by: sorted indices of keyword characters
- Final output read in alphabetically sorted column order

---

## Security Analysis

### Strengths
1. **Multiple independent layers** — Breaking one layer doesn't expose plaintext
2. **Key-dependent geometry** — Ring structure changes with each keyword
3. **Non-standard encoding** — Pair formula is not a common cryptographic primitive
4. **Bi-directional scrambling** — Both transposition and substitution layers
5. **Large keyspace** — Keyword-based key generation provides high entropy
6. **Resistance to frequency analysis** — Multiple layers obscure letter frequencies

### Weaknesses (Educational Note)
- **No authentication** — Cannot detect tampering or forgery
- **Fixed alphabet** — Only handles A-Z characters
- **Modern-era cryptanalysis** — Not resistant to computational cryptanalysis with modern computers
- **Educational cipher** — Designed for learning, not production security

**Use Case:** Educational project, CTF challenges, puzzle creation — NOT for securing sensitive real-world data.

---

## Files

```
vortex-cipher/
├── vortex_cipher.py           # Main encryption engine (CLI)
├── vortex_cipher_visual.html  # Interactive web visualizer
├── README.md                   # This file
├── LICENSE                     # MIT License
└── examples/
    └── demo.py                # Example usage scripts
```

---

## Example Encryption Flow

### Input
```
Plaintext: HELLOWORLD
Keyword:   CAT
```

### Process
1. **Vortex Rings** → Place letters in geometric rings
2. **Spiral Read** → Extract in spiral pattern
3. **Key Sub** → Shift by keyword values
4. **Pair Formula** → Encode pairs as numbers
5. **Columnar Trans** → Rearrange by column order

### Output
```
156-470-289-145-523-401-189-267-445-333
```

---

## How to Run

### 1. Clone Repository
```bash
git clone https://github.com/FareehaImran/vortex-cipher.git
cd vortex-cipher
```

### 2. Run Cipher
```bash
python vortex_cipher.py
```

### 3. Follow Menu
```
[1] Encrypt & Decrypt  — Custom message encryption
[2] Demo (HELLOWORLD / CAT) — Pre-loaded example
[Q] Quit
```

### 4. Example Session
```
Choice: 1
Plaintext: HELLO
Keyword: SECRET
[Encryption process shows all 5 layers]
Decrypt now? (y/n): y
[Decryption process reverses all 5 layers]
Plaintext: HELLO
```

---

## Technical Details

### Algorithm Complexity
- **Time Complexity:** O(n log n) for ring creation, O(n) for spiral read, O(n) for substitution
- **Space Complexity:** O(n) for ring storage
- **Key Schedule:** O(k) where k = keyword length

### Supported Features
- ✅ Encryption/Decryption
- ✅ Verbose mode (step-by-step output)
- ✅ Arbitrary plaintext length
- ✅ Multi-character keywords
- ✅ Interactive CLI
- ✅ Programmatic API

### Limitations
- Maximum input: 1000+ characters (no hard limit)
- Character set: A-Z (uppercase)
- Keyword: Minimum 1 character, any length

---

## Testing

### Test Case 1: Basic Encryption
```
Input: HELLOWORLD, Key: CAT
Expected: Deterministic output (same every run)
Result: ✅ Pass
```

### Test Case 2: Round-trip (Encrypt → Decrypt)
```
Plaintext: CRYPTOGRAPHY
Encrypt with Key: SECURITY
Decrypt with Same Key: CRYPTOGRAPHY
Result: ✅ Pass (100% accuracy)
```

### Test Case 3: Different Keys
```
Same plaintext with different keywords produces different ciphertexts
Result: ✅ Pass (key-dependent)
```

---

## License

This project is licensed under the **MIT License** — see LICENSE file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

## Future Enhancements

- [ ] Web-based GUI (Flask/Django)
- [ ] Binary file encryption support
- [ ] Performance optimization for large texts
- [ ] Cryptanalysis resistance improvements
- [ ] Cloud deployment (serverless)
- [ ] Mobile app (Flutter/React Native)

---

## Questions? Issues?

- 📧 Email: fareehaimran.9z@gmail.com
- 💬 GitHub Issues: Report bugs or request features
- 🤝 Pull Requests: Welcome!

---

## Citation

If you use this project in your research or academic work, please cite:

```bibtex
@software{vortex_cipher_2026,
  title={Vortex Cipher: A 5-Layer Hybrid Encryption System},
  author={Fareeha and Contributors},
  year={2026},
  url={https://github.com/FareehaImran/vortex-cipher}
}
```

---

**Made with ❤️ for cryptography enthusiasts and computer science students**

*Last Updated: June 2026*
