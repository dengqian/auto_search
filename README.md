## 功能描述

国家自然科学基金查询系统自动查询脚本，可以添加多个查询条件，自动识别验证码，提交项目查询

## 环境要求

python PIL(Pillow)库, pytesseract库用于验证码识别，firefox驱动geckodriver

###1.安装pip
sudo apt-get install python-pip python-dev build-essential 
###2.安装Pillow
pip install Pillow
###3.安装tesseract-ocr
sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
### 安装OCR引擎
sudo apt-get install tesseract-ocr
### 安装训练数据(equ为数学公式包)
sudo apt-get install tesseract-ocr-eng tesseract-ocr-chi-sim  tesseract-ocr-equ
### 可以跳过，可选安装Leptonica
sudo apt-get install liblept5  libleptonica-dev
###4.安装pytesseract
pip install pytesseract：

## 使用方法
year.config为查询年份的配置文件
keyword.config是关键词的配置文件
subject.config是申请代码的配置文件

上述在配置文件都是每行一个值，注意文件末尾不要留空行

资助类别没有单独建立配置文件，需要修改的话要再auto_search.py里面直接更改，第91行的数组，第90行的数组是从上到下的各个类别对应的值，可以把需要写到91行的数组里面

运行auto_search.py
结果写到了result.txt, 每次都是在文件末尾写入新的结果。每次查询结束的结果需要手动删除。
