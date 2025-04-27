#!/usr/bin/env python
"""
Example script demonstrating the use of the XER Explorer tool.

This script shows how to explore an XER file and generate a summary report
using both the functional and object-oriented approaches.
"""

import logging
import os
import sys

from xerparser_dev.tools import XerExplorer, explore_xer_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the XER Explorer example."""
    # Check if a file path was provided
    if len(sys.argv) < 2:
        logger.error("Usage: python explore_xer.py <path_to_xer_file> [output_file]")
        logger.error("Example: python explore_xer.py ../tests/fixtures/sample.xer report.txt")
        return 1

    # Get file paths
    xer_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "xer_exploration.txt"

    if not os.path.exists(xer_path):
        logger.error(f"Error: File not found - {xer_path}")
        return 1

    logger.info(f"Exploring XER file: {xer_path}")
    logger.info(f"Results will be saved to: {output_file}")
    logger.info("\n1. Using the functional approach:")

    # Method 1: Using the simple function
    result = explore_xer_file(xer_path, output_file)
    if result:
        logger.info(f"  Successfully generated report at {output_file}")
    else:
        logger.error("  Failed to generate report")
        return 1

    logger.info("\n2. Using the object-oriented approach:")

    # Method 2: Using the XerExplorer class for more control
    explorer = XerExplorer(xer_path)

    # Parse the file
    logger.info("  Parsing XER file...")
    if not explorer.parse_file():
        logger.error("  Failed to parse XER file")
        return 1

    # Collect data from the XER file
    logger.info("  Collecting data...")
    data = explorer.collect_data()

    # Print some statistics about the data
    logger.info("\n  Quick summary of XER file contents:")
    for collection_name, items in data.items():
        logger.info(f"  - {collection_name}: {len(items)} items")

    # Generate a custom report with different parameters
    custom_output = "custom_" + output_file
    logger.info(f"\n  Generating custom report with all collections: {custom_output}")
    explorer.generate_report(custom_output, skip_large_collections=False)

    logger.info("\nExploration complete!")
    logger.info("Two reports have been generated:")
    logger.info(f"1. Standard report: {output_file}")
    logger.info(f"2. Custom report including large collections: {custom_output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
