from pexpect.popen_spawn import PopenSpawn
import subprocess
import sys
import locale
import os


def _default_pexpect_kwargs():
    encoding = 'utf-8'
    if sys.platform == 'win32':
        default_encoding = locale.getdefaultlocale()[1]
        if default_encoding is not None:
            encoding = default_encoding
    return {
        'env': os.environ.copy(),
        'encoding': encoding,
        'timeout': 30
    }

_defualt_popen = _default_pexpect_kwargs().copy()
_defualt_popen['env']['PYTHONUNBUFFERED'] = '1'

try:
    child = PopenSpawn('node')
    print(child.read())
except:
    print("Exception was thrown")
    print("debug information:")
    print(str(child))

# import pexpect
# child = pexpect.spawn('ftp ftp.openbsd.org')
# child.expect('Name .*: ')
# child.sendline('anonymous')
# child.expect('Password:')
# child.sendline('noah@example.com')
# child.expect('ftp> ')
# child.sendline('lcd /tmp')
# child.expect('ftp> ')
# child.sendline('cd pub/OpenBSD')
# child.expect('ftp> ')
# child.sendline('get README')
# child.expect('ftp> ')
# child.sendline('bye')