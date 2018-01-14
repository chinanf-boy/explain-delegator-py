import subprocess
import os

_defualt_popen = {
    'env': os.environ.copy(),
    'stdin': subprocess.PIPE,
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'shell': True,
    'universal_newlines': True,
    'bufsize': 0
}

a = subprocess.Popen('ls', **_defualt_popen)

print('pid:-'+str(a.pid))
print('----  例子 1 ---- $ls\n')
print(a.stdout.read())