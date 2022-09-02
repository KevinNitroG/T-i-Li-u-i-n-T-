import json
import bs4
import subprocess
import sys
import re

def checker(package):
    #return str(subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout).split('\n')
    return str(subprocess.run(["pip", "install", package], capture_output=True, text=True).stdout)

def parser(filename, type, chapter=None):
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
	# links.sort(key=lambda n: int(n[n.find('-b')+2 : n.find('-b')+4]))

	full = []
	for link in links:
		raw_title = re.findall("-\d+-[0-9a-zA-z\-]+\.mp4", link)
		#title = raw_title[0][raw_title[0].find('-b'):raw_title[0].find('.mp4')]

		full.append([raw_title, link])

	if (type==1):
		return links
	elif (type==2):
		return '\n\n'.join(links)
	elif (type==3):
		txt = '#EXTM3U\n'
		for i in full:
			txt += f'#EXTINF:-1 group-title="{chapter}",{i[0]}\n{i[1]}\n\n'
		return txt

res = parser('toshiba.har', 3, 'Video Sửa Bo Điều hòa Toshiba Inverter 12000 Gas32 -SX2019')
print(res)

with open("full-links.m3u.txt", "w", encoding="utf-8") as f:
	f.writelines(res)
	f.close()

'''
Sử dụng hàm "parser":
	"1" nếu in dạng list
	"2" nếu in từng dòng
	"3" để in full
'''