#!/usr/bin/python
#_*_ coding:utf8 -*- #
import json
import sys,os
import xlrd
import xlwt

# json data for path
def data_for_path(file_path):
  with open(file_path, 'r') as f:
    json_data = json.load(f)
    return json_data
    
def xls_to_json(xls_file):
    # 打开 xls 文件
    workbook = xlrd.open_workbook(xls_file)
    # 获取第一个 sheet
    worksheet = workbook.sheet_by_index(0)
    # 获取行数和列数
    num_rows = worksheet.nrows
    num_cols = worksheet.ncols
    print("[xml] xls_to_json num_rows: %s", num_rows)
    print("[xml] xls_to_json num_cols: %s", num_cols)
    # 构建一个空的结果列表
    result = {}
    # 遍历每一行
    for i in range(num_rows):
        key = worksheet.cell_value(i, 0)
        value = worksheet.cell_value(i, 1)
        result[key] = value
    # 将结果列表转换为 json 格式
    return result

def json_to_xls(json_file, xls_file, tag_list):
    # 打开 json 文件
    with open(json_file, 'r') as f:
        data = json.load(f)
    # 创建一个新的 xls 文件
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Unity全面汉化')
    count = len(data)
    print("[xml] count: %s", count)
    
    line = 0
    for key, value in data.items():
      worksheet.write(line, 0, key)
      worksheet.write(line, 1, value)
      if key in tag_list:
        worksheet.write(line, 2, "UI展示")
      line += 1
    # 保存 xls 文件
    workbook.save(xls_file)

# data write to path
def data_write_to_path(data, output_path):
  with open(output_path, 'w') as json_file:
    json.dump(data, json_file, ensure_ascii=False)

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
    
def key_is_validate(key):
  filter_keys = ["requestId", "DC token", "DC Token", "wallet", "Digital collectible", "'s space" ]
  # 是否包含中文
  if is_contain_chinese(key):
     return False
  else:
    for filterKey in filter_keys:
      if filterKey in key:
        return False
    return True
    
def mkdir(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)
  
def del_none(sourcePath, keyPath):
  cPath = os.getcwd();
  print ("0. 工作路径: %s", cPath)
  
  filter_path = cPath + "/output"
  mkdir(filter_path)
  
  outPath = filter_path + "/filter.json"
  abnormalPath = filter_path + "/sourceAbnormal.json"
  excelPath = filter_path + "/excel.xls"
  differPath = filter_path + "/differ.json"
  
  if not os.path.isfile(sourcePath) :
    print ("当前文件不存在: %s", sourcePath)
    sys.exit(1)
  print ("1. 解析源文件: %s", sourcePath)
  source_data = data_for_path(sourcePath)
  key_list = data_for_path(keyPath)
  
  print ("2. 过滤 key 为中文、value == none、后端请求 类型的情况")
  del_list = []
  none_data = {}
  
  for key, value in source_data.items():
    if value is None:
      none_data[key] = ""
    elif value == "":
      none_data[key] = value
    elif key_is_validate(key) == False:
      del_list.append(key)
      none_data[key] = value

  for key in del_list:
    del source_data[key]
  #
  focus_data = {}
  # souce中没有的keys
  differ_list = []
  # 需要重点验证的keys
  tag_list = []
  for key in key_list:
    if key in source_data:
      tag_list.append(key)
      focus_data[key] = source_data[key]
    else:
      differ_list.append(key)
    
  print ("3. 输出过滤后文件: %s", outPath)
  data_write_to_path(source_data, outPath)
  print ("3. 输出删除后文件: %s", abnormalPath)
  data_write_to_path(none_data, abnormalPath)
  print ("3. 输出端上独有的key: %s", differPath)
  data_write_to_path(differ_list, differPath)
  print ("3. 生成excel: %s", excelPath)
  json_to_xls(outPath, excelPath, tag_list)
  
#  exportPath = cPath + "/test.json"
#  print ("4. 测试excel to json: %s", exportPath)
#  exportData = xls_to_json(excelPath)
#  data_write_to_path(exportData, exportPath)
  
if __name__ == '__main__':
  print ('脚本名:', str(sys.argv[0]))
  del_none(sys.argv[1], sys.argv[2])
