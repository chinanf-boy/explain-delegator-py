# delegator.py

[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

Version 0.0.13

> Child process for humans 2.0. By`kennethreitz`

[github source](https://github.com/kennethreitz/delegator.py)

* * *

explain

In general, for`kennethreitz`of`Function name`Is quite straightforward

* * *

## use

```py
>>> c = delegator.run('ls')
>>> print c.out
README.rst   delegator.py

>>> c = delegator.run('long-running-process', block=False)
>>> c.pid
35199
>>> c.block()
>>> c.return_code
0
```

## Please install

```fish
$ pip install delegator.py
```

✨🍰✨

* * *

## explain directory

-   [Use delegator.run](#run)

-   [The main class command](#command)

-   [out output](#out)

-   [Error output err](#错误输出)

-   [Process-id pid](#进程-id)

-   [Interaction match output expect](#交互匹配输出)

-   [Send input send](#发送输入)

-   [A variety of ways to terminate](#终止的多种方式)

-   [Pipeline process](#管道进程)

-   [Return the command array \_expand_args](#返回命令数组)

-   [Run the command array chain](#运行命令数组)

-   [Other like**repe**such as](#其他)

* * *

We are from the first one`delegator.run`Start

## run

Code 278-285

Try the example`trydelegator.py`

```bash
python trydelegator.py
```

[delegator.py - run](./delegator.py/delegator.py#L278)

```py
def run(command, block=True, binary=False, timeout=TIMEOUT, cwd=None):
    c = Command(command, timeout=timeout) # 命令类
    c.run(block=block, binary=binary, cwd=cwd) # 运行

    if block:   # True
        c.block() # 

    return c # 返回整个 类 Command
```

Then we can see that,`run`Function is control`command`Class interface

* * *

## command

### command.**init**

Code 19-29

```py
class Command(object):

    def __init__(self, cmd, timeout=TIMEOUT):
        # 父类 初始化
        super(Command, self).__init__()

        # 变量 初始化 
        self.cmd = cmd # 子进程命令
        self.timeout = timeout # 超时
        self.subprocess = None # 子进程
        self.blocking = None # 阻断
        self.was_run = False # 状态
        self.__out = None # 私有数据输出
        self.__err = None # 私有错误
```

-   `__init__`Initialize the class

-   `self`direction`command`Pointer

> here is`c = command (command, timeout = timeout)`, The main code logic

* * *

Next

>  `c.run (block = block, binary = binary, cwd = cwd)`

### command.run

Code 140-162

```py
    def run(self, block=True, binary=False, cwd=None):
        """Runs the given command, with or without
         pexpect functionality enabled."""
        self.blocking = block # 不需要交互

        # Use subprocess.
        if self.blocking:
            popen_kwargs = self._default_popen_kwargs.copy()
            popen_kwargs['universal_newlines'] = not binary
            if cwd:
                popen_kwargs['cwd'] = cwd
            s = subprocess.Popen(self._popen_args, **popen_kwargs)
        # Otherwise, use pexpect.
        else:
            pexpect_kwargs = self._default_pexpect_kwargs.copy()
            if binary:
                pexpect_kwargs['encoding'] = None
            if cwd:
                pexpect_kwargs['cwd'] = cwd
            # Enable Python subprocesses to work with expect functionality.
            pexpect_kwargs['env']['PYTHONUNBUFFERED'] = '1'
            s = PopenSpawn(self._popen_args, **pexpect_kwargs)
        self.subprocess = s
        self.was_run = True # 是否运行的状态
```

> \-

-   [`_default_popen_kwargs`subprocess.popen default popen option](#default-popen-kwargs)

* * *

-   [Copy () shallow copy](#copy)

```py
dict1 = {'Name': 'Zara', 'Age': 7};
dict2 = dict1.copy()
print "New Dictinary : %s" %  str(dict2)
# New Dictinary : {'Age': 7, 'Name': 'Zara'}
```

-   [\_default_pexpect_kwargs popenspawn The default option](#default_pexpect_kwargs)

-   [`subprocess.popen`](#subprocess-popen)

> subprocess - can execute other programs or commands in the current program;
>
> subprocess.popen - child process

-   [`from pexpect.popen_spawn import popenspawn`](#popenspawn)

> `pexpect`Is a pure python module used to start and automate subroutines

* * *

### default-popen-kwargs

Code 38-46

```py
    @property
    def _default_popen_kwargs(self):
        return {
            'env': os.environ.copy(),
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'shell': True,
            'universal_newlines': True,
            'bufsize': 0
        }
```

-   [@property](http://python.jobbole.com/80955/)

    -   Convert class methods to read-only properties

    -   Re-implement a property`setter`with`getter`method

-   `env`

> Dictionaries, keys, and values ​​are strings that define environment variables for child processes;

-   `stdin, stdout, stderr`

> If you call popen () when the corresponding parameter is subprocess.pipe, then the corresponding attribute here is a wrapped file object of the pipeline,

-   `shell: Boolean variables,`

> Clearly require the use of the shell to run the program, along with the parameter executable to specify what shell the child process is running in - if executable = none and shell = true, use / bin / sh to execute the program specified by args;

-   `universal_newline: Boolean variable,`

> When true, stdout and stderr open in universal newline mode,

-   `bufsize`

> Control the stdin, stdout, stderr and other parameters specified file buffer, and open the file open () function parameters bufsize the same meaning.

* * *

### default_pexpect_kwargs

Code 49-60

```py
    @property
    def _default_pexpect_kwargs(self):
        encoding = 'utf-8'
        if sys.platform == 'win32':
            default_encoding = locale.getdefaultlocale()[1]
            if default_encoding is not None:
                encoding = default_encoding
        return {
            'env': os.environ.copy(),
            'encoding': encoding,
            'timeout': self.timeout
        }
```

-   locale.getdefaultlocale ()[1]

> Default encoding

-   `env` 

> Dictionaries, keys, and values ​​are strings that define environment variables for child processes;

-   `encoding`

> coding

-   `timeout`

> time out

### subprocess-popen

[./trysubprocess.py](./trySubprocess.py)

`subprocees.popen`Create and return a child process and execute the specified program in this process.

```bash
python trySubprocess.py
```

### popenspawn

> Class`subprocess.popen`, Provided like`pexpect.spawn`Interface

~~[trypopenspawn example](./tryPopenSpawn.py)~~

[api--](https://pexpect.readthedocs.io/en/stable/api/popen_spawn.html)

Because I can not figure out, what can be interactive

* * *

My example is

```py
import delegator

c = delegator.run('ls')
print(c.out)
```

So, look next`out`

## out

Code 90-101

```py
    @property
    def out(self):
        """Std/out output (cached)"""
        if self.__out is not None:
            return self.__out

        if self._uses_subprocess:
            self.__out = self.std_out.read()
        else:
            self.__out = self._pexpect_out

        return self.__out
```

-   `@property`

-   `self._uses_subprocess`

Code 62-64

```py
    @property
    def _uses_subprocess(self):
        # 是否属于 `subprocess.Popen` 类
        return isinstance(self.subprocess, subprocess.Popen)
```

* * *

-   `self.std_out.read ()`

> Belong`subprocess.popen`class

Code 70-72

```py
    @property
    def std_out(self):
        return self.subprocess.stdout
```

-   `self._pexpect_out`

> Does not belong`subprocess.popen`class

Code 74-88

```py
    @property
    def _pexpect_out(self):
        if self.subprocess.encoding:
            result = ''
        else:
            result = b''
    
        if self.subprocess.before:
            result += self.subprocess.before

        if self.subprocess.after:
            result += self.subprocess.after

        result += self.subprocess.read() # 
        return result
```

> `before and after`The property will be set as the sub-application printed text.`This`before`The property will contain all the text until the expected string pattern.`This

### after

-   The string will contain the text that matches the expected pattern.

Error output

```py
    @property
    def err(self):
        """Std/err output (cached)"""
        if self.__err is not None:
            return self.__err

        if self._uses_subprocess:
            self.__err = self.std_err.read()
            return self.__err
        else:
            return self._pexpect_out
```

> err

Code 107-117

```py
    @property
    def std_err(self):
        return self.subprocess.stderr
```

* * *

### Returned error

-   Code 103-105

```py
    @property
    def pid(self):
        """The process' PID."""
        # Support for pexpect's functionality.
        if hasattr(self.subprocess, 'proc'):
            return self.subprocess.proc.pid
        # Standard subprocess method.
        return self.subprocess.pid
```

* * *

### Process-id

-   pid

Interaction match output

```py
    def expect(self, pattern, timeout=-1):
        """Waits on the given pattern to appear in std_out"""

        # 设置了阻断,抛出错误
        if self.blocking:
            raise RuntimeError('expect can only be used on non-blocking commands.')

        # pattern 匹配
        # timeout 超时
        self.subprocess.expect(pattern=pattern, timeout=timeout)
```

> expect
>
> Code 164-170

So-called, interactive match output - is the match - the output of the terminal command

    >su
    password:

According to Ɯ match the text, to make the appropriate action.`Such as bash`

* * *

### The text that needs to match is

-   password

Send input

```py
    def send(self, s, end=os.linesep, signal=False):
        """Sends the given string or signal to std_in."""
        # end 平台换行符,s 发送文本, signal 是否发送信号

        # 阻断,错误
        if self.blocking:
            raise RuntimeError('send can only be used on non-blocking commands.')


        if not signal:
            if self._uses_subprocess:
                # 父进程与子进程通话
                return self.subprocess.communicate(s + end)
            else:
                # 交互发送
                return self.subprocess.send(s + end)
        else:
            # 向子进程发送信号 signal;
            self.subprocess.send_signal(s)
```

> send

* * *

### Code 172-184

-   Have output, naturally need user input

A variety of ways to terminate

```py
    def terminate(self):
        self.subprocess.terminate()
```

> terminate

-   Code 186-187

`Terminate the child process, equal to the sigterm signal sent to the child process;`

kill

```py
    def kill(self):
        self.subprocess.kill(signal.SIGINT)
```

> import signal

-   Code 189-190

Kill the child process p, equal to send sigkill signal to the child process;

```py
    def block(self):
        """Blocks until process is complete."""
        if self._uses_subprocess:
            # consume stdout and stderr
            try:
                stdout, stderr = self.subprocess.communicate()
                self.__out = stdout
                self.__err = stderr
            except ValueError:
                pass  # Don't read from finished subprocesses.
        else:
            self.subprocess.wait()
```

> block`Code 192-203`Block the child process`wait`

* * *

### -

-   Waits for the child process to terminate, returning the returncode property

Pipeline process

```py
    def pipe(self, command, timeout=None, cwd=None):
        """Runs the current command and passes its output to the next
        given process.
        """
        if not timeout:
            timeout = self.timeout

        if not self.was_run:
            self.run(block=False, cwd=cwd)

        data = self.out

        if timeout:
            c = Command(command, timeout)
        else:
            c = Command(command)

        c.run(block=False, cwd=cwd)
        if data:
            c.send(data)
            c.subprocess.sendeof()
        c.block()
        return c
```

> pipe`Code 205-227`Mainly done`New interactive child process c = command (command)`, Send`send (data)`After local output
>
> c.subprocess.sendeof ()`Send after the end`Waiting

* * *

> New interactive child process c.block ()
>
> End

```py
import delegator

c = delegator.run('ls') # <--- 这个 run 同等级的函数
print(c.out)
```

* * *

### The above is the command command class content

-   Here is it

Return the command array

```py
def _expand_args(command):
    """Parses command strings and returns a Popen-ready list."""

    # Prepare arguments.
    if isinstance(command, STR_TYPES):
        if sys.version_info[0] == 2:
            splitter = shlex.shlex(command.encode('utf-8'))
        elif sys.version_info[0] == 3:
            splitter = shlex.shlex(command)
        else:
            splitter = shlex.shlex(command.encode('utf-8'))
        splitter.whitespace = 'Ɯ' # 换行
        splitter.whitespace_split = True # 分隔
        command = []

        while True:
            token = splitter.get_token() # 每运行一次,返回一个命令文本
            if token:
                command.append(token) # 所有的命令放入数组
            else:
                break

        command = list(map(shlex.split, command))

    return command
```

1.  \_expand_args

Code 230-254

```py
# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str, )
```

> str_types

-   Code 10-14

> [Constraint command type](http://blog.51cto.com/yaotiaochimei/1157633)

-   shlex.shlex

> [Look for examples of text outside the quotes](http://blog.csdn.net/victoriaw/article/details/54022511)

-   shlex.split

> Use a shell-like syntax to split string examples[map shlexsplit command]For each value of the array command, use shlex.split (command

-   i

> )`list`run out`map`->

### &lt;class 'map'>

-   \-> list -> \[]

Run the command array

```py
def chain(command, timeout=TIMEOUT, cwd=None):
    commands = _expand_args(command) # 获取命令数组
    data = None

    for command in commands: # 

        c = run(command, block=False, timeout=timeout, cwd=cwd)

        if data: 
            c.send(data)
            c.subprocess.sendeof()

        data = c.out

    return c
```

> chain

```py
# 进程1 运行

运行,发送 None,返回结果 out -> data,等待关闭 # 获得 --> data

#进程2 运行

运行,发送 data,返回结果 out -> 新的 data,等待关闭 # 获得 --> 新的 data

#...
```

* * *

## Code 257-271

-   **On the command array, run, send, return the result, wait for the closure,**

other

```py
    def __repr__(self):
        return '<Command {!r}>'.format(self.cmd)
```

> repr**Code 30-31**print (command) == command.

-   repr

()

```py
    @property
    def _popen_args(self):
        return self.cmd
```

> \_popen_args

-   Code 33-35

Return the command

```py
    @property
    def _uses_pexpect(self):
        return isinstance(self.subprocess, PopenSpawn)
```

> `_uses_pexpect`Code 66-68`self.subprocess`Whether belongs to

-   popenspawn

class

```py
    @property
    def return_code(self):
        # Support for pexpect's functionality.
        if self._uses_pexpect:
            return self.subprocess.exitstatus
        # Standard subprocess method.
        return self.subprocess.returncode
```

    该属性表示子进程的返回状态,returncode 可能有多重情况: 

    None ℴℴ 子进程尚未结束;
    ==0 ℴℴ 子进程正常退出;
    > 0ℴℴ 子进程异常退出,returncode对应于出错码;
    < 0ℴℴ 子进程被信号杀掉了. 

* * *

### return_code

[Code 128-134copyRookie tutorial](http://www.runoob.com/python/att-dictionary-copy.html)