# Failure-Aware System (v0.1)

A minimal Python system that demonstrates how to **persist user intent safely in the presence of failures**, while allowing domain logic and external integrations to fail, retry, and recover independently.

This project is intentionally small in scope and strict in guarantees. It focuses on **correctness, durability, and observability**, not scale or UI.

---

## 📌 Problem Statement

In many applications, user actions are tightly coupled with downstream processing:

- If domain logic fails, the action is lost
- If external sync fails, state becomes inconsistent
- Retries are ad-hoc or invisible
- Failures are silent or destructive

This project explores a different approach:

> **Persist user intent first.  
> Everything else is allowed to fail.**

---

## 🎯 Core Idea

The system is built around an **append-only event log** that records every user intent before any other processing occurs.

From that single source of truth:
- Domain state is *derived*
- External synchronization is *attempted*
- Failures are *tracked, not hidden*
- Retries are *bounded and observable*

Nothing deletes or overwrites history.

---

## 🧱 System Guarantees (v0.1)

- Durable intent recording  
- Failure isolation  
- Idempotent domain projection  
- Bounded retries  
- Explicit failure states  
- Read-only observability  

---

## 🗂 Architecture Overview

### Event Log (Source of Truth)
Append-only `event_detected` table that is never deleted or destructively modified.

### Domain Projection
Derived state that may fail safely and be retried without side effects.

### External Sync
Unreliable by design, with retries driven by the event log.

---

## 🛠 Tech Stack

- Python 3.10+
- SQLite
- argparse-based CLI

---

## ▶️ Running

```bash
python app.py
```

## 🔍 Inspecting State

```bash
python cli.py --status
python cli.py --recent 5
```

---

## 🚫 Non-Goals

- UI dashboards
- Authentication
- Distributed systems
- Auto cleanup

---

## 🔖 Version

**v0.1.0** – Failure-aware core frozen.

---

## 🧠 What This Demonstrates

- Failure-aware design
- Intent-first persistence
- Safe retries
- System observability
