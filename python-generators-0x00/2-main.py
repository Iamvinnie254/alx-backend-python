#!/usr/bin/python3
import sys
from batch_processing import batch_processing

# Print processed users in a batch of 50
try:
    batch_processing(50)
except BrokenPipeError:
    # This handles cases when piping output through commands like `head`
    sys.stderr.close()
