# Debug/Development Tests

This directory contains **temporary tests** created during feature development and debugging.

## Purpose

- Quick experiments during development
- One-off debugging scripts
- Tests for features still in progress
- Exploratory testing code

## Lifecycle

Tests in this directory have three possible outcomes:

1. **Promoted** → Move to `tests/regression/` when feature is stable
2. **Archived** → Move to `tests/manual/` if requires human verification
3. **Deleted** → Remove when no longer needed

## Not Tracked by Git

Files in this directory are **automatically ignored** by git (see `.gitignore`).

This directory is for local development only and should not be committed to the repository.

## When to Use

Create tests here when:
- Rapidly prototyping a new feature
- Debugging a specific issue
- Experimenting with different approaches
- Need quick throwaway test code

## Clean Up

Periodically review this directory and:
- Delete obsolete tests
- Promote valuable tests to regression suite
- Keep only actively used development tests
