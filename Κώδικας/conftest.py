# conftest.py
import sys
import os

# Insert the project root (one level up from test/) onto PYTHONPATH
# so that `import model.payment_method` will work everywhere.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
