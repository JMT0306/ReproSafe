from pathlib import Path
import pytest
from reprosafe.utils.files import FileSafetyError, read_text_file, write_new_file

def test_rejects_binary_and_overwrite(tmp_path: Path):
    source = tmp_path / "x.log"; source.write_bytes(b"a\0b")
    with pytest.raises(FileSafetyError): read_text_file(source, 100)
    output = tmp_path / "out.log"; write_new_file(output, "one")
    with pytest.raises(FileSafetyError): write_new_file(output, "two")
