#!/usr/bin/python
#_*_ coding:utf8 -*- #

import os, time, datetime
from os import listdir
from os.path import isfile, islink, realpath, join, basename
import random
import json
from PIL import Image

import urllib
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# ========================================================================================================
# Global Fields
# ========================================================================================================

gCmd = ''

# ========================================================================================================
# Common Functions
# ========================================================================================================

# 获取今天时间
def get_today_time():
  return datetime.datetime.now().strftime('%Y-%m-%d')

# 创建文件夹
def mkdir(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)

def delete_file(filePath):
  if os.path.exists(filePath):
    os.remove(filePath)
  else:
    print "要删除的文件不存在！%s" %(filePath)

# 复制文件到指定路径
def copy_file(srcPath, dstPath):
  cmd = "cp \"%s\" \"%s\"" %(srcPath, dstPath)
  os.system(cmd)

# 重命名
def rename_file(srcPath, dstPath):
  os.rename(srcPath, dstPath)

# 图片是否有效
def IsValidImage(pathfile):
  bValid = True
  try:
    Image.open(pathfile).verify()
  except:
    bValid = False
  return bValid

# 读取数据
def data_for_path(file_path):
  f = file(file_path)
  return json.load(f)

# data write to path
def data_write_to_path(data, output_path):
  fw = open(output_path, 'w')
  fw.write(json.dumps(data, indent=2, ensure_ascii=False).decode('utf8'))
  fw.close()

# 下载文件
def download_file(from_url,to_path):
  conn = urllib.urlopen(from_url)
  f = open(to_path,'wb')
  f.write(conn.read())
  f.close()

# 路径下所有文件夹名称
def folder_names(dir):
  folders = []
  path = os.listdir(dir)
  for p in path:
    if not os.path.isfile(p):
      folders.append(p)
  return folders

# 路径下所有文件夹路径
def folder_paths(dir):
  folders = []
  path = os.listdir(dir)
  for p in path:
    if not os.path.isfile(p):
      path = dir + '/' + p
      folders.append(path)
  return folders

##

def filpImageMask(img_path, save_path):
  img = Image.open(img_path)
  img = img.convert("RGBA")
  datas = img.getdata()

  #  print img.size  #图片的尺寸
  #  print img.mode  #图片的模式
  #  print img.format  #图片的格式

  width = img.size[0]
  height = img.size[1]
  newData = list()
  edgeInset = 5

  edge = False
  for j in range(0, height):
    for i in range(0, width):
      if i < edgeInset or i > (width - edgeInset) or j < edgeInset or j > (height - edgeInset) :
        #        newData.append(( 0, 0, 0, 0))
        edge = True
      #      else :
      pixelData = img.getpixel((i, j))
      a = pixelData[3]
      newData.append(( 0, 0, 0, 255 - a))
  img.putdata(newData)
  img.save(save_path,"PNG")
  return edge

