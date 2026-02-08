from app.utils import ALPHABET, CODE_LENGTH, generate_short_code


def test_generate_short_code_length():
    code = generate_short_code()
    assert len(code) == CODE_LENGTH


def test_generate_short_code_charset():
    code = generate_short_code()
    assert all(char in ALPHABET for char in code)
