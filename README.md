# Failure-Aware System — Final (v0.4)

A deliberately engineered backend system that treats **failure as first-class data** rather than an exception to be hidden or auto-remediated.

This project explores how modern systems can *observe, reason about, and prioritize failures* without sacrificing correctness, explainability, or historical integrity.

---

## 🎯 Project Goal

Most systems either:
- retry blindly, or
- escalate prematurely via alerts.

This project takes a third path:

> **Failures are immutable facts. Severity is derived. Decisions remain human.**

The system records failures, retries responsibly, identifies patterns, and surfaces *evidence-based severity* — without alerts, dashboards, or automation loops.

---

## 🧱 Core Design Principles

- **Event immutability** — failures are never overwritten
- **Derived intelligence** — severity and clusters are computed, not stored as truth
- **Explainability over automation**
- **Retry awareness without panic**
- **Read-only observability via CLI**

---

## 🧩 System Architecture

```
failure-aware-system/
│
├── app.py                     # System execution entrypoint
├── cli.py                     # Read-only observability CLI
├── requirements.txt
├── README.md
│
├── db/
│   ├── failure_aware.db       # SQLite event store
│   ├── connection.py
│   ├── schema.py              # All schema & migrations
│   └── repositories/
│       ├── event_repo.py      # Event-level queries
│       ├── cluster_repo.py    # Failure clustering logic
│       └── severity_repo.py   # Severity snapshot queries
│
├── services/
│   ├── event_service.py       # Event ingestion
│   ├── retry_service.py       # Retry & backoff logic
│   ├── sync_service.py        # Domain projection
│   └── severity_service.py   # Severity derivation engine
│
├── models/
│   └── event.py
│
├── utils/
│   ├── json_utils.py
│   └── time.py
│
└── tests/
    ├── test_event_persistence.py
    ├── test_retry_logic.py
    └── test_failure_modes.py
```

---

## 🗂️ Data Model Overview

### `event_detected`
Immutable log of detected events and failures.

Key fields:
- `event_type`
- `event_payload` (raw JSON)
- `sync_status` (PENDING / FAILED / DEAD / SYNCED)
- `retry_count`
- `last_error`

### `failure_severity` (Derived)
A disposable snapshot describing **how serious failures are right now**.

Fields:
- `entity_type` (event / cluster)
- `entity_id`
- `severity` (LOW / MEDIUM / HIGH / CRITICAL)
- `reason`
- `computed_at`

This table can be wiped and recomputed at any time.

---

## 🚦 Severity Model (v0.4)

Severity is **deterministic and explainable**.

### Event-level rules
- FAILED + retries remaining → **LOW**
- FAILED + repeated retries → **MEDIUM**
- DEAD → **HIGH**

### Cluster-level rules
- Multiple failures of same type → **HIGH**
- Recurring clusters → **CRITICAL**

Severity is never manually set.

---

## 🖥️ CLI Observability

The system exposes **read-only introspection** via CLI.

### Health snapshot
```
python cli.py --health
```

Shows:
- total events
- pending / failed / dead / synced
- oldest unresolved failure
- most retried event

### Severity overview
```
python cli.py --severity
```

Example:
```
CRITICAL : 2
HIGH     : 5
MEDIUM   : 4
LOW      : 1
```

No alerts. No side effects.

---

## 🧪 Testing Philosophy

Tests focus on:
- failure persistence
- retry exhaustion
- severity derivation correctness

The system is validated by **behavior**, not UI.

---

## 🏁 Version History

### v0.1
- Event persistence
- Retry logic
- Dead-letter handling

### v0.2
- Retry backoff
- Health diagnostics
- CLI observability

### v0.3
- Failure clustering
- Pattern detection

### v0.4 (Final)
- Evidence-based severity model
- Derived severity snapshot
- Severity visibility via CLI

---

## 🛑 What This System Deliberately Does NOT Do

- No alerts
- No dashboards
- No auto-remediation
- No orchestration
- No production claims

This is a **thinking system**, not a reacting one.

---

## 🎓 What This Project Demonstrates

- Event-driven system design
- Failure-aware architecture
- Safe retries & dead-letter patterns
- Derived analytics over mutable state
- Discipline in stopping at the right time

---

## ✅ Final Note

This project is intentionally **finished at v0.4**.

Further features would reduce clarity rather than increase value.

The system stands as a complete case study in:

> *How to design systems that respect failure instead of hiding it.*
