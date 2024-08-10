import sys, os, subprocess, re

def check_or_install_library(name):
    # Checks if pyserial is installed
    python_manager = "pip"
    lib_name = name
    lib_location = subprocess.run([python_manager, "show", lib_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Installing missing library
    if lib_location.returncode != 0:   
        result = subprocess.run([python_manager, "install", lib_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Adding installed library to global PATH variable
    if lib_location.stdout.strip() not in sys.path:
        match = re.search(r'^Location: (.+)$', lib_location.stdout, re.MULTILINE)
        if match:
            lib_location = match.group(1)
            sys.path.append(lib_location)