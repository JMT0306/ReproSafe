# Development

```bash
python -m pip install -e '.[dev]'
ruff check .
mypy reprosafe
pytest
```

Add synthetic regression cases for every detector change. Never commit a real credential. Keep subprocess access centralized and shell-free.
