# Failure-Aware System  
**v0.2.0 — Operable, Observable, Honest**

A minimal failure-aware system built in Python that treats failures as first-class data instead of edge cases.

This project focuses on recording, retrying, and explaining failures in a deterministic and inspectable way.

---

## 📌 What This System Is

This system captures events, attempts to synchronize them with an external system, and records everything that happens along the way:
- when an event was detected  
- whether synchronization succeeded or failed  
- how many retries were attempted  
- when the next retry is allowed  
- when an event is permanently dead  
- why an operator believes the failure occurred  

Failures are not exceptions. They are data.

---

## 🧠 Design Philosophy

This project intentionally avoids:
- silent retries  
- infinite retry loops  
- auto-healing magic  

Instead, it guarantees:
- explicit failure states  
- time-aware retries  
- human-readable diagnostics  

---

## ✨ Core Capabilities (v0.2)

- Event detection & persistence  
- Explicit failure states  
- Retry backoff with scheduling  
- Dead-letter handling  
- Human annotations  
- Read-only CLI diagnostics  

---

## 🔖 Versioning

v0.1.0: Core failure-aware pipeline  
v0.2.0: Backoff, health diagnostics, annotations  

---

## 🧠 Final Note

This system is built for clarity, not convenience.
