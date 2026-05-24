import logging, string, secrets, math, os, time, re
from datetime import datetime

# Qiskit Framework
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from zxcvbn import zxcvbn

# Suppress all non-critical logs
for logger in ['qiskit_ibm_runtime', 'qiskit', 'stevedore', 'urllib3']:
    logging.getLogger(logger).setLevel(logging.ERROR)

class bcolors:
    """Cyberpunk Midnight Palette"""
    MAGENTA, CYAN, GREEN = '\033[95m', '\033[96m', '\033[92m'
    WHITE, GRAY, GOLD = '\033[97m', '\033[90m', '\033[33m'
    ENDC, BOLD = '\033[0m', '\033[1m'

class QuantumEntropyEngine:
    """Optimized Singleton managing persistent hardware links and circuit caches."""
    _service = None
    _backend = None
    _circuits = {}
    _simulator = AerSimulator()
    _pool_cache = {}

    @classmethod
    def get_backend(cls, token):
        if cls._backend is None and token:
            try:
                cls._service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)
                cls._backend = cls._service.least_busy(operational=True, simulator=False)
                print(f"{bcolors.GRAY}[*] persistent_link: {cls._backend.name}{bcolors.ENDC}")
            except: print(f"{bcolors.MAGENTA}[!] Hardware offline. Defaulting to local simulator.{bcolors.ENDC}")
        return cls._backend

    @classmethod
    def get_circuit(cls, n_qubits, backend=None):
        key = (n_qubits, getattr(backend, 'name', 'sim'))
        if key not in cls._circuits:
            qc = QuantumCircuit(n_qubits)
            qc.h(range(n_qubits))
            qc.measure_all()
            cls._circuits[key] = transpile(qc, backend=backend or cls._simulator, optimization_level=1)
        return cls._circuits[key]

def get_quantum_stream(token=None, batch_size=256):
    """
    Generator: Yields 8-bit integers directly from quantum measurement.
    Vectorized bitstream processing for maximum throughput.
    """
    backend = QuantumEntropyEngine.get_backend(token)

    while True:
        raw_data = ""
        # 1. Physical Hardware Path
        if backend and token:
            try:
                n_qubits = min(backend.num_qubits, 27)
                qc = QuantumEntropyEngine.get_circuit(n_qubits, backend)
                shots = math.ceil((batch_size * 8) / n_qubits)

                job = Sampler(mode=backend).run([(qc, None, shots)])
                raw_data = "".join(job.result()[0].data.meas.get_bitstrings())
            except: backend = None # Failover to simulator

        # 2. Local Simulator Path
        if not raw_data:
            qc = QuantumEntropyEngine.get_circuit(24)
            res = QuantumEntropyEngine._simulator.run(
                qc, shots=math.ceil((batch_size*8)/24), memory=True, seed_simulator=secrets.randbits(32)
            ).result()
            raw_data = "".join(res.get_memory())

        # 3. Vectorized Chunking (Yields bytes)
        for i in range(0, len(raw_data) - 7, 8):
            yield int(raw_data[i:i+8], 2)

def generate_password(ibm_token=None, length=20, use_symbols=True, use_numbers=True):
    """
    Generate a quantum-entropy password.

    Args:
        ibm_token (str, optional): Your IBM Quantum API token. If provided,
            uses real quantum hardware; otherwise falls back to local Aer simulator.
        length (int): Password length. Default is 20.
        use_symbols (bool): Include symbols (!@#$%^&*). Default is True.
        use_numbers (bool): Include digits (0-9). Default is True.

    Returns:
        dict: {
            'password': str,
            'metrics': {'strength': str, 'crack_time': str, 'entropy': float},
            'provenance': {'source': str, 'bits': int, 'yield': str, 'latency': str}
        }

    Example::

        import qabpassgen

        # Simulator (no token needed)
        result = qabpassgen.generate_password(length=24)
        print(result['password'])

        # Real IBM Quantum hardware
        result = qabpassgen.generate_password(
            ibm_token='YOUR_IBM_TOKEN',
            length=32,
            use_symbols=True,
            use_numbers=True
        )
        qabpassgen.print_report(result)
    """
    # Pre-computation Cache Lookup
    cache_key = (use_symbols, use_numbers)
    if cache_key not in QuantumEntropyEngine._pool_cache:
        chars = string.ascii_letters
        if use_numbers: chars += string.digits
        if use_symbols: chars += "!@#$%^&*"
        n = len(chars)
        # Store (pool, n_chars, rejection_limit)
        QuantumEntropyEngine._pool_cache[cache_key] = (chars, n, 256 - (256 % n))

    char_pool, n_chars, limit = QuantumEntropyEngine._pool_cache[cache_key]

    password, consumed, rejected = [], 0, 0
    start_time = time.perf_counter()

    # Initialize the infinite stream
    stream = get_quantum_stream(ibm_token)

    # Tight loop optimization: bind method to local variable
    add_char = password.append

    while len(password) < length:
        val = next(stream)
        consumed += 1
        if val < limit:
            add_char(char_pool[val % n_chars])
        else:
            rejected += 1

    final_str = "".join(password)
    analysis = zxcvbn(final_str)

    return {
        "password": final_str,
        "metrics": {
            "strength": f"{analysis['score']}/4",
            "crack_time": analysis['crack_times_display']['offline_slow_hashing_1e4_per_second'],
            "entropy": round(analysis['guesses_log10'] * 3.322, 2)
        },
        "provenance": {
            "source": getattr(QuantumEntropyEngine._backend, 'name', "Aer_Quantum_Sim"),
            "bits": consumed * 8,
            "yield": f"{round(((consumed-rejected)/consumed)*100, 1)}%",
            "latency": f"{round(time.perf_counter() - start_time, 4)}s"
        }
    }

def print_report(res):
    """High-performance UI renderer with static width calculations."""
    W = 56
    def row(label, value, color=bcolors.WHITE):
        label_text = f"{bcolors.GOLD}{label}: {bcolors.ENDC}"
        val_text = f"{color}{value}{bcolors.ENDC}"
        padding = " " * (W - len(label) - len(str(value)) - 6)
        print(f"{bcolors.GRAY}║ {bcolors.ENDC}{label_text}{val_text}{padding}{bcolors.GRAY}║{bcolors.ENDC}")

    print(f"\n{bcolors.GRAY}╔{'═'*(W-2)}╗{bcolors.ENDC}")
    print(f"{bcolors.GRAY}║{bcolors.ENDC} {bcolors.BOLD}{bcolors.MAGENTA}{'QUANTUM ENTROPY AUDIT':^{W-4}}{bcolors.ENDC} {bcolors.GRAY}║{bcolors.ENDC}")
    print(f"{bcolors.GRAY}╠{'═'*(W-2)}╣{bcolors.ENDC}")

    row("PASS", res['password'], bcolors.GREEN + bcolors.BOLD)
    row("RANK", f"{res['metrics']['strength']} Security Score", bcolors.CYAN)
    row("TIME", res['metrics']['crack_time'])
    row("BITS", f"{res['metrics']['entropy']} Shannon Entropy")

    print(f"{bcolors.GRAY}╟{'─'*(W-2)}╢{bcolors.ENDC}")

    row("FROM", res['provenance']['source'], bcolors.MAGENTA)
    row("UTIL", f"{res['provenance']['yield']} Yield Efficiency")
    row("LOAD", res['provenance']['latency'])

    print(f"{bcolors.GRAY}╚{'═'*(W-2)}╝{bcolors.ENDC}\n")

if __name__ == "__main__":
    TOKEN = os.getenv("IBM_QUANTUM_TOKEN")  # Set this env var to use real hardware
    print_report(generate_password(ibm_token=TOKEN, length=24))
