# C/C++代码起爆器

## 依赖

Python 3.12或更高版本。

## 用途

大幅度增加C语言或C++代码的长度，但是仍然能够正常运行。

## 用法

```bash
python main.py <input_c_source_file> <output_c_source_file>
```

## 工作原理

对所有#include进行深度优先遍历，并将全部内容展开。每个文件只会被展开一次。

## 作者

白霜渡鸦_Corvus

- Github：[白霜渡鸦_Corvus](https://github.com/YourHanpi)
- B站：[白霜渡鸦_Corvus](https://space.bilibili.com/470563327)
- 知乎：[白霜渡鸦](https://www.zhihu.com/people/yun-xing-3-13)