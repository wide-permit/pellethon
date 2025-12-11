import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now run unittest
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover("test")
    runner = unittest.TextTestRunner()
    runner.run(tests)
