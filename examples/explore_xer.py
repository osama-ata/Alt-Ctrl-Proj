#!/usr/bin/env python
"""
Example script demonstrating the use of the XER Explorer tool.

This script shows how to explore an XER file and generate a summary report
using both the functional and object-oriented approaches.
"""

import os
import sys

from xerparser.tools import XerExplorer, explore_xer_file


def main():
    """Run the XER Explorer example."""
    # Check if a file path was provided
    if len(sys.argv) < 2:
        print("Usage: python explore_xer.py <path_to_xer_file> [output_file]")
        print("Example: python explore_xer.py ../tests/fixtures/sample.xer report.txt")
        return 1

    # Get file paths
    xer_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "xer_exploration.txt"

    if not os.path.exists(xer_path):
        print(f"Error: File not found - {xer_path}")
        return 1

    print(f"Exploring XER file: {xer_path}")
    print(f"Results will be saved to: {output_file}")
    print("\n1. Using the functional approach:")

    # Method 1: Using the simple function
    result = explore_xer_file(xer_path, output_file)
    if result:
        print(f"  Successfully generated report at {output_file}")
    else:
        print("  Failed to generate report")
        return 1

    print("\n2. Using the object-oriented approach:")

    # Method 2: Using the XerExplorer class for more control
    explorer = XerExplorer(xer_path)

    # Parse the file
    print("  Parsing XER file...")
    if not explorer.parse_file():
        print("  Failed to parse XER file")
        return 1

    # Collect data from the XER file
    print("  Collecting data...")
    data = explorer.collect_data()

    # Print some statistics about the data
    print("\n  Quick summary of XER file contents:")
    for collection_name, items in data.items():
        print(f"  - {collection_name}: {len(items)} items")

    # Generate a custom report with different parameters
    custom_output = "custom_" + output_file
    print(f"\n  Generating custom report with all collections: {custom_output}")
    explorer.generate_report(custom_output, skip_large_collections=False)

    print("\nExploration complete!")
    print("Two reports have been generated:")
    print(f"1. Standard report: {output_file}")
    print(f"2. Custom report including large collections: {custom_output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
