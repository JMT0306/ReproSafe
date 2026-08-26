# Examples

All example credentials are synthetic.

```bash
reprosafe inspect examples/sample-python-error.log
reprosafe scan examples/sample-python-error.log --output /tmp/python.safe.log
reprosafe bundle --output /tmp/reprosafe-report --file examples/sample-python-error.log
```

`inspect` never writes. `scan --dry-run` reports categories but does not write. A bundle is deliberately refused when its destination already exists.
