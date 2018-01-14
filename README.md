# delegator.py


[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

版本 0.0.13

> 子进程 for Humans 2.0. by `kennethreitz`

[github source](https://github.com/kennethreitz/delegator.py)

---

explain

一般来说，对于 `kennethreitz` 的 `函数命名` 是相当直白的

---

## 使用

``` py
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

## 请先安装

``` fish
$ pip install delegator.py
```

✨🍰✨

---

## explain 目录

- [使用 delegator.run](#run)

- [主要类Command](#command)

- [out 输出](#out)

- [错误输出 err](#错误输出)

- [进程-id pid](#进程-id)

- [交互匹配输出 expect](#交互匹配输出)

- [发送输入 send](#发送输入)

- [终止的多种方式 ](#终止的多种方式)

- [管道进程 pipe](#管道进程)

- [返回命令数组 _expand_args](#返回命令数组)

- [运行命令数组 chain](#运行命令数组)

- [其他 像__repe__之类](#其他)

---

我们从第一个 `delegator.run` 开始

## run 

代码 278-285

尝试一下例子 `trydelegator.py`

``` bash
python trydelegator.py
```

[delegator.py -- run](./delegator.py/delegator.py#L278)

``` py
def run(command, block=True, binary=False, timeout=TIMEOUT, cwd=None):
    c = Command(command, timeout=timeout) # 命令类
    c.run(block=block, binary=binary, cwd=cwd) # 运行

    if block:   # True
        c.block() # 

    return c # 返回整个 类 Command
```

那么我们可以看出，`run` 函数就是控制 `Command` 类的接口

---

## Command

### Command.__init__

代码 19-29

``` py
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

- `__init__` 初始化 类

- `self` 指向 `Command` 的 指针

> 这里是 ` c = Command(command, timeout=timeout)` ，主要代码逻辑

---

接下来

>  `c.run(block=block, binary=binary, cwd=cwd)`

### Command.run

代码 140-162

``` py
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

> --

- [`_default_popen_kwargs` subprocess.Popen 默认 popen 选项](#default-popen-kwargs)


---

- [.copy() 浅复制](#copy)

``` py
dict1 = {'Name': 'Zara', 'Age': 7};
dict2 = dict1.copy()
print "New Dictinary : %s" %  str(dict2)
# New Dictinary : {'Age': 7, 'Name': 'Zara'}
```

-  [_default_pexpect_kwargs PopenSpawn 默认 选项](#default_pexpect_kwargs)

- [`subprocess.Popen`](#subprocess-popen)

> subprocess - 可以在当前程序中执行其他程序或命令；

> subprocess.Popen - 子进程

- [`from pexpect.popen_spawn import PopenSpawn`](#popenspawn)

> `Pexpect` 是一个用来启动子程序并对其进行自动控制的纯 Python 模块

---

### default-popen-kwargs

代码 38-46

``` py
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

- [@property](http://python.jobbole.com/80955/)

    - 将类方法转换为只读属性

    - 重新实现一个属性的 `setter`和 `getter`方法

- `env`

> 字典，键和值都是为子进程定义环境变量的字符串；

- `stdin, stdout, stderr`

> 如果调用Popen()的时候对应的参数是subprocess.PIPE，则这里对应的属性是一个包裹了这个管道的 file 对象，

- `shell：布尔型变量，`

> 明确要求使用shell运行程序，与参数 executable 一同指定子进程运行在什么 Shell 中——如果executable=None 而 shell=True，则使用 /bin/sh 来执行 args 指定的程序；

- `universal_newline：布尔型变量，`

> 为 True 时，stdout 和 stderr 以通用换行（universal newline）模式打开，

- `bufsize`

> 控制 stdin, stdout, stderr 等参数指定的文件的缓冲，和打开文件的 open()函数中的参数 bufsize 含义相同。

---

### default_pexpect_kwargs

代码 49-60

``` py
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

- locale.getdefaultlocale()[1]

> 默认编码

- `env` 

> 字典，键和值都是为子进程定义环境变量的字符串；

- `encoding`

> 编码

- `timeout`

> 超时

### subprocess-Popen

[./trySubprocess.py](./trySubprocess.py)

`subprocees.Popen` 创建并返回一个子进程，并在这个进程中执行指定的程序。

``` bash
python trySubprocess.py
```

### popenspawn

> 类 `subprocess.Popen`，提供像`pexpect.spawn`的接口

~~[trypopenspawn 例子](./tryPopenSpawn.py)~~

[API--](https://pexpect.readthedocs.io/en/stable/api/popen_spawn.html)

因为想不出，有什么可以交互的

---

我的例子是

``` py
import delegator

c = delegator.run('ls')
print(c.out)
```

所以，接下来看 `out`

## out

代码 90-101

``` py
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

- `@property`

- `self._uses_subprocess`

代码 62-64

``` py
    @property
    def _uses_subprocess(self):
        # 是否属于 `subprocess.Popen` 类
        return isinstance(self.subprocess, subprocess.Popen)
```

---

- `self.std_out.read()`

> 属于 `subprocess.Popen` 类

代码 70-72

``` py
    @property
    def std_out(self):
        return self.subprocess.stdout
```

- `self._pexpect_out`

> 不属于 `subprocess.Popen` 类

代码 74-88

``` py
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

> `before和after` 属性将被设置为子应用程序打印的文本。该`before` 属性将包含所有文本，直到预期的字符串模式。该`after `字符串将包含与预期模式匹配的文本。

### 错误输出

- err

代码 107-117

``` py
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
    
> 返回错误

代码 103-105

``` py
    @property
    def std_err(self):
        return self.subprocess.stderr
```

---

### 进程-id

- pid

``` py
    @property
    def pid(self):
        """The process' PID."""
        # Support for pexpect's functionality.
        if hasattr(self.subprocess, 'proc'):
            return self.subprocess.proc.pid
        # Standard subprocess method.
        return self.subprocess.pid
```

---

### 交互匹配输出

- expect

代码 164-170

``` py
    def expect(self, pattern, timeout=-1):
        """Waits on the given pattern to appear in std_out"""

        # 设置了阻断，抛出错误
        if self.blocking:
            raise RuntimeError('expect can only be used on non-blocking commands.')

        # pattern 匹配
        # timeout 超时
        self.subprocess.expect(pattern=pattern, timeout=timeout)

```

> 所谓的，交互匹配输出-是匹配-终端命令的输出

> 可以根据 | 匹配到的文本，做出相应操作。

如 bash
```
>su
password:
```
需要匹配的文本就是 `password`

---

### 发送输入

- send

代码 172-184

``` py
    def send(self, s, end=os.linesep, signal=False):
        """Sends the given string or signal to std_in."""
        # end 平台换行符，s 发送文本, signal 是否发送信号

        # 阻断，错误
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
            # 向子进程发送信号 signal；
            self.subprocess.send_signal(s)
```

> 有输出，自然就需要用户输入

---

### 终止的多种方式

- terminate

代码 186-187

``` py
    def terminate(self):
        self.subprocess.terminate()
```

> 　终止子进程  ，等于向子进程发送 SIGTERM 信号；

- kill

`import signal`

代码 189-190

``` py
    def kill(self):
        self.subprocess.kill(signal.SIGINT)
```

> 杀死子进程 p ，等于向子进程发送 SIGKILL 信号；

- block

代码 192-203

``` py
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

> 阻断子进程 `wait` - `等待子进程 终止，返回 returncode 属性`

---

### 管道进程

- pipe

代码 205-227

``` py
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

> 主要做了 `新建交互子进程 c = Command(command)`，发送 `send(data)` 本地输出后 `c.subprocess.sendeof()` 发送后结束

> 等待 `新建交互子进程 c.block()` 结束

---

> 以上就是 Command 命令类 的 内容

> 下面就是

``` py
import delegator

c = delegator.run('ls') # <--- 这个 run 同等级的函数
print(c.out)
```

---

### 返回命令数组

- _expand_args

代码 230-254

``` py
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
        splitter.whitespace = '|' # 换行
        splitter.whitespace_split = True # 分隔
        command = []

        while True:
            token = splitter.get_token() # 每运行一次，返回一个命令文本
            if token:
                command.append(token) # 所有的命令放入数组
            else:
                break

        command = list(map(shlex.split, command))

    return command
```

1. STR_TYPES

代码 10-14

``` py
# Include `unicode` in STR_TYPES for Python 2.X
try:
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (str, )
```

> 约束 命令类型

- shlex.shlex

> [来查找引号之外的文本部分 例子](http://blog.51cto.com/yaotiaochimei/1157633)

- shlex.split

> [使用类似shell的语法分割字符串 例子](http://blog.csdn.net/victoriaw/article/details/54022511)

- map(shlex.split, command)

> 对 数组 command 的 每个数值，使用 shlex.split(command[i])

- list 

> 用完 `map` ->`<class 'map'>` -> list -> []

### 运行命令数组

- chain

代码 257-271

``` py
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

> 对 命令 数组，运行，发送，返回结果，等待关闭，

``` py
# 进程1 运行

运行，发送 None，返回结果 out -> data，等待关闭 # 获得 --> data

#进程2 运行

运行，发送 data，返回结果 out -> 新的 data，等待关闭 # 获得 --> 新的 data

#...
```

---

## 其他

- __repr__

代码 30-31

``` py
    def __repr__(self):
        return '<Command {!r}>'.format(self.cmd)
```

> print(Command) == Command.__repr__()

- _popen_args

代码 33-35

``` py
    @property
    def _popen_args(self):
        return self.cmd
```

> 返回 命令

- _uses_pexpect

代码 66-68

``` py
    @property
    def _uses_pexpect(self):
        return isinstance(self.subprocess, PopenSpawn)

```

> `self.subprocess` 是否 属于 `PopenSpawn`类

- return_code

代码 128-134

``` py
    @property
    def return_code(self):
        # Support for pexpect's functionality.
        if self._uses_pexpect:
            return self.subprocess.exitstatus
        # Standard subprocess method.
        return self.subprocess.returncode
```

```
该属性表示子进程的返回状态，returncode 可能有多重情况：

None —— 子进程尚未结束；
==0 —— 子进程正常退出；
> 0—— 子进程异常退出，returncode对应于出错码；
< 0—— 子进程被信号杀掉了。
```

---

### copy

[菜鸟教程](http://www.runoob.com/python/att-dictionary-copy.html)

