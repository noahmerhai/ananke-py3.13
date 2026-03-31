# Python 3.13 Compatibility Audit — ananke

**Date:** 2026-03-31 (revised — deep pass)
**Scope:** All `.py` files under `ananke/`, `setup.py`, `tox.ini`, `pyproject.toml`
**Python target:** 3.9–3.13 (latest stable)

---

## Summary of All Findings

| # | File | Line | Issue | Severity | Status |
|---|---|---|---|---|---|
| 1 | `estimation/counterfactual_mean.py` | 969 | `data.iteritems()` removed in pandas 2.0 | **CRITICAL** | ✅ Fixed |
| 2 | `estimation/counterfactual_mean.py` | 966, 298 | Caller's DataFrame mutated directly | **High** | ✅ Fixed |
| 3 | `graphs/sg.py` | 300 | `n.fixed` on a string → `AttributeError` | **High** | ✅ Fixed |
| 4 | `pyproject.toml` | deps | `autograd>=1.5` incompatible with NumPy 2.x | **High** | ✅ Fixed |
| 5 | `graphs/graph.py` et al. | 13 | Mutable default arguments (`vertices=[]`) | Medium | ✅ Fixed (prev session) |
| 6 | `setup.py` | all | Legacy packaging, no `python_requires` | Medium | ✅ Replaced with `pyproject.toml` |
| 7 | `tox.ini` | 7 | `envlist = py37` (EOL), `coverage<5` | Medium | ✅ Fixed (prev session) |
| 8 | `identification/one_line.py` | 348 | `vars` shadows builtin | Low | ✅ Fixed |
| 9 | `setup.py` | deps | `networkx` listed but never imported | Low | ✅ Documented |
| 10 | `graphs/graph.py` | — | NumPy removed aliases | **CLEAN** | — |
| 11 | `ananke/` | — | `collections.abc` issues | **CLEAN** | — |
| 12 | `ananke/` | — | `distutils` usage | **CLEAN** | — |
| 13 | `ananke/` | — | `typing` generic imports | **CLEAN** | — |

---

## Issues Found in Deep Pass (not in first audit)

### Issue 1 — `data.iteritems()` removed in pandas 2.0 ✅ FIXED

- **File:** `ananke/estimation/counterfactual_mean.py`
- **Line:** 969
- **Pattern:** `for colname, colvalues in data.iteritems():`
- **Severity:** **Critical** — `DataFrame.iteritems()` was deprecated in pandas 1.5 and **removed in pandas 2.0**. Calling it on any modern pandas installation raises `AttributeError`, crashing `compute_effect()` entirely.
- **Fix:** `data.items()` — the standard dict-style method that works in all pandas versions.

```python
# Before (crashes on pandas 2.0+)
for colname, colvalues in data.iteritems():

# After
for colname, colvalues in data.items():  # compat: py313
```

---

### Issue 2 — Caller's DataFrame mutated inside `compute_effect()` ✅ FIXED

- **File:** `ananke/estimation/counterfactual_mean.py`
- **Lines:** 966, 298
- **Pattern:** `data['ones'] = np.ones(len(data))` and `data["primal"] = primal` modify the user's DataFrame in place.
- **Severity:** High — adds undocumented columns (`ones`, `primal`) to the caller's DataFrame as a side effect. Under pandas 2.2+ Copy-on-Write (opt-in) and mandatory in pandas 3.x, this pattern may raise `ChainedAssignmentError`. Also simply unexpected API behavior.
- **Fix:** `data = data.copy()` before each mutation so internal columns stay internal.

---

### Issue 3 — `AttributeError` in `sg.py` when fixing vertices with undirected neighbors ✅ FIXED

- **File:** `ananke/graphs/sg.py`
- **Line:** 300
- **Pattern:**
  ```python
  neighbors = [n.name for n in self.vertices[v].neighbors]  # list of strings
  for n in neighbors:
      if n.fixed:  # ← n is a str; AttributeError at runtime
  ```
- **Severity:** High — `n` is a vertex name (string), not a `Vertex` object. Accessing `.fixed` on a string raises `AttributeError`. This bug is silent in the test suite only because no test exercises the undirected-edge deletion path inside `SG.fix()`.
- **Fix:** `if self.vertices[n].fixed:`

---

### Issue 4 — `autograd>=1.5` incompatible with NumPy 2.x ✅ FIXED

- **File:** `pyproject.toml` (dependency pin)
- **Pattern:** `autograd>=1.5`
- **Severity:** High — `autograd` versions below 1.7 use internal NumPy APIs (`np.complex`, `np.bool`, etc.) that were **removed in NumPy 2.0** (released mid-2024). A fresh install of ananke could resolve NumPy 2.x + autograd 1.5, causing immediate `AttributeError` on first import of `autograd.numpy`.
- **Fix:** `autograd>=1.7`  — version 1.7 was the first release to fully support NumPy 2.x.

---

## Previously Fixed Issues (Session 3)

### Mutable Default Arguments — 8 graph files ✅ Fixed
All `Graph.__init__` and subclass constructors changed from `vertices=[], di_edges=set()` to `None` defaults with inline guards.

### Packaging — `setup.py` → `pyproject.toml` ✅ Fixed
Full migration with `python_requires=">=3.9"`, version-pinned deps, dev extras, and corrected tox matrix.

---

## Remaining Observations — All Resolved ✅

### `vars` shadows builtin (`one_line.py:348`) ✅ Fixed
Renamed to `non_fixed_vars` in `OnelineAID.functional()`. Both the assignment on line 348 and the downstream reference on line 354 updated. No other scopes affected.

### `networkx` in original `setup.py` but not used in source ✅ Documented
Intentionally omitted from `pyproject.toml`. A comment has been added directly above the `dependencies` list in `pyproject.toml` explaining the omission:
```toml
# networkx intentionally omitted — not imported anywhere in ananke/ source
```

---

## Full Change Log

| Session | File | Change |
|---|---|---|
| 3 | `pyproject.toml` | New file — replaced `setup.py` |
| 3 | `tox.ini` | envlist → py39–py313, coverage updated |
| 3 | `graphs/graph.py` | Mutable defaults → `None` |
| 3 | `graphs/sg.py` | Mutable defaults → `None` |
| 3 | `graphs/admg.py` | Mutable defaults → `None` |
| 3 | `graphs/cg.py` | Mutable defaults → `None` |
| 3 | `graphs/dag.py` | Mutable defaults → `None` |
| 3 | `graphs/bg.py` | Mutable defaults → `None` |
| 3 | `graphs/ug.py` | Mutable defaults → `None` |
| 3 | `graphs/missing_admg.py` | Mutable defaults → `None` |
| 4 | `estimation/counterfactual_mean.py` | `iteritems()` → `items()` |
| 4 | `estimation/counterfactual_mean.py` | `data = data.copy()` before mutations (×2) |
| 4 | `graphs/sg.py` | `n.fixed` → `self.vertices[n].fixed` |
| 4 | `pyproject.toml` | `autograd>=1.5` → `autograd>=1.7` |
| 5 | `identification/one_line.py` | `vars` → `non_fixed_vars` (builtin shadow) |
| 5 | `pyproject.toml` | Comment documenting networkx omission |
| 5 | `docs/migration-audit.md` | Final status update — all issues resolved |

**Total files changed:** 13
**Total breaking/high-severity issues resolved:** 7
**Total issues resolved (all severities):** 9 of 9 ✅
