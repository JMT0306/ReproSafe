import json
from reprosafe.collectors.system import collect_system
from reprosafe.reports.json_report import build_json
from reprosafe.reports.markdown import build_markdown
from reprosafe.sanitizers.text import sanitize_text

SENSITIVE = ["sk-example-super-secret-value", "ghp_example_secret", "myPassword", "very-secret-token", "john@example.com", "JohnDoe"]
TEXT = """OPENAI_API_KEY=sk-example-super-secret-value
GITHUB_TOKEN=ghp_example_secret
DATABASE_URL=postgres://admin:myPassword@localhost/db
Authorization: Bearer very-secret-token
john@example.com
C:\\Users\\JohnDoe\\project
"""
def test_full_pipeline_never_leaks():
    result = sanitize_text(TEXT, "synthetic.log")
    outputs = [result.sanitized_text, build_markdown(collect_system(), {}, [result]), build_json(collect_system(), {}, [result]), json.dumps(result.safe_metadata())]
    for secret in SENSITIVE:
        assert all(secret not in output for output in outputs)

def test_adversarial_assignments():
    text = "password = hunter2\nPASSWORD='hunter2'\npassword: hunter2\nAuthorization: Bearer abc123\nhttps://user:password@example.com/x"
    output = sanitize_text(text).sanitized_text
    assert "hunter2" not in output and "abc123" not in output and "user:password" not in output
