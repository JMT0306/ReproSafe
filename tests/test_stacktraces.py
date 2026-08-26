from reprosafe.scanners.stacktrace import detect_stack_traces

def test_python():
    assert "python" in detect_stack_traces('Traceback (most recent call last):\n  File "app.py", line 2\nValueError: bad')
def test_node():
    assert "node" in detect_stack_traces("TypeError: bad\n    at main (/app/index.js:3:2)\n")
