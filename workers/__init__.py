import os
import sys
from pathlib import Path
from . import sdc_config


BASE_DIR = Path(__file__).resolve().parent
# Add to path worker path and the main project directory.
sys.path.append(str(BASE_DIR))  # Workers directory.
sys.path.append(str(BASE_DIR.parent))  # Project directory.
# Add to path the thrid party specifics
SUBMODULES_DIR = BASE_DIR.parent / os.getenv("SUBMODULES_DIR", "third_party")
# Adding SDC submodule
SDC_DIR = os.getenv("SDC_DIR", "SDC")
sys.path.append(str(SUBMODULES_DIR / SDC_DIR))

__all__ = ["sdc_config"]