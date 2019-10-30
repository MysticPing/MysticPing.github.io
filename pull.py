import os
import sys
import subprocess

# This script is meant to run daily before APK.py to ensure that it is up to date.

# Set working directory to script location
os.chdir(sys.path[0])
# Pulls latest version of website
subprocess.call(["git", "pull"])

