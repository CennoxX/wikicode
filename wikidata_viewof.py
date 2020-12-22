#!/usr/bin/python
# -*- coding: utf-8  -*-
# Seach for Commons 'views from' categories and create new items for them
# 12 December 2020 - started
# 17 December 2020 - bot version
from __future__ import unicode_literals

import pywikibot
import numpy as np
import time
import string
from pywikibot import pagegenerators
from pywikibot.data import api
import urllib

commons = pywikibot.Site('commons', 'commons')
repo = commons.data_repository()  # this is a DataSite object
maxnum = 100
j = 0
debug = False

def search_entities(site, itemtitle,limit=100,offset=0):
	 params = { 'action' :'query', 
	 			'list': 'search',
				'format' : 'json',
				'srlimit': limit,
				'sroffset': offset,
				'srnamespace': 14,
				'srsearch': itemtitle}
	 request = api.Request(site=site, parameters=params)
	 return request.submit()

def newitem(category, items,cat=True):
	new_item = pywikibot.ItemPage(repo)
	label = category.title()
	if cat == False:
		label = label.replace('Category:','')
	# if cat == True and 'Category:' not in label:
	# 	label = 'Category:' + label
	new_item.editLabels(labels={"en":label}, summary="Creating item")
	candidate_item = pywikibot.ItemPage(repo, new_item.getID())
	print(candidate_item)

	data = {'sitelinks': [{'site': 'commonswiki', 'title': category.title()}]}
	candidate_item.editEntity(data, summary=u'Add commons sitelink')

	for item in items:
		claim = pywikibot.Claim(repo, item[0])
		if item[0] == 'P458':
			claim.setTarget(item[1])
		else:
			claim.setTarget(pywikibot.ItemPage(repo, item[1]))
		try:
			candidate_item.addClaim(claim, summary=u'Setting '+item[0]+' value')
			# claim.addSources([statedin, retrieved], summary=u'Add source.')
		except:
			print("That didn't work")
	return candidate_item

offset = 0
step = 100
for i in range(0,100):
	offset += step
	# View of, Views of, View from, Views from
	candidates = search_entities(commons, '":Views_from"',limit=step,offset=offset)
	for result in candidates['query']['search']:
		targetcat = pywikibot.Page(commons, str(result['title']))
		print('https://commons.wikimedia.org/wiki/'+targetcat.title().replace(" ", "_"))
		if ':Views from' in targetcat.title():
			try:
				wd_item = pywikibot.ItemPage.fromPage(targetcat)
				item_dict = wd_item.get()
				print(wd_item.title())
				continue
			except:
				null = 0
			target = ''
			test = 'n'
			for parentcat in targetcat.categories():
				if target == '' and 'view' not in parentcat.title().lower() and 'redirect' not in parentcat.title().lower() and 'categor' not in parentcat.title().lower().replace('category:','') and 'redirect' not in parentcat.text.lower():
					try:
						wd_item = pywikibot.ItemPage.fromPage(parentcat)
						item_dict = wd_item.get()
						print(wd_item.title())
					except:
						continue
					# If we have a P301 value, switch to using that Wikidata item
					try:
						existing_id = item_dict['claims']['P301']
						print('P301 exists, following that.')
						for clm2 in existing_id:
							wd_item = clm2.getTarget()
							item_dict = wd_item.get()
							qid = wd_item.title()
							print(wd_item.title())
					except:
						null = 0

					print('https://commons.wikimedia.org/wiki/'+parentcat.title().replace(" ","_"))
					if debug:
						test = input('OK?')
					else:
						test = 'y'
					if test == 'y':
						target = wd_item.title()

			if target != '':
				print(target)
				# Start assembling the Wikdata entry
				target_text = targetcat.get()
				items = [['P31','Q4167836']] # Instance of Wikimedia category
				items.append(['P971','Q2075301']) # combines view
				items.append(['P971',target]) # combines parentcat
				print(items)

				# if debug:
				# 	test = input('OK?')
				# else:
				# 	test = 'y'
				# if test == 'y':
				new_item = newitem(targetcat, items)
				newclaim = pywikibot.Claim(repo, 'P8933')
				newclaim.setTarget(new_item)
				wd_item.addClaim(newclaim, summary=u'Setting P8933 value')
				j += 1
				print(j)

				if j >= maxnum:
					exit()
