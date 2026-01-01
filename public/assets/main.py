# main.py

import logging
import sys
import argparse
import pandas as pd
import os
from analytics_service import AnalyticService

def main():
    # Set up logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analytics Worker')
    parser.add_argument('--input-file', required=True, help='Input CSV file')
    parser.add_argument('--output-file', required=True, help='Output CSV file')
    args = parser.parse_args()

    # Create an instance of the analytics service
    analytic_service = AnalyticService()

    # Load input data from CSV file
    try:
        input_data = pd.read_csv(args.input_file)
    except FileNotFoundError:
        logging.error(f'Input file {args.input_file} not found')
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logging.error(f'Input file {args.input_file} is empty')
        sys.exit(1)

    # Run analytics on the input data
    try:
        output_data = analytic_service.run_analytics(input_data)
    except Exception as e:
        logging.error(f'Error running analytics: {e}')
        sys.exit(1)

    # Save output data to CSV file
    try:
        output_data.to_csv(args.output_file, index=False)
    except Exception as e:
        logging.error(f'Error saving output: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()