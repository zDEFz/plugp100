# import actual context
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Vendoring: add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, '_vendor')
if os.path.exists(vendor_dir):
    for vendor_path in os.listdir(vendor_dir):
        sys.path.append(os.path.join(vendor_dir, vendor_path))

from .discover import TapoApiDiscover
from plugp100.responses.tapo_exception import TapoException, TapoError

__all__ = []

__version__ = "2.5.1"
