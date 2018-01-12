# delegator.py

[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

Version 0.0.13

> Child process for humans 2.0. By`kennethreitz`

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

Code 19-29

```py
class Command(object):

    def __init__(self, cmd, timeout=TIMEOUT):
        # 父类 初始化
        super(Command, self).__init__()
        # 变量 初始化 
        self.cmd = cmd
        self.timeout = timeout
        self.subprocess = None
        self.blocking = None
        self.was_run = False
        self.__out = None
        self.__err = None
```

-   `__init__`Initialize the class

-   `self`direction`command`Pointer