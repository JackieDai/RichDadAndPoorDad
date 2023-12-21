# 正则匹配相关
import re
# 系统库
import os
# 日期
from datetime import datetime
# 时间
import time

# 获取文件夹下的子文件夹
def list_subdirectories(root_dir):
    subdirectories = [d for d in os.listdir(root_dir) 
                      if os.path.isdir(os.path.join(root_dir, d)) 
                      and not d.startswith('.')  # 排除隐藏文件夹
                      and d.lower() != 'unfamiliarwords']  # 排除名为 UnfamiliarWords 的文件夹

    subdirectories.sort()
    return subdirectories

# 获取.md 文件的文件名称
def list_md_file(file_path):
    md_files = [f for f in os.listdir(file_path) if f.endswith(".md")]
    md_files.sort()
    return md_files

# 计算md文件的标题数量
def count_markdown_headings(file_path):
    # 读取 Markdown 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配 Markdown 标题
    heading_pattern = re.compile(r'^#+\s', re.MULTILINE)
    matches = heading_pattern.findall(content)

    # 统计各级别标题的数量
    heading_count = {}
    for match in matches:
        level = match.count('#')
        heading_count[level] = heading_count.get(level, 0) + 1

    # 打印统计结果
    result = []
    for level, count in heading_count.items():
        # print(f'Level {level} headings: {count}')
        info_dict = {
            "level": level,
            "headings": count
        }
        result.append(info_dict)
    return result


# 注入内容
def inject_content_to_markdown(file_path, content_to_inject):
    try:
        # 打开原始Markdown文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()

        # 向内容开头注入新的内容
        new_content = f"{content_to_inject}\n\n{original_content}"

        # 将修改后的内容写回Markdown文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"内容已成功注入到文件：{file_path}")

    except Exception as e:
        print(f"发生错误：{e}")

# 注入的内容
def inject_content_func(markdown_file_path, markdown_file_name):

    time.sleep(1)

    # 获取当前时间
    current_time = datetime.now()

    markdown_file_name = markdown_file_name.split(".")[0]

    # 格式化时间为字符串
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 要注入的内容
    inject_content = f'''---
title: {markdown_file_name}
date: {formatted_time}
index_img: /img/richpoordad.png
excerpt: The Part of {markdown_file_name} unfamiliar words
tags: 
    - RichDadPoorDad
categories: English
---'''
    print(inject_content)
    inject_content_to_markdown(markdown_file_path, inject_content)


if __name__ == "__main__":
    # if u want to log ecah detail of secitons, just set the boolen value True
    should_log_detail = False
    # 指定文件夹路径
    folder_path = '/Users/lingxiao/RichDadAndPoorDad'
    # 获取子文件夹列表
    subdirectories = list_subdirectories(folder_path)

    total_count = 0

    # 输出子文件夹名称
    for subdir in subdirectories:
        # print(subdir)
        folder_sub_path = folder_path + "/" + subdir

        subdir_count = 0

        
        if should_log_detail:
            print("==========="*5)
            print(f"{subdir} section detail as follows:")
       
        md_files = list_md_file(folder_sub_path)

        # 打印文件名
        for md_file in md_files:
            whole_md_address = folder_sub_path + "/" + md_file
            # 给 md 文件注入 通用脚本  !!!!!!
            inject_content_func(whole_md_address,md_file)

            # 计算每一个md文件的标题个数
            result = count_markdown_headings(whole_md_address)
            for info_dict in result:
                if info_dict["level"] == 2:
                    word_count = info_dict["headings"]
                    total_count = total_count + word_count
                    subdir_count = subdir_count + word_count
                    if should_log_detail:
                        print(f'\t{md_file} words count == {word_count}')

        log_str = f"{subdir} words count == {subdir_count} \n"
        if should_log_detail:
            log_str = f"---Total count:{subdir_count} \n"
        print(log_str)

    print(f"RichDadAndPoorDad 总 数 == {total_count}\n")    




