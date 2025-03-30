import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the main function from src.main
from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
