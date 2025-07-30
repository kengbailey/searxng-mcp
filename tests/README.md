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

## Writing Tests

### Basic Test Structure

```python
import pytest
from unittest.mock import patch, Mock

class TestYourFeature:
    def setup_method(self):
        """Run before each test."""
        self.client = YourClient()
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = self.client.some_method()
        assert result == "expected"
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function(self):
    """Test async functions."""
    result = await async_function()
    assert result is not None
```

### Testing Exceptions

```python
def test_error_handling(self):
    """Test exception handling."""
    with pytest.raises(CustomException):
        function_that_should_fail()
```

### Mocking External Calls

```python
@patch('module.external_call')
def test_with_mock(self, mock_call):
    """Test with mocked dependencies."""
    mock_call.return_value = "mocked result"
    
    result = function_using_external_call()
    
    assert result == "expected"
    mock_call.assert_called_once()
```

## Common Assertions

```python
assert actual == expected
assert item in collection  
assert isinstance(obj, Type)
assert len(items) > 0
```

## Tips

- Keep tests simple and focused
- Mock external dependencies (network, files, etc.)
- Use descriptive test names
- Test both success and error cases