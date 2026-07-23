# Testing Guide

## Commands

### Fast (TDD cycle / pre-commit)
| Purpose | Command |
|---|---|
| Targeted unit | `python -m pytest tests/unit/test_<module>.py -v` |
| Full unit | `python -m pytest tests/unit/ -v` |
| Lint | `ruff check .` |
| Typecheck | `not available` (project has no type stubs) |

### Slow (pre-merge / CI)
| Purpose | Command |
|---|---|
| Integration | `python -m pytest tests/integration/ -v` |
| E2E | `not available` |
| Build | `not available` |
| Full validation | `python -m pytest tests/ -v && ruff check .` |
| Coverage report | `python -m pytest tests/unit/ --cov=services --cov=routers --cov=database.py --cov-report=term-missing` |
| DESIGN.md lint | `not available` (no design.md yet) |

## Test Levels
| Level | Purpose | Isolation | When to run |
|---|---|---|---|
| Unit | Business logic, pure functions, isolated components | No network, no DB, no IO (all mocked) | Every TDD cycle |
| Integration | Interaction between layers (API + DB) | SQLite in memory for DB, mocks for external APIs | Pre-commit / CI |
| E2E | Full flow (UI → API → DB → response) | Real or staging environment | CI / pre-release |

## Coverage
| Item | Configuration |
|---|---|
| Tool | pytest-cov |
| Threshold | 70% (74% actual) |
| Command | `python -m pytest tests/unit/ --cov=services --cov=routers --cov=database.py --cov-report=term-missing` |
| Excluded paths | `*/__pycache__/*`, `*/tests/*` |
| Fail on below threshold | yes |

## Environment
- Required services: None (all external dependencies are mocked)
- Required environment variables: None
- Reset/cleanup: Test files under `tests/` are self-contained

## Fixtures
| Type | Location | When used |
|---|---|---|
| Unit (mock DB, mock TF model, mock client) | `tests/conftest.py` | All unit tests |
| Integration (SQLite seed data) | `tests/integration/` | Integration tests |
| Shared utilities | `tests/conftest.py` | All levels |

## External Services Strategy
| Level | Strategy |
|---|---|
| Unit | Always mock or stub |
| Integration | Project DB: SQLite in memory. Third-party APIs: mock |
| E2E | Staging or sandbox environment |

## Test Locations
- Unit: `tests/unit/`
- Integration: `tests/integration/`
- E2E: `not available`

## TDD Coordination
- The approved plan and TDD skill govern behavior changes. For pre-existing code (this project), write regression tests that capture expected behavior without modifying production code.
- Use the commands and locations in this guide while following the skill's red/green/refactor cycle.
- Record any approved TDD exception in the task plan and checklist before implementing under that exception.

## Test Quality
- Prefer deterministic fixtures.
- Avoid shared mutable state and order-dependent tests.
- Keep sensitive or production-like data out of fixtures.
- Mock external services at boundaries; prefer real code for domain logic.
- Do not assert only on mock calls when user-visible behavior can be asserted.

## Failure Handling
- Fix unexpected targeted-test failures before continuing.
- Report unrelated failures before broadening scope.
- Record skipped commands, reasons, and residual risk.
