# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys
from typing import Optional


HEADER_PATTERN: re.Pattern[str] = re.compile(r"\s*#include\s+((<.+?>)|(\".+?\"))")


def _get_c_header_paths() -> list[str]:
    """
    获取C头文件所在的目录。
    :return: C头文件所在的目录。
    """
    return os.environ["CPLUS_INCLUDE_PATH"].split(";" if os.name == "nt" else ":")


_C_HEADER_PATHS = _get_c_header_paths()


class Exploder:
    """
    “代码起爆器”类。暂时只支持UTF-8编码。
    """

    def __init__(self, input_path: str, output_path: str) -> None:
        with open(input_path, "r", encoding="utf-8") as f:
            self._text: list[str] = f.readlines()
        if self._text[0].startswith(codecs.BOM_UTF8.decode('utf-8')):  # 去掉BOM
            self._text[0] = self._text[0][1:]
        self._c_header_paths: list[str] = _C_HEADER_PATHS.copy() + [os.path.dirname(input_path)]
        self._output_path: str = output_path
        self._added_headers: set[str] = set()

    def scan(self) -> None:
        """
        对#include进行深度优先遍历，并将全部内容展开。每个文件只会被插入一次。
        """
        line_count: int = 0
        while line_count < len(self._text):
            line = self._text[line_count]
            match = HEADER_PATTERN.match(line.strip())
            if match:
                header_name = match.group(1)[1:-1]
                if header_name not in self._added_headers:
                    self._text = self._text[:line_count] + self._read_c_header(header_name) + self._text[line_count + 1:]
                    line_count = -1
                else:
                    self._text[line_count] = "// " + line
            line_count += 1
        with open(self._output_path, "w", encoding="utf-8") as f:
            f.writelines(self._text)

    def _find_c_header(self, name: str) -> Optional[str]:
        """
        获取指定C头文件的具体路径。
        :param name: C头文件的文件名。
        :return: 完整路径，如果未找到则返回None。
        """
        for path in self._c_header_paths:
            if os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)
        print(f"[NOT FOUND]{name}")
        return None

    def _read_c_header(self, name: str) -> list[str]:
        """
        读取C头文件。
        :param name: C头文件的文件名。
        :return: 读取获得的文件内容（逐行）。如果未找到则返回空列表。
        """
        path = self._find_c_header(name)
        self._added_headers.add(name)
        if path:
            self._c_header_paths.append(os.path.dirname(path))
            with open(path, "r", encoding="utf-8") as f:
                print(f"[INCLUDE]{name}")
                return f.readlines()
        return []


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_c_source_file> <output_c_source_file>")
        return
    input_path = sys.argv[1].strip("\"")
    output_path = sys.argv[2].strip("\"")
    exploder = Exploder(input_path, output_path)
    exploder.scan()


if __name__ == "__main__":
    main()
