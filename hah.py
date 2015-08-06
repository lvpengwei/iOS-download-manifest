#!/usr/bin/env python
# -*- coding: utf-8 -*-

' hah '


__author__ = 'pengwei.lv'


import sys, os, time

URLPATH = 'https://ios.ichuanyi.me/iPhone/'

# 获取ipa文件的名字
def getIPAFileNames():
	list = [os.path.splitext(file)[0] for file in os.listdir('./ipa') if os.path.splitext(file)[1] == '.ipa']
	return list

# 生成对应的plist
def createPlistFile(filenames):
	f = open('./template.plist', 'r')
	plistTemplate = f.read()
	for filename in filenames:
		path = './plist/' + filename + '.plist'
		plist = plistTemplate.replace('#url#', URLPATH + 'ipa/' + filename + '.ipa')
		file = open(path, 'w')
		file.write(plist)
		file.close()
	f.close()

# <div class="page">
#     <div class="box">
#         <h1>feature</h1>
#         <a href="itms-services://?action=download-manifest&url=https://ios.ichuanyi.me/iPhone/cyzs-rc.plist" class="last">scheme: time</a>
#     </div>
# </div>

# 生成code
def createHTMLCode(map):
	code = '<div class="page">\n'
	for (feature, arr) in map.items():
		code = code + '\t<div class="box">\n'
		code = code + '\t\t<h1>' + feature + '</h1>\n'
		i = 0
		for scheme in arr:
			cls = ''
			if i % 3 == 1:
				cls = ' class="middle"'
			elif i % 3 == 2:
				cls = ' class="last"'
			i = i + 1
			filename = feature + '-' + scheme
			code = code + '\t\t<a href="itms-services://?action=download-manifest&url=' + URLPATH + 'plist/' + filename + '.plist"' + cls + '>' + scheme + ': ' + time.ctime(os.path.getmtime('./ipa/' + filename+ '.ipa')) + '</a>\n'
		code = code + '\t</div>\n'
	code = code + '\t</div>'
	return code

# 生成html
def createHTMLFile(code):
	f = open('./template.html', 'r')
	htmlTemplate = f.read()
	file = open('./html/index.html', 'w')
	html = htmlTemplate.replace('##', code)
	file.write(html)
	file.close()
	f.close()

def convertToMap(filenames):
	map = {}
	for filename in filenames:
		tempList = filename.rsplit('-', 1)
		if len(tempList) == 2:
			feature = tempList[0]
			scheme = tempList[1]
			if (feature in map.keys()) == False:
				map[feature] = []
			map[feature].append(scheme)
	return map


def main():
	filenames = getIPAFileNames()
	createPlistFile(filenames)
	map = convertToMap(filenames)
	code = createHTMLCode(map)
	createHTMLFile(code)

if __name__ == '__main__':
	main()