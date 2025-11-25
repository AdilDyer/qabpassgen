from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from zxcvbn import zxcvbn
import string
import secrets

def _get_quantum_random_bits(n):
    """
    Internal helper: Generates n random bits using Qiskit Aer Simulator,
    seeded by the OS's cryptographically secure random source.
    """
    try:
        if n <= 0:
            return ""

        qc = QuantumCircuit(n, n)
        qc.h(range(n))
        qc.measure(range(n), range(n))

        # Use a secure seed for the simulator
        secure_seed = secrets.randbits(32)

        simulator = AerSimulator(seed_simulator=secure_seed)
        result = simulator.run(qc, shots=1).result()
        counts = result.get_counts()

        raw_bits = list(counts.keys())[0]
        return raw_bits.zfill(n)

    except Exception as e:
        # Fallback to standard secure random if quantum simulation fails
        # print(f"Quantum Simulation Error: {e}") # Uncomment for debugging
        return bin(secrets.randbits(n))[2:].zfill(n)

def generate_password(length=12, include_numbers=False, include_symbols=False):
    """
    Generates a password using quantum-simulated random bits.

    Args:
        length (int): Length of the password (default 12).
        include_numbers (bool): Whether to include digits 0-9.
        include_symbols (bool): Whether to include special characters.

    Returns:
        dict: A dictionary containing the 'password', 'score' (0-4),
              and 'feedback' string.
    """

    # Build Character Set
    char_set = string.ascii_letters
    # char_set = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    if include_numbers:
        char_set += string.digits
        # char_set = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    if include_symbols:
        char_set += string.punctuation

    # Calculate required bits (8 bits per character)
    required_bits = length * 8

    # Generate bits (Securely Seeded)
    random_bits_str = _get_quantum_random_bits(required_bits)

    password = ""
    bit_index = 0

    for _ in range(length):
        # Take 8 bits for each character
        chunk = random_bits_str[bit_index : bit_index + 8]
        if chunk:
            decimal_val = int(chunk, 2)
            # Map the random value to a character in our set
            char_index = decimal_val % len(char_set)
            password += char_set[char_index]
            bit_index += 8

    # Check Password Strength using zxcvbn, a library developed at dropbox that estimates password strength against common patterns and attacks.

    analysis = zxcvbn(password)

    return {
        "password": password,
        "score": analysis['score'],
        "warning": analysis['feedback']['warning'],
        "suggestions": analysis['feedback']['suggestions']
    }
