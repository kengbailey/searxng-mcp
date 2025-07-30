# Testing Guide

This directory contains tests for the search application using pytest.

## Running Tests

Install pytest:
```bash
pip install pytest pytest-asyncio
```

Run all tests:
```bash
pytest tests/
```

Run with verbose output:
```bash
pytest tests/ -v
```

Run a specific test file:
```bash
pytest tests/test_search.py
```

## Test Files

- `test_search.py` - Core search functionality tests
- `test_fetch.py` - Web content fetching tests  
- `test_server.py` - Server handler tests