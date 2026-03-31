# Ananke — Python 3.13 Compatibility Migration

## Project
Python package for causal inference with graphical models.
Source: https://github.com/ghosthamlet/ananke (originally from https://gitlab.com/causal/ananke)
Target: make the package fully compatible with Python 3.9–3.13.

## Stack
- Pure Python package (no compiled extensions)
- Dependencies: numpy, autograd, scipy, pandas, statsmodels, networkx, graphviz
- Tests: pytest via tox (currently py37 only)
- Build: setup.py (legacy — migrate to pyproject.toml)

## Commands
```bash
# Run tests
pytest ananke/

# Run with coverage
pytest --cov=ananke ananke/

# Check for deprecated numpy aliases
grep -rn "np\.bool\b\|np\.int\b\|np\.float\b\|np\.complex\b\|np\.object\b\|np\.str\b" ananke/

# Check for collections.abc issues
grep -rn "from collections import" ananke/

# Check for distutils usage
grep -rn "distutils" .

# Check for pandas.DataFrame.append usage
grep -rn "\.append(" ananke/

# Install in editable mode for testing
pip install -e ".[dev]"
```

## Migration Scope

### Phase 1 — Breaking (must fix before anything else)
1. NumPy removed aliases: `np.bool`, `np.int`, `np.float`, `np.complex`, `np.object`, `np.str`
   - Replace with builtins (`bool`, `int`, `float`) or explicit types (`np.float64`, `np.int64`)
   - Files to audit: all of `ananke/`
2. `collections.Iterable` / `collections.Callable` etc. removed in Python 3.10
   - Replace with `from collections.abc import Iterable, Callable, ...`
3. `distutils` removed in Python 3.12
   - Migrate `setup.py` to `pyproject.toml`
4. `autograd` must be >= 1.7 for NumPy 2.x compatibility
   - Update version pin in requirements

### Phase 2 — Soft breaks (audit and fix)
5. `pandas.DataFrame.append()` removed in pandas 2.0
   - Replace with `pd.concat([df, new_row])` pattern
6. `statsmodels` must be >= 0.14 for Python 3.12+ wheel support
   - Update version pin
7. `networkx` 3.x changed some function signatures
   - Audit `ananke/graphs/` for networkx API usage
8. `typing` generics — update `List[x]`, `Dict[x, y]` etc. to `list[x]`, `dict[x, y]` (Python 3.9+)

### Phase 3 — Packaging and tooling
9. Replace `setup.py` with `pyproject.toml` using `[build-system]` = setuptools
10. Add `python_requires = ">=3.9"` and pin minimum dependency versions
11. Update `tox.ini` envlist to `py39,py310,py311,py312,py313`
12. Add `pyproject.toml` dev extras: pytest, pytest-cov

## Code Style
- Keep changes minimal — do not refactor logic, only fix compatibility issues
- One commit per phase
- Add a comment `# compat: py313` next to non-obvious fixes
- Do not introduce type annotations where none existed before
- Preserve all existing docstrings exactly

## Testing Strategy
- After each phase, run `pytest ananke/` and confirm zero new failures
- If a test was already broken before the migration, note it but do not fix it (out of scope)
- After Phase 3, run `tox -e py312` as the final validation target

## Do Not
- Do not change any algorithm logic or mathematical operations
- Do not bump ananke's own version number
- Do not modify test files unless a test itself uses a deprecated API
- Do not add new dependencies
