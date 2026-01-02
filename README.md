# Failure-Aware System  
**v0.3.0 — Failure Correlation & Pattern Detection**

A minimal failure-aware system built in Python that treats failures as first-class data and analyzes them for recurring patterns.

This release extends the system from observing individual failures to detecting systemic behavior.

---

## 📌 What v0.3 Adds

v0.3 introduces failure correlation: the ability to detect when failures are not isolated incidents, but part of a broader pattern.

The system now answers a new question:

Is this failure happening alone, or is it happening repeatedly?

---

## 🧠 Design Principles (Unchanged)

The system continues to enforce strict guarantees:

- Failures are explicit states, not exceptions  
- No silent retries or background magic  
- No auto-healing or hidden behavior  
- Read-only observability by default  
- Human reasoning is additive, not invasive  

Correlation logic does not modify core event history.

---

## ✨ Core Capabilities (v0.3)

### 1️⃣ Failure Clustering
- Groups FAILED events by event_type
- Detects bursts within a fixed time window
- Uses deterministic, rule-based logic
- No probabilistic or ML-based inference

Clusters represent patterns, not causes.

---

### 2️⃣ Derived & Recomputable Data
- Failure clusters are stored in a separate table
- Cluster data is non-authoritative
- Clusters can be safely deleted and rebuilt
- Core failure records remain untouched

---

### 3️⃣ Correlation Service
- Explicit, manually-invoked detection
- No background schedulers
- No hidden recomputation
- Predictable and inspectable behavior

---

### 4️⃣ CLI Pattern Inspection

```bash
python cli.py --clusters
```

Shows detected failure patterns without mutating system state.

---

## 🗄 Data Model (Conceptual)

event_detected  
- Immutable event history  
- Failure states, retry counts, annotations  

failure_cluster  
- Derived summaries  
- Event type  
- Time window  
- Number of correlated failures  

---

## 🔖 Version History

v0.1.0  
- Event persistence  
- Explicit failure states  

v0.2.0  
- Time-aware retry backoff  
- Health diagnostics  
- Operator annotations  

v0.3.0  
- Failure correlation  
- Pattern detection  
- CLI visibility  

---

## 🧠 Why This Matters

Most systems only answer: Did this fail?

This system now also answers: Is this failing repeatedly?

---

## 🧊 Status

v0.3.0 is frozen.
