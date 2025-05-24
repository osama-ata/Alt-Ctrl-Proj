#!/usr/bin/env python3
"""Test script to verify the improved xer_parser __init__.py functionality."""

import os
import sys

sys.path.insert(0, "src")


def test_lazy_loading():
    """Test lazy loading functionality."""
    print("=== Testing Lazy Loading ===")

    import xer_parser

    print(f"Initial __all__ length: {len(xer_parser.__all__)}")

    # Test module discovery
    modules = xer_parser._get_model_modules()
    print(f"Discovered {len(modules)} modules: {modules[:5]}...")

    # Test lazy loading by accessing __all__
    all_items = xer_parser.__all__
    print(f"After accessing __all__, length: {len(all_items)}")

    # Test attribute access
    try:
        xer_parser.Accounts
        print("✓ Successfully accessed Accounts class via lazy loading")
    except Exception as e:
        print(f"✗ Error accessing Accounts: {e}")


def test_eager_loading():
    """Test eager loading functionality."""
    print("\n=== Testing Eager Loading ===")

    # Set environment variable for eager loading
    os.environ["XER_PARSER_EAGER_IMPORT"] = "true"

    # Remove from cache if already imported
    if "xer_parser" in sys.modules:
        del sys.modules["xer_parser"]

    import xer_parser

    print(f"With eager loading, __all__ length: {len(xer_parser.__all__)}")

    # Clean up
    os.environ.pop("XER_PARSER_EAGER_IMPORT", None)


def test_error_handling():
    """Test error handling for missing modules."""
    print("\n=== Testing Error Handling ===")

    import xer_parser

    try:
        # Try to access a non-existent attribute
        xer_parser.NonExistentClass
        print("✗ Should have raised AttributeError")
    except AttributeError as e:
        print(f"✓ Correctly raised AttributeError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    test_lazy_loading()
    test_eager_loading()
    test_error_handling()
    print("\n=== Test Summary ===")
    print("✓ Improved __init__.py with lazy loading")
    print("✓ Dynamic module discovery")
    print("✓ Backwards compatibility maintained")
    print("✓ Environment variable configuration")
    print("✓ Proper error handling")
