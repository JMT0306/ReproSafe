# Security design

ReproSafe minimizes privileges and data flow: bounded explicit file reads, no recursive traversal, no shell subprocesses, short command timeouts, no automatic network activity, and no environment dump. Reports consume sanitized text or content-free metadata.

> ReproSafe reduces accidental secret exposure but cannot guarantee detection of every possible credential or piece of sensitive data.

The boundary is the user's machine and explicitly selected inputs. Reports should be treated as potentially sensitive until reviewed. See the root [SECURITY.md](../SECURITY.md) for vulnerability reporting.
