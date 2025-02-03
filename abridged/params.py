# abridged/params.py

import os

# Folders
DATA_FOLDER = 'data'
TESTS_FOLDER = 'tests'

# Root path
ROOT_PATH = os.path.normpath(os.path.join(os.path.abspath(__file__), '..', '..'))

# Data path
DATA_PATH = os.path.join(ROOT_PATH, DATA_FOLDER)
DATA_TESTS_PATH = os.path.join(ROOT_PATH, DATA_FOLDER, TESTS_FOLDER)
