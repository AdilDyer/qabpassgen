QabPassGen 🔐⚛️
===============

**Quantum-Simulation Backed Password Generator**

qabpassgen is a Python library that generates strong, random passwords using quantum circuit simulation for entropy. It leverages **Qiskit Aer** to simulate quantum superposition (Hadamard gates) and measures the collapse of quantum states to generate random bits, seeded by your OS's cryptographically secure random source.

It also includes built-in password strength estimation using zxcvbn.

📦 Installation
---------------

Install easily via pip:

`pip install qabpassgen`

> **Note:** This library requires Python **\>=3.9** and **<3.13**.

🚀 Usage
--------

### Basic Generation

Generate a standard 12-character password:

`import qabpassgen  result = qabpassgen.generate_password()`

`print(f"Password: {result['password']}")  print(f"Strength Score: {result['score']}/4")  print(f"Feedback: {result['feedback']}")   `

### Customizing Complexity

You can specify length, numbers, and symbols:

To Generate a complex 16-char password with numbers and symbols :

`import qabpassgen
 complex_pass = qabpassgen.generate_password(      length=16,      include_numbers=True,      include_symbols=True  )  print(complex_pass['password']) `

Output example: "K9$mP#v2!LqR5@xZ"

🧠 How It Works
---------------

1.  **Quantum Entropy Simulation:** The library creates a Quantum Circuit with n qubits (where n is based on the requested password length).

2.  **Superposition:** It applies **Hadamard gates** to all qubits, putting them into a state of equal probability (superposition).

3.  **Measurement:** The qubits are measured, forcing them to collapse into classical bits (0 or 1).

4.  **Secure Seeding:** The simulator is seeded using Python's secrets module (OS-level cryptographically secure source) to ensure the simulation itself is unpredictable.

5.  **Mapping:** The resulting random bits are converted into characters from your chosen character set.

6.  **Validation:** The final password is analyzed by zxcvbn to ensure it meets modern strength standards.


_If quantum simulation fails (e.g., due to environment issues), the library gracefully falls back to standard cryptographically secure generation._

🛡️ Dependencies
----------------

*   qiskit: For defining quantum circuits.

*   qiskit-aer: For high-performance quantum simulation.

*   zxcvbn: For realistic password strength estimation.


📄 License
----------

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
