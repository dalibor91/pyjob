import os, sys
from lib import PyTerm
from lib import JobScanner
from lib import start_jobs
from jobs import JOBS_DIR


APP_ROOT = os.getenv('APP_ROOT')

#make sure always is set
if APP_ROOT is None:
    PyTerm.error("Please export APP_ROOT!")
    sys.exit(1)


start_jobs(JOBS_DIR);
