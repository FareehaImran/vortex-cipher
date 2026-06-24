"""
╔══════════════════════════════════════════╗
║         VORTEX CIPHER                    ║
║  5 Layers: Rings + Spiral Inward +       ║
║  Key Sub + Pair Formula + Columnar       ║
╚══════════════════════════════════════════╝

PAIR FORMULA (Layer 4):
  code = (26 × pos1) + pos2   where A=0, B=1 ... Z=25
  decode: pos1 = code // 26,  pos2 = code % 26
  Example: HX → (26×7)+23 = 205
  Padding: 676 (beyond max ZZ=675), stripped on decrypt

READING RULE (Layer 2):
  Written CW  → Read CCW from Part 1, outermost ring first
  Written CCW → Read CW  from Part 1, outermost ring first
"""

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def clean(text):
    return ''.join(c for c in text.upper() if c.isalpha())

def key_values(keyword):
    return [ord(c) - ord('A') + 1 for c in clean(keyword)]

def key_for_ring(kvals, ring_idx):
    return kvals[ring_idx % len(kvals)]


# ─────────────────────────────────────────
# LAYER 1 — VORTEX RINGS
# ─────────────────────────────────────────

def build_ring_sizes(length):
    sizes = []
    total = 0
    n = 1
    while total < length:
        s = 2 ** n
        sizes.append(s)
        total += s
        n += 1
    return sizes

def encrypt_rings(plaintext, kvals, verbose=False):
    sizes = build_ring_sizes(len(plaintext))
    rings = []
    letter_idx = 0

    for r, size in enumerate(sizes):
        kv = key_for_ring(kvals, r)
        clockwise = (kv % 2 == 1)
        fill_char = 'X' if clockwise else 'Y'

        start = kv % size if clockwise else (size - (kv % size)) % size

        ring_letters = []
        while letter_idx < len(plaintext) and len(ring_letters) < size:
            ring_letters.append((plaintext[letter_idx], False))
            letter_idx += 1
        while len(ring_letters) < size:
            ring_letters.append((fill_char, True))

        slots = [None] * size
        for i, item in enumerate(ring_letters):
            slot = (start + i) % size if clockwise else ((start - i) % size + size) % size
            slots[slot] = item

        rings.append({'slots': slots, 'size': size, 'kv': kv,
                      'cw': clockwise, 'fill': fill_char, 'start': start})

        if verbose:
            wd = "CW ↻" if clockwise else "CCW ↺"
            rd = "CCW ↺" if clockwise else "CW ↻"
            print(f"  Ring {r+1} | size={size} | key={kv} | start=Part {start+1} | write={wd} | read={rd}")
            row = ""
            for idx2, s in enumerate(slots):
                mark = "●" if idx2 == start else " "
                row += f"[{mark}{s[0]}{'*' if s[1] else ''}]"
            print(f"    {row}")

    return rings, sizes


# ─────────────────────────────────────────
# LAYER 2 — SPIRAL INWARD READ
# ─────────────────────────────────────────

def spiral_read(rings, verbose=False):
    output = []
    for ring in reversed(rings):  # outermost first
        size = ring['size']
        cw = ring['cw']
        slots = ring['slots']
        letters = []
        for i in range(size):
            idx = (size - i) % size if cw else i
            letters.append(slots[idx][0])
        output.extend(letters)
        if verbose:
            rd = "CCW" if cw else "CW"
            print(f"  Ring {rings.index(ring)+1} read {rd}: {''.join(letters)}")

    result = ''.join(output)
    if verbose:
        print(f"  Full spiral: {result}")
    return result

def reverse_spiral(spiral_text, rings, verbose=False):
    result = [None] * len(rings)
    idx = 0
    for r in range(len(rings) - 1, -1, -1):  # outermost first
        size = rings[r]['size']
        cw = rings[r]['cw']
        chunk = list(spiral_text[idx:idx + size])
        idx += size
        slots = ['?'] * size
        for i in range(size):
            read_idx = (size - i) % size if cw else i
            slots[read_idx] = chunk[i]
        result[r] = slots
        if verbose:
            print(f"  Ring {r+1} slots: {''.join(slots)}")
    return result


# ─────────────────────────────────────────
# LAYER 3 — KEY SUBSTITUTION
# ─────────────────────────────────────────

def key_substitution(text, kvals, verbose=False):
    result = [chr((ord(c) - 65 + kvals[i % len(kvals)]) % 26 + 65) for i, c in enumerate(text)]
    out = ''.join(result)
    if verbose:
        print(f"  After key sub: {out}")
    return out

def key_substitution_decrypt(text, kvals, verbose=False):
    result = [chr((ord(c) - 65 - kvals[i % len(kvals)] + 260) % 26 + 65) for i, c in enumerate(text)]
    out = ''.join(result)
    if verbose:
        print(f"  After reverse key sub: {out}")
    return out


# ─────────────────────────────────────────
# LAYER 4 — PAIR FORMULA
#   encode: code = (26 × pos1) + pos2   A=0..Z=25
#   decode: pos1 = code // 26, pos2 = code % 26
#   padding code = 676 (beyond ZZ=675)
# ─────────────────────────────────────────

PAD_CODE = 676

def pair_encode(pair):
    """Two letters → single number."""
    a = ord(pair[0]) - ord('A')
    b = ord(pair[1]) - ord('A')
    return 26 * a + b

def pair_decode_single(code):
    """Number → two letters."""
    a = code // 26
    b = code % 26
    return chr(a + ord('A')) + chr(b + ord('A'))

def pairs_encrypt(text, verbose=False):
    if len(text) % 2 != 0:
        text += 'X'
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    codes = [pair_encode(p) for p in pairs]
    if verbose:
        print("  Pair encoding:")
        for p, c in zip(pairs, codes):
            print(f"    {p} → (26×{ord(p[0])-65})+{ord(p[1])-65} = {c}")
    return codes

def pairs_decrypt(codes, verbose=False):
    result = ''.join(pair_decode_single(c) for c in codes if c != PAD_CODE)
    if verbose:
        print(f"  After pair decode: {result}")
    return result


# ─────────────────────────────────────────
# LAYER 5 — COLUMNAR TRANSPOSITION
# ─────────────────────────────────────────

def columnar_encrypt(codes, keyword, verbose=False):
    cols = len(keyword)
    padded = list(codes)
    while len(padded) % cols != 0:
        padded.append(PAD_CODE)
    rows_count = len(padded) // cols
    rows = [padded[i:i+cols] for i in range(0, len(padded), cols)]
    order = sorted(range(cols), key=lambda i: keyword[i])

    result = []
    for col in order:
        for row in rows:
            result.append(row[col])

    if verbose:
        print(f"  Grid ({rows_count} rows × {cols} cols):")
        header = "  " + "  ".join(f"{keyword[c]:>6}" for c in range(cols))
        print(header)
        for row in rows:
            print("  " + "  ".join(f"{x:>6}" for x in row))
        print(f"  Column order: {[keyword[i] for i in order]}")
        print(f"  After columnar: {result}")

    return result, rows_count

def columnar_decrypt(codes, keyword, rows_count, verbose=False):
    cols = len(keyword)
    order = sorted(range(cols), key=lambda i: keyword[i])
    columns = {}
    idx = 0
    for col in order:
        columns[col] = list(codes[idx:idx + rows_count])
        idx += rows_count
    result = []
    for r in range(rows_count):
        for c in range(cols):
            result.append(columns[c][r])
    if verbose:
        print(f"  After reverse columnar: {result}")
    return result


# ─────────────────────────────────────────
# SERIALIZE CIPHERTEXT
# ─────────────────────────────────────────

def codes_to_str(codes):
    return '-'.join(f"{c:03d}" for c in codes)

def str_to_codes(s):
    return [int(x) for x in s.split('-')]


# ─────────────────────────────────────────
# FULL ENCRYPT
# ─────────────────────────────────────────

def encrypt(plaintext, keyword, verbose=True):
    print("\n" + "═"*58)
    print("  ⬡  VORTEX CIPHER — ENCRYPTION")
    print("═"*58)

    pt = clean(plaintext)
    kw = clean(keyword)
    kv = key_values(kw)

    print(f"\n  Plaintext : {pt}")
    print(f"  Keyword   : {kw}  →  {kv}")

    print("\n─── Layer 1: Vortex Rings ───")
    rings, sizes = encrypt_rings(pt, kv, verbose)

    print("\n─── Layer 2: Spiral Inward Read ───")
    after_spiral = spiral_read(rings, verbose)

    print("\n─── Layer 3: Key Substitution ───")
    after_ks = key_substitution(after_spiral, kv, verbose)

    print("\n─── Layer 4: Pair Formula ───")
    codes = pairs_encrypt(after_ks, verbose)
    print(f"  Codes: {codes}")

    print("\n─── Layer 5: Columnar Transposition ───")
    final_codes, rows_count = columnar_encrypt(codes, kw, verbose)

    ciphertext = codes_to_str(final_codes)

    print("\n" + "═"*58)
    print(f"  CIPHERTEXT:\n  {ciphertext}")
    print("═"*58)

    meta = {
        'rows_count': rows_count,
        'sizes': sizes,
        'original_len': len(pt),
        'rings': rings,
    }
    return ciphertext, meta


# ─────────────────────────────────────────
# FULL DECRYPT
# ─────────────────────────────────────────

def decrypt(ciphertext, keyword, meta, verbose=True):
    print("\n" + "═"*58)
    print("  ⬡  VORTEX CIPHER — DECRYPTION")
    print("═"*58)

    kw = clean(keyword)
    kv = key_values(kw)
    rows_count = meta['rows_count']
    sizes = meta['sizes']
    original_len = meta['original_len']
    rings = meta['rings']

    print(f"\n  Ciphertext: {ciphertext[:60]}{'...' if len(ciphertext)>60 else ''}")
    print(f"  Keyword   : {kw}")

    print("\n─── Reverse Layer 5: Columnar ───")
    final_codes = str_to_codes(ciphertext)
    codes = columnar_decrypt(final_codes, kw, rows_count, verbose)
    codes = [c for c in codes if c != PAD_CODE]

    print("\n─── Reverse Layer 4: Pair Formula ───")
    after_ks = pairs_decrypt(codes, verbose)

    print("\n─── Reverse Layer 3: Key Sub ───")
    after_spiral = key_substitution_decrypt(after_ks, kv, verbose)

    print("\n─── Reverse Layer 2: Rebuild Rings ───")
    ring_data = reverse_spiral(after_spiral, rings, verbose)

    print("\n─── Reverse Layer 1: Extract Letters ───")
    out = []
    for r, (rd, ring) in enumerate(zip(ring_data, rings)):
        size = ring['size']
        cw = ring['cw']
        fill = ring['fill']
        start = ring['start']
        for i in range(size):
            slot = (start + i) % size if cw else ((start - i) % size + size) % size
            letter = rd[slot]
            if letter != fill and letter != '?':
                out.append(letter)

    result = ''.join(out[:original_len])
    print("\n" + "═"*58)
    print(f"  PLAINTEXT: {result}")
    print("═"*58)
    return result


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("""
 ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗
 ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
 ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝
 ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗
  ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗
   ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                    C I P H E R
  Pair formula: code = (26 × pos1) + pos2  [A=0..Z=25]
    """)

    while True:
        print("\n[1] Encrypt & Decrypt")
        print("[2] Demo  (HELLOWORLD / CAT)")
        print("[Q] Quit")
        choice = input("\n  Choice: ").strip().upper()

        if choice == 'Q':
            print("  Goodbye!")
            break
        elif choice == '2':
            ct, meta = encrypt("HELLOWORLD", "CAT")
            decrypt(ct, "CAT", meta)
        elif choice == '1':
            pt = input("\n  Plaintext : ").strip()
            kw = input("  Keyword   : ").strip()
            if not pt or not kw:
                print("  ✗ Need both.")
                continue
            ct, meta = encrypt(pt, kw)
            if input("\n  Decrypt now? (y/n): ").strip().lower() == 'y':
                decrypt(ct, kw, meta)
        else:
            print("  Invalid choice.")
