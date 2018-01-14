# delegator.py


[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

版本 0.0.13

> 子进程 for Humans 2.0. by `kennethreitz`

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

``` py
    def run(self, block=True, binary=False, cwd=None):
        """Runs the given command, with or without
         pexpect functionality enabled."""
        self.blocking = block # 需要交互吗

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

[trypopenspawn](./tryPopenSpawn.py)

[API--](https://pexpect.readthedocs.io/en/stable/api/popen_spawn.html)

``` py
python tryPopenSpawn.py
```

因为想不出，有什么可以交互的
---

### 其他

### copy

[菜鸟教程](http://www.runoob.com/python/att-dictionary-copy.html)

