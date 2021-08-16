import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install','requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','azure-storage-file-datalake'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','azure-identity'])