#!/usr/bin/env python3
"""
MkDocs 构建脚本
自动生成配置文件并启动 MkDocs 服务
"""

import sys
import subprocess
from pathlib import Path
from mkdocs.__main__ import cli

def generate_mkdocs_config():
    """生成 mkdocs.yml 配置文件"""
    print("=" * 60)
    print("正在生成 mkdocs.yml 配置文件...")
    print("=" * 60)
    
    script_path = Path(__file__).parent / "script" / "create_mkdocs_yml.py"
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print("\n✓ 配置文件生成成功！\n")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 配置文件生成失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ 找不到脚本文件: {script_path}")
        sys.exit(1)

def main():
    """主函数"""
    # 1. 生成配置文件
    generate_mkdocs_config()
    
    # 2. 检查配置文件是否存在
    config_file = Path(__file__).parent / "mkdocs.yml"
    if not config_file.exists():
        print(f"❌ 错误: 配置文件不存在: {config_file}")
        sys.exit(1)
    
    # 3. 启动 MkDocs
    print("=" * 60)
    print("正在启动 MkDocs 服务...")
    print("=" * 60)
    
    sys.argv[0] = 'mkdocs'
    
    # 如果没有指定命令，默认使用 serve
    if len(sys.argv) == 1:
        sys.argv.append('serve')
    
    # 调用 MkDocs CLI
    cli()

if __name__ == '__main__':
    main()