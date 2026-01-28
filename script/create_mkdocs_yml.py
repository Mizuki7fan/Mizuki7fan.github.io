#!/usr/bin/env python3
"""
自动扫描docs目录结构并生成完整的mkdocs.yml配置文件
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any

class MkDocsConfigGenerator:
    """MkDocs配置文件生成器"""
    
    def __init__(self, project_root: str = "."):
        """
        初始化生成器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.skip_dirs = ["asset"]  # 跳过的目录列表
        
    def scan_directory(self, directory: Path, relative_to: Path = None) -> List[Dict[str, Any]]:
        """
        递归扫描目录结构，生成导航配置
        
        Args:
            directory: 要扫描的目录
            relative_to: 相对路径的基准目录
            
        Returns:
            导航配置列表
        """
        if relative_to is None:
            relative_to = self.docs_dir
            
        nav_items = []
        
        # 收集所有文件和子目录
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_file(), x.name))
        
        for item in items:
            # 跳过隐藏文件和指定目录
            if item.name.startswith('.') or item.name in self.skip_dirs:
                continue
                
            if item.is_file() and item.suffix == '.md':
                # Markdown文件
                title = item.stem
                relative_path = item.relative_to(relative_to)
                nav_items.append({title: str(relative_path)})
                
            elif item.is_dir():
                # 子目录
                sub_items = self.scan_directory(item, relative_to)
                if sub_items:  # 只添加非空目录
                    nav_items.append({item.name: sub_items})
        
        return nav_items
    
    def generate_nav_config(self) -> List[Dict[str, Any]]:
        """
        生成导航配置
        
        Returns:
            导航配置列表
        """
        nav = []
        
        # 添加首页
        index_file = self.docs_dir / "index.md"
        if index_file.exists():
            nav.append({"Welcome": "index.md"})
        
        # 扫描docs目录下的所有顶级目录
        for item in sorted(self.docs_dir.iterdir()):
            if item.is_dir() and item.name not in self.skip_dirs and not item.name.startswith('.'):
                # 扫描该目录
                sub_items = self.scan_directory(item)
                if sub_items:
                    nav.append({item.name: sub_items})
        
        return nav
    
    def generate_config(self) -> Dict[str, Any]:
        """
        生成完整的mkdocs.yml配置
        
        Returns:
            配置字典
        """
        config = {
            'site_name': 'mizuki7fan site',
            'site_url': 'https://mizuki7fan.github.io/',
            'site_author': 'meigyoku',
            'site_description': 'mizuki7fan site',
            
            # Repository
            'repo_name': 'mizukifan site',
            'repo_url': 'https://github.com/Mizuki7fan/Mizuki7fan.github.io',
            
            'use_directory_urls': False,
            
            # Theme
            'theme': {
                'name': 'material',
                'logo': 'asset/favi.ico',
                'favicon': 'asset/favi.ico',
                'language': 'zh',
                'features': [
                    'navigation.tabs',
                    'navigation.sections',
                    'search.highlight',
                    'content.annotate'
                ],
                'palette': [
                    {
                        'scheme': 'default',
                        'primary': 'indigo',
                        'accent': 'indigo'
                    },
                    {
                        'scheme': 'slate',
                        'primary': 'indigo',
                        'accent': 'indigo'
                    }
                ]
            },
            
            # Navigation (自动生成)
            'nav': self.generate_nav_config(),
            
            # Dev server
            'dev_addr': '0.0.0.0:6324',
            
            # Markdown extensions
            'markdown_extensions': [
                {'toc': {'permalink': True}},
                'tables',
                'fenced_code',
                {'pymdownx.arithmatex': {'generic': True}},
                'admonition',
                'pymdownx.details'
            ],
            
            # Extra JavaScript
            'extra_javascript': [
                'javascripts/mathjax.js',
                'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
            ],
            
            # Plugins
            'plugins': [
                'search',
                {
                    'minify': {
                        'minify_html': True,
                        'minify_js': True,
                        'minify_css': True,
                        'htmlmin_opts': {
                            'remove_comments': True
                        }
                    }
                },
                {
                    'pdf-export': {
                        'enabled': False
                    }
                }
            ]
        }
        
        return config
    
    def save_config(self, output_file: str = "mkdocs.yml"):
        """
        保存配置到文件
        
        Args:
            output_file: 输出文件路径
        """
        config = self.generate_config()
        output_path = self.project_root / output_file
        
        # 使用自定义的YAML格式化
        yaml_content = self._format_yaml(config)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"✓ 已生成配置文件: {output_path}")
        print(f"✓ 共扫描到 {self._count_nav_items(config['nav'])} 个导航项")
    
    def _format_yaml(self, config: Dict[str, Any]) -> str:
        """
        格式化YAML输出，使其更易读
        
        Args:
            config: 配置字典
            
        Returns:
            格式化后的YAML字符串
        """
        # 使用PyYAML生成基础YAML
        yaml_str = yaml.dump(
            config,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=1000  # 避免长行被折叠
        )
        
        return yaml_str
    
    def _count_nav_items(self, nav: List[Dict[str, Any]]) -> int:
        """
        递归统计导航项数量
        
        Args:
            nav: 导航配置列表
            
        Returns:
            导航项总数
        """
        count = 0
        for item in nav:
            count += 1
            if isinstance(item, dict):
                for value in item.values():
                    if isinstance(value, list):
                        count += self._count_nav_items(value)
        return count
    
    def print_nav_structure(self):
        """打印导航结构预览"""
        nav = self.generate_nav_config()
        print("\n" + "=" * 60)
        print("导航结构预览:")
        print("=" * 60)
        self._print_nav_recursive(nav, indent=0)
        print("=" * 60 + "\n")
    
    def _print_nav_recursive(self, nav: List[Dict[str, Any]], indent: int = 0):
        """
        递归打印导航结构
        
        Args:
            nav: 导航配置列表
            indent: 缩进级别
        """
        prefix = "  " * indent
        for item in nav:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, list):
                        print(f"{prefix}📁 {key}/")
                        self._print_nav_recursive(value, indent + 1)
                    else:
                        print(f"{prefix}📄 {key} -> {value}")


def main():
    """主函数"""
    print("=" * 60)
    print("MkDocs配置文件自动生成工具")
    print("=" * 60)
    
    # 创建生成器实例
    generator = MkDocsConfigGenerator()
    
    # 检查docs目录是否存在
    if not generator.docs_dir.exists():
        print(f"❌ 错误: docs目录不存在: {generator.docs_dir}")
        return
    
    print(f"\n📂 扫描目录: {generator.docs_dir}")
    print(f"⏭️  跳过目录: {', '.join(generator.skip_dirs)}")
    
    # 打印导航结构预览
    # generator.print_nav_structure()
    
    # 生成并保存配置
    generator.save_config()
    
    print("\n" + "=" * 60)
    print("✓ 配置文件生成完成！")
    print("💡 提示: 运行 'mkdocs serve' 或 'python build_mkdocs.py' 启动服务")
    print("=" * 60)


if __name__ == "__main__":
    main()
