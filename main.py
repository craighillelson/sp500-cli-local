#!/usr/bin/env python3
"""
S&P 500 One-Year Return - Command Line Interface
Simple CLI to display the S&P 500's current one-year return.
"""

import sys
import argparse

def get_sp500_year_return():
    """
    Get the 1-year return for the S&P 500 from Yahoo Finance.
    
    Returns:
        dict: Contains current_price, year_ago_price, year_return, date
        None: If data fetch fails
    """
    try:
        import yfinance as yf
        
        sp500 = yf.Ticker('^GSPC')
        
        # Get current data
        current_data = sp500.history(period='1d')
        if current_data.empty:
            print("Error: Could not fetch current S&P 500 data")
            return None
        current_price = float(current_data['Close'].iloc[-1])
        
        # Get data from 1 year ago
        historical_data = sp500.history(period='1y')
        if len(historical_data) < 2:
            print("Error: Insufficient historical data")
            return None
        year_ago_price = float(historical_data['Close'].iloc[0])
        
        # Calculate return
        year_return = ((current_price - year_ago_price) / year_ago_price) * 100
        
        return {
            'current_price': current_price,
            'year_ago_price': year_ago_price,
            'year_return': year_return,
            'date': current_data.index[-1].strftime('%Y-%m-%d')
        }
    except ImportError:
        print("Error: yfinance not installed. Run: pip3 install yfinance")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def format_price(price):
    """Format price with commas and 2 decimal places."""
    return f"${price:,.2f}"


def display_return(data, colorize=True):
    """
    Display the S&P 500 return in a nice terminal format.
    
    Args:
        data (dict): Return data from get_sp500_year_return()
        colorize (bool): If True, use terminal colors for output
    """
    if data is None:
        return
    
    # ANSI color codes (work on Mac/Linux terminals)
    if colorize and sys.stdout.isatty():
        GREEN = '\033[92m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        BLUE = '\033[94m'
        YELLOW = '\033[93m'
    else:
        GREEN = RED = BOLD = RESET = BLUE = YELLOW = ''
    
    # Determine color based on return
    return_value = data['year_return']
    color = GREEN if return_value >= 0 else RED
    sign = '+' if return_value >= 0 else ''
    
    # Print header
    print(f"\n{BOLD}{'=' * 50}{RESET}")
    print(f"{BOLD}       S&P 500 ONE-YEAR RETURN{RESET}")
    print(f"{BOLD}{'=' * 50}{RESET}\n")
    
    # Print the big return number
    print(f"{BOLD}{color}  {sign}{return_value:.2f}%{RESET}")
    print()
    
    # Print details
    print(f"{BOLD}Details:{RESET}")
    print(f"  Current Price:      {format_price(data['current_price'])}")
    print(f"  Price 1 Year Ago:   {format_price(data['year_ago_price'])}")
    print(f"  As of:              {data['date']}")
    
    print(f"\n{BOLD}{'=' * 50}{RESET}\n")


def display_json(data):
    """Display data in JSON format."""
    import json
    if data:
        print(json.dumps(data, indent=2))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Display S&P 500 one-year return from Yahoo Finance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sp500_cli.py               # Display S&P 500 return
  python3 sp500_cli.py --json        # Output as JSON
  python3 sp500_cli.py --no-color    # Disable colors
        """
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output data as JSON instead of formatted text'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    args = parser.parse_args()
    
    # Fetch data from Yahoo Finance
    data = get_sp500_year_return()
    
    if data is None:
        sys.exit(1)
    
    # Display results
    if args.json:
        display_json(data)
    else:
        display_return(data, colorize=not args.no_color)


if __name__ == '__main__':
    main()
