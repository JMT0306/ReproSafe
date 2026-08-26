import pytest
from reprosafe.sanitizers.text import sanitize_text
@pytest.mark.parametrize("value", ["ghp_abcdefgh12345678", "github_pat_abcdefgh12345678", "eyJabcdefgh.abcdefgh.abcdefgh", "AKIAIOSFODNN7EXAMPLE", "xoxb-1234567890-abcdefghij", "Authorization: Bearer abc123", "token=abcdefgh", "api_key=abcdefgh", "password: hunter2"])
def test_secret_redaction(value):
    assert value not in sanitize_text(value).sanitized_text

def test_benign_words_remain():
    text = "token bucket algorithm and password policy"
    assert sanitize_text(text).sanitized_text == text
