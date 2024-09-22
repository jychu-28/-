import csv
import argparse

# 函数：处理GTF文件并添加gene_name标签
def add_gene_name(gtf_file, output_file):
    with open(gtf_file, 'r') as infile, open(output_file, 'w') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        for row in reader:
            # 跳过注释行
            if row[0].startswith("#"):
                outfile.write("\t".join(row) + "\n")
                continue

            feature_type = row[2]
            attributes = row[8]

            # 如果第三列是gene，增加gene_name标签
            if feature_type == 'gene':
                # 解析现有属性字符串
                attrs = parse_attributes(attributes)

                # 添加gene_name，如果不存在则将gene_id的值作为gene_name
                if 'gene_id' in attrs:
                    gene_id = attrs['gene_id']
                    attrs['gene_name'] = gene_id

                # 重新构建属性字符串
                new_attributes = format_attributes(attrs)
                row[8] = new_attributes

            # 写入修改后的行
            outfile.write("\t".join(row) + "\n")

# 辅助函数：解析GTF文件的第9列的属性信息为字典
def parse_attributes(attr_string):
    attrs = {}
    items = attr_string.split(';')
    for item in items:
        if item.strip():
            key, value = item.strip().split(' ')
            attrs[key] = value.strip('"')
    return attrs

# 辅助函数：将字典格式化为GTF第9列的字符串
def format_attributes(attrs):
    attr_list = []
    for key, value in attrs.items():
        attr_list.append(f'{key} "{value}"')
    return "; ".join(attr_list) + ";"

# 主函数：处理命令行输入
def main():
    # 使用argparse模块处理命令行参数
    parser = argparse.ArgumentParser(description="Add gene_name tag to GTF file if feature is 'gene'.")
    parser.add_argument('input_gtf', type=str, help='Input GTF file')
    parser.add_argument('output_gtf', type=str, help='Output GTF file')

    # 解析参数
    args = parser.parse_args()

    # 调用添加gene_name的函数
    add_gene_name(args.input_gtf, args.output_gtf)

# 如果该脚本是作为主程序运行，则执行main函数
if __name__ == "__main__":
    main()
