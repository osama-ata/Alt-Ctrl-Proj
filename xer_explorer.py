#!/usr/bin/env python
"""
Command-line script to run the XER Explorer.
This makes it easy to use the explorer without writing Python code.
"""

import argparse
import logging
import sys

from xerparser_dev.tools.explorer import explore_xer_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the XER explorer from the command line."""
    parser = argparse.ArgumentParser(description="Explore and summarize XER files")
    parser.add_argument("xer_file", help="Path to the XER file to explore")
    parser.add_argument(
        "-o",
        "--output",
        default="xer_exploration.txt",
        help="Path to the output file (default: xer_exploration.txt)",
    )
    parser.add_argument(
        "--include-large",
        action="store_true",
        help="Include detailed exploration of large collections",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1000,
        help="Threshold for what is considered a large collection (default: 1000)",
    )

    args = parser.parse_args()

    logger.info(f"Exploring XER file: {args.xer_file}")
    success = explore_xer_file(
        args.xer_file, args.output, not args.include_large, args.threshold
    )

    if success:
        logger.info(f"Exploration complete! Results saved to {args.output}")
        return 0
    logger.error("Exploration failed!")
    return 1


if __name__ == "__main__":
    sys.exit(main())
