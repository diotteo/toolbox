#! /usr/bin/env python3

import requests
import xml.etree.ElementTree as ETree
from urllib.parse import urljoin

BASE_URL = 'https://sourceforge.net/projects/libsdlinput/files/'

class Page():
	def __init__(self, url=None, title=None, is_folder=False):
		self.url = url
		self.title = title
		self.is_folder = is_folder
		self.time = None
		self.childlist = []

	def append(self, child):
		self.childlist.append(child)


	def __str__(self):
		return self.title


def txtFromUrl(url):
  return requests.get(url).text

def idxFromTxt(txt):
	tidx = txt.find('<table id="files_list"')
	teidx = txt.find('</tbody>', tidx)
	tbidx = txt.find('<tbody>', tidx, teidx)
	return tidx, teidx, tbidx


def timeFromTxt(txt):
	tidx, teidx, tbidx = idxFromTxt(txt)
	lines = [s.strip() for s in txt[tbidx:teidx].split('\n')]
	for l in lines:
		if ('<tr title=' in l):
			pass


def printPages(page):
	ts = page.time
	if (ts is None):
		ts = 'N/A'
	print('{:s} - {:s}\n  {:s}'.format(ts, page.title, page.url))
	for c in page.childlist:
		printPages(c)


rootpage = Page(url = BASE_URL, title = 'root', is_folder = True)
pagelist = [rootpage]

while len(pagelist) > 0:
	page = pagelist.pop()
	txt = txtFromUrl(page.url)
	t = idxFromTxt(txt)
	tree = ETree.XML(txt[t[2]:t[1]+len('<tbody>')+1])

	for tr in tree.findall('tr'):
		newpage = Page()
		newpage.title = tr.attrib['title']
		newpage.url = urljoin(page.url, tr.find('th').find('a').attrib['href'])

		clazz = tr.attrib['class'].strip()
		newpage.is_folder = clazz == 'folder'
		if (newpage.is_folder):
			pagelist.append(newpage)

		time = None
	
		for td in tr.findall('td'):
			if ('headers' in td.attrib and td.attrib['headers'] == 'files_date_h'):
				abbr = td.find('abbr')
				time = abbr.attrib['title']
				break
		newpage.time = time
		page.append(newpage)

#printPages(rootpage)
pagelist = [rootpage]
while len(pagelist) > 0:
	page = pagelist.pop()
	if (page.is_folder):
		os.mkdir(page.title)
	else:
		dllist.append(page)
