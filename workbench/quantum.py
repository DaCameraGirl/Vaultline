from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class QuantumSeedResult:
    synthesis_seed: str
    source: str
    backend: str
    job_id: str | None
    bits_sampled: int
    created_at: str
    metadata: dict[str, Any]


def _api_key() -> str | None:
    return os.environ.get("IBM_QUANTUM_API_KEY") or os.environ.get("QISKIT_IBM_TOKEN")


def quantum_status() -> dict[str, Any]:
    key = _api_key()
    installed = _qiskit_installed()
    return {
        "configured": bool(key),
        "qiskit_installed": installed,
        "ready": bool(key) and installed,
        "usage": "Quantum-backed synthesis_seed for synthetic_audio_v1 compliance",
        "env_vars": ["IBM_QUANTUM_API_KEY", "QISKIT_IBM_TOKEN"],
    }


def _qiskit_installed() -> bool:
    try:
        import qiskit  # noqa: F401
        import qiskit_ibm_runtime  # noqa: F401

        return True
    except ImportError:
        return False


def generate_quantum_seed(*, prefer_hardware: bool = False) -> QuantumSeedResult:
    """Run a small quantum randomness circuit and derive a synthesis_seed."""
    key = _api_key()
    if not key:
        raise RuntimeError(
            "IBM Quantum API key not set. Run: powershell -File setup/quantum-key.ps1"
        )
    if not _qiskit_installed():
        raise RuntimeError(
            "Qiskit not installed. Run: pip install -r requirements-quantum.txt"
        )

    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    service = QiskitRuntimeService(token=key)
    if prefer_hardware:
        backend = service.least_busy(operational=True, simulator=False)
        source = "ibm_quantum_hardware"
    else:
        try:
            backend = service.least_busy(operational=True, simulator=True)
            source = "ibm_quantum_simulator"
        except Exception:
            backend = service.least_busy(operational=True, simulator=False)
            source = "ibm_quantum_hardware"

    num_qubits = 16
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))

    sampler = Sampler(backend)
    job = sampler.run([qc], shots=1)
    result = job.result()
    measured, counts = _extract_measurement(result)
    digest = hashlib.sha256(measured.encode()).hexdigest()[:16]
    synthesis_seed = f"ibmq_{digest}"
    job_id = getattr(job, "job_id", None) or getattr(job, "job_id()", None)

    return QuantumSeedResult(
        synthesis_seed=synthesis_seed,
        source=source,
        backend=backend.name,
        job_id=str(job_id) if job_id else None,
        bits_sampled=num_qubits,
        created_at=datetime.now(timezone.utc).isoformat(),
        metadata={
            "measurement": measured,
            "counts": counts,
        },
    )


def _extract_measurement(result: Any) -> tuple[str, dict[str, int]]:
    pub = result[0]
    data = pub.data
    for field in ("c", "meas"):
        if hasattr(data, field):
            register = getattr(data, field)
            if hasattr(register, "get_counts"):
                counts = register.get_counts()
                if counts:
                    return next(iter(counts.keys())), dict(counts)
            if hasattr(register, "get_bitstrings"):
                bits = register.get_bitstrings()
                if len(bits):
                    value = bits[0]
                    if isinstance(value, bytes):
                        measured = "".join(str(b) for b in value)
                    else:
                        measured = str(value)
                    return measured, {measured: 1}
    raise RuntimeError("Could not parse quantum measurement from job result")


def attach_seed_to_asset(catalog, asset_id: str, seed: QuantumSeedResult) -> None:
    asset = catalog.get_asset(asset_id)
    if not asset:
        raise KeyError(f"Unknown asset: {asset_id}")

    asset.compliance["synthesis_seed"] = seed.synthesis_seed
    asset.metadata["quantum"] = {
        "source": seed.source,
        "backend": seed.backend,
        "job_id": seed.job_id,
        "bits_sampled": seed.bits_sampled,
        "created_at": seed.created_at,
    }
    catalog.upsert_asset(asset)
    catalog.record_provenance(
        asset_id=asset.asset_id,
        event_type="quantum_seed",
        tool="ibm_quantum",
        details={
            "synthesis_seed": seed.synthesis_seed,
            "backend": seed.backend,
            "job_id": seed.job_id,
        },
    )