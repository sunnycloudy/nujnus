from ruamel.yaml import YAML


# 加载 YAML 文档并保留映射的顺序
yaml = YAML(typ='safe')

# 设置为块风格输出，默认就是False，因此通常不需要显式设置
yaml.default_flow_style = False

yaml.preserve_quotes = True  # 保留引号
yaml.allow_unicode = True
yaml.indent(mapping=2, sequence=4, offset=2)  # 设置缩进
