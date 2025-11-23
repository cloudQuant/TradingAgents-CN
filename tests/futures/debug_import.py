import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

try:
    from app.routers import currencies
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Other error: {e}")
