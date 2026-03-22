#!/bin/bash

# # 加载系统级bash配置
if [[ -f "/data/workspace/configure/.bashrc" ]]; then
    source "/data/workspace/configure/.bashrc"
fi

# 项目特定的bash配置
# 这个文件只在该项目打开终端时生效

# 激活Python虚拟环境
if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
    echo "Virtual environment activated: $(python --version)"
fi

# 添加项目路径到PYTHONPATH
if [[ -n "$VIRTUAL_ENV" ]]; then
    export PYTHONPATH="$PYTHONPATH:${PWD}"
fi

# 项目特定的别名或函数
alias run="python build_mkdocs.py"
alias build="python build_mkdocs.py"

echo "Mizuki7fan.github.io project environment loaded"
