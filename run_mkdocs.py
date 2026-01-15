import sys
import yaml
import yaml_include
from mkdocs.__main__ import cli
from mkdocs.config import load_config

# 0. 先运行目录结构扫描
print("正在扫描目录结构并生成导航文件...")
import subprocess
subprocess.run([sys.executable, "script/scan_dir_structure.py"], check=True)
print("目录扫描完成！\n")

# 1. 注册 !include 标签到所有常用的 YAML 加载器
yaml.add_constructor('!include', yaml_include.Constructor(base_dir='.'), yaml.FullLoader)
yaml.add_constructor('!include', yaml_include.Constructor(base_dir='.'), yaml.SafeLoader)
yaml.add_constructor('!include', yaml_include.Constructor(base_dir='.'), yaml.Loader)

# 2. 重写 MkDocs 的配置加载函数
original_load_config = load_config

def custom_load_config(config_file=None, **kwargs):
    """自定义配置加载函数，使用支持 !include 的 YAML 加载器"""
    if config_file:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用支持 !include 的加载器解析 YAML
        config_data = yaml.load(content, yaml.FullLoader)
        
        # 使用原始函数处理解析后的数据
        return original_load_config(config_file=None, config_data=config_data, **kwargs)
    else:
        return original_load_config(config_file=config_file, **kwargs)

# 3. 替换 MkDocs 的配置加载函数
import mkdocs.config
mkdocs.config.load_config = custom_load_config

if __name__ == '__main__':
    sys.argv[0] = 'mkdocs'
    if len(sys.argv) == 1:
        sys.argv.append('serve')
    
    cli()