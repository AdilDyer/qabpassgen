QabPassGen 🔐⚛️
===============

**Quantum-Entropy Password Generator** — powered by real IBM Quantum hardware or local Aer simulation.

`qabpassgen` generates cryptographically strong passwords using true quantum randomness. It applies **Hadamard gates** to put qubits into superposition, measures their collapse, and converts the resulting bitstream into passwords via **rejection sampling** (eliminating modulo bias). Password strength is then verified by `zxcvbn`.

📦 Installation
---------------

```bash
pip install qabpassgen
```

> **Note:** Requires Python **>=3.9**

---

🚀 Usage
--------

### Minimal — Simulator (no token needed)

```python
import qabpassgen

result = qabpassgen.generate_password()
print(result['password'])
# Example: "X7kPq2mNvLz!8Yw3A#m"
```

### With all options

```python
import qabpassgen

result = qabpassgen.generate_password(
    ibm_token="YOUR_IBM_QUANTUM_TOKEN",  # Optional: use real hardware
    length=32,
    use_symbols=True,
    use_numbers=True
)
print(result['password'])
```

### Pretty terminal report

```python
import qabpassgen

result = qabpassgen.generate_password(length=24, use_symbols=True, use_numbers=True)
qabpassgen.print_report(result)
```

```
╔══════════════════════════════════════════════════════╗
║              QUANTUM ENTROPY AUDIT                   ║
╠══════════════════════════════════════════════════════╣
║ PASS: X7#kPq@2mNvLz!8Yw3A#m                         ║
║ RANK: 4/4 Security Score                             ║
║ TIME: centuries                                      ║
║ BITS: 87.3 Shannon Entropy                           ║
╟──────────────────────────────────────────────────────╢
║ FROM: Aer_Quantum_Sim                                ║
║ UTIL: 96.1% Yield Efficiency                         ║
║ LOAD: 0.312s                                         ║
╚══════════════════════════════════════════════════════╝
```

---

📖 API Reference
----------------

### `generate_password(...) → dict`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ibm_token` | `str` | `None` | IBM Quantum API token. Uses real hardware if provided; falls back to Aer simulator if omitted or if hardware is offline. |
| `length` | `int` | `20` | Number of characters in the password. |
| `use_symbols` | `bool` | `True` | Include symbols: `!@#$%^&*` |
| `use_numbers` | `bool` | `True` | Include digits `0–9` |

**Returns** a `dict`:

```python
{
    "password": "X7#kPq@2mNvLz!8Yw3A#m",
    "metrics": {
        "strength": "4/4",          # zxcvbn score
        "crack_time": "centuries",  # estimated offline crack time
        "entropy": 87.3             # Shannon entropy in bits
    },
    "provenance": {
        "source": "Aer_Quantum_Sim",  # or real IBM device name e.g. "ibm_kyiv"
        "bits": 1920,                 # total quantum bits consumed
        "yield": "96.1%",            # rejection sampling efficiency
        "latency": "0.312s"          # total generation time
    }
}
```

### `print_report(result)`

Renders a formatted terminal report. Pass the `dict` returned by `generate_password()`.

```python
qabpassgen.print_report(result)
```

---

🧠 How It Works
---------------

1. **Quantum Circuit:** Creates a circuit with Hadamard gates on all qubits → perfect 50/50 superposition.
2. **Measurement:** Collapses qubits to classical bits → true quantum randomness.
3. **Bitstream:** Raw measurements are packed into 8-bit integers (0–255).
4. **Rejection Sampling:** Bytes outside the uniform range are discarded to eliminate modulo bias.
5. **Hardware Fallback:** If a token is given but IBM hardware is unreachable, automatically uses the local Aer simulator.
6. **Strength Check:** Result is validated with `zxcvbn`.

---

🔑 IBM Quantum Token
--------------------

To use real quantum hardware, get a free token at [quantum.ibm.com](https://quantum.ibm.com) and pass it as `ibm_token`. Without a token, the local Aer simulator is used automatically.

You can also set it via environment variable:

```bash
export IBM_QUANTUM_TOKEN="your_token_here"
```

```python
import os, qabpassgen
result = qabpassgen.generate_password(ibm_token=os.getenv("IBM_QUANTUM_TOKEN"))
```

---

🛡️ Dependencies
----------------

- `qiskit` — quantum circuit definition
- `qiskit-aer` — local quantum simulator
- `qiskit-ibm-runtime` — real IBM Quantum hardware access
- `zxcvbn` — password strength estimation

📄 License
----------

MIT License — see [LICENSE](LICENSE) for details.
