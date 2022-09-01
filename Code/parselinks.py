import json
import bs4
import subprocess
import sys

def checker(package):
    #return str(subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout).split('\n')
    return str(subprocess.run(["pip", "install", package], capture_output=True, text=True).stdout)

def sorting_function(temp):
	for i in range(len(temp)):
		if temp[i:i+5] == '-bai-':
			key = i+5
			break
	ordinal = int(temp[key:key+2].replace('-',''))
	return ordinal

def parser(filename, type):
	links = []

	with open(filename, encoding='utf-8') as f:
		data = json.load(f)

	for i in data['log']['entries']:
		try:
			# elems = bs4.BeautifulSoup(str(content), 'html.parser').find('source').get('src')
			content = str(i['request']['url'])
			if ('__sd.mp4' in content) and ('m3u8' in content): 
				links.append(content)
		except Exception:
			pass

	links = [f"{i.replace('__sd', '')[:i.find('?nimblesessionid')-4]}" for i in links]

# shorting part
	links.sort(key=sorting_function)

	if (type==1):
		return links
	elif (type==2):
		return '\n'.join(links)

print(parser('test 6.har', 2))

'''
Sử dụng hàm "parser":
	"1" nếu in dạng list
	"2" nếu in từng dòng
'''
