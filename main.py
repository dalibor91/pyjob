import os, sys
from lib import PyTerm
from lib import JobScanner
from lib import print_help
from lib import run_command
from jobs import JOBS_DIR

APP_ROOT = os.getenv('APP_ROOT')

#make sure always is set
if APP_ROOT is None:
    PyTerm.error("Please export APP_ROOT!")
    sys.exit(1)

if len(sys.argv) == 1:
    print_help()
else:
    run_command(sys.argv[1], sys.argv[2:], APP_ROOT)
