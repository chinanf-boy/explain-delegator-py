# delegator.py


[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

版本 0.0.13

> 子进程 for Humans 2.0. by `kennethreitz`

---

explain

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

- [run](#run)

---

我们从第一个 `delegator.run` 开始

## run 

try-delegator.py

``` bash
python trydelegator.py
```
