"""
Contains tests for the utilities module.
"""

from unittest.mock import patch

from html_builder.utilities import (
    is_valid_class_name,
    module_exists,
    split_preserving_quotes,
)


def test_module_exists() -> None:
    """Tests the module_exists function."""

    # Test with built-in modules
    assert module_exists("sys") is True
    assert module_exists("os") is True

    # Test with non-existent modules
    assert module_exists("does_not_exist") is False

    # Test with a third-party module
    try:
        import pandas  # noqa: F401

        pandas_installed = True
    except ImportError:
        pandas_installed = False
    assert module_exists("pandas") is (True if pandas_installed else False)

    # Simulate an import error
    with patch("importlib.import_module", side_effect=ImportError):
        assert module_exists("html_builder") is False


def test_split_preserving_quotes() -> None:
    """Tests the split_preserving_quotes function."""

    # Test with only boolean attributes
    string = "required disabled itemscope"
    expected = ["required", "disabled", "itemscope"]
    assert split_preserving_quotes(string) == expected

    # Test with only non-boolean attributes
    string = "id='test' class='class1 class2' width='50'"
    expected = ["id='test'", "class='class1 class2'", "width='50'"]
    assert split_preserving_quotes(string) == expected

    # Test with boolean and non-boolean attributes
    string = "id='test' required disabled class='class1 class2' width='50' itemscope"
    expected = [
        "id='test'",
        "required",
        "disabled",
        "class='class1 class2'",
        "width='50'",
        "itemscope",
    ]
    assert split_preserving_quotes(string) == expected


def test_is_valid_class_name() -> None:
    """Tests the is_valid_class_name function."""

    # Test with valid class names
    valid_classes = [
        "class",  # Purely alphabetic, same case
        "Class",  # Purely alphabetic, mixed case
        "_class",  # Starts with an underscore
        "-class",  # Starts with a hyphen
        "-_class",  # Character following hyphen is underscore or letter
        "c",  # Too short
    ]
    for valid_class in valid_classes:
        assert is_valid_class_name(valid_class) is True

    # Test with invalid class names
    invalid_classes = [
        "1234567890",  # Purely numeric
        "$class",  # Starts with an invalid character
        "class!",  # Contains an invalid character
        "test class",  # Contains a space
        "--class",  # Character following hyphen is hyphen
        "-!class",  # Character following hyphen is invalid character
        "-",  # Starts with a hyphen but not 2 characters long
    ]
    for invalid_class in invalid_classes:
        assert is_valid_class_name(invalid_class) is False
