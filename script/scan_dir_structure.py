#!/usr/bin/env python3
"""
自动扫描docs目录结构并生成MkDocs导航文件
"""

import os
import yaml
from pathlib import Path


def scan_docs_structure(docs_path="docs", nav_path="nav", skip_dirs=None):
    """
    扫描docs目录结构并生成导航文件
    
    Args:
        docs_path: docs目录路径
        nav_path: nav目录路径
        skip_dirs: 要跳过的目录列表
    """
    if skip_dirs is None:
        skip_dirs = ["asset"]
    
    docs_dir = Path(docs_path)
    nav_dir = Path(nav_path)
    
    # 确保nav目录存在
    nav_dir.mkdir(exist_ok=True)
    
    print(f"扫描目录: {docs_dir}")
    print(f"跳过目录: {skip_dirs}")
    
    # 扫描docs下的顶级目录
    for item in docs_dir.iterdir():
        if item.is_dir() and item.name not in skip_dirs:
            category_name = item.name
            nav_file = nav_dir / f"{category_name.capitalize()}.yml"
            
            print(f"\n处理分类: {category_name}")
            print(f"生成导航文件: {nav_file}")
            
            # 生成该分类的导航内容
            nav_content = generate_nav_content(category_name, item)
            
            # 写入导航文件
            with open(nav_file, 'w', encoding='utf-8') as f:
                f.write(nav_content)
            
            print(f"✓ 已生成: {nav_file}")
    
    print("\n✓ 目录扫描完成！")


def generate_nav_content(category_name, category_dir):
    """
    为指定分类目录生成导航内容
    
    Args:
        category_name: 分类名称
        category_dir: 分类目录路径
        
    Returns:
        str: 导航文件内容
    """
    lines = []
    
    # 添加分类标题
    lines.append(f"{category_name.capitalize()}:")
    
    # 收集所有.md文件
    md_files = list(category_dir.rglob("*.md"))
    
    # 按目录层级组织文件
    file_structure = {}
    
    for md_file in md_files:
        # 计算相对于分类目录的相对路径
        relative_path = md_file.relative_to(category_dir)
        
        # 如果是直接位于分类目录下的文件
        if len(relative_path.parts) == 1:
            file_structure.setdefault("root", []).append(md_file)
        else:
            # 文件在子目录中
            subdir = relative_path.parts[0]
            file_structure.setdefault(subdir, []).append(md_file)
    
    # 处理根目录下的文件
    if "root" in file_structure:
        for md_file in sorted(file_structure["root"]):
            title = md_file.stem  # 使用文件名作为标题
            nav_path = f"{category_name}/{md_file.name}"
            lines.append(f"  - {title}: {nav_path}")
    
    # 处理子目录
    for subdir in sorted([d for d in file_structure.keys() if d != "root"]):
        lines.append(f"  - {subdir}:")
        
        for md_file in sorted(file_structure[subdir]):
            relative_path = md_file.relative_to(category_dir)
            title = md_file.stem
            nav_path = f"{category_name}/{relative_path}"
            lines.append(f"    - {title}: {nav_path}")
    
    return "\n".join(lines)


def update_mkdocs_nav(mkdocs_file="mkdocs.yml"):
    """
    更新mkdocs.yml中的nav配置
    
    Args:
        mkdocs_file: mkdocs.yml文件路径
    """
    print(f"\n更新 {mkdocs_file} 中的导航配置...")
    
    with open(mkdocs_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找nav配置的开始位置
    nav_start = content.find("nav:")
    if nav_start == -1:
        print("⚠ 未找到nav配置，需要手动添加")
        return
    
    # 查找nav配置的结束位置（下一个顶级配置的开始）
    nav_end = content.find("\n\n", nav_start)
    if nav_end == -1:
        nav_end = len(content)
    
    # 生成新的nav配置
    nav_dir = Path("nav")
    nav_files = sorted(nav_dir.glob("*.yml"))
    
    # 修复：避免在nav:后产生多余空行
    new_nav_content = "nav:\n"
    new_nav_content += "  - Welcome: index.md\n"
    
    for nav_file in nav_files:
        category_name = nav_file.stem.lower()
        new_nav_content += f"  - !include nav/{nav_file.name}\n"
    
    # 移除最后一个多余的换行符
    if new_nav_content.endswith("\n"):
        new_nav_content = new_nav_content.rstrip("\n")
    
    # 替换nav配置
    new_content = content[:nav_start] + new_nav_content + content[nav_end:]
    
    with open(mkdocs_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✓ mkdocs.yml导航配置已更新")


def main():
    """主函数"""
    print("=" * 50)
    print("MkDocs目录结构扫描工具")
    print("=" * 50)
    
    # 扫描目录结构并生成导航文件
    scan_docs_structure()
    
    # 更新mkdocs.yml中的导航配置
    update_mkdocs_nav()
    
    print("\n" + "=" * 50)
    print("✓ 所有操作完成！")
    print("现在可以运行: python run_mkdocs.py")
    print("=" * 50)


if __name__ == "__main__":
    main()