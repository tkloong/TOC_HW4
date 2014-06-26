#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author		: 陳勁龍
#Student ID	: F74005018
#Description: Please refer to 'README.md'

import sys
import urllib
import json
import re

if len(sys.argv) != 2:
	print 'Usage: {0} <URL>'.format(sys.argv[0])
	sys.exit()
try:
	data = json.load(urllib.urlopen(sys.argv[1]))
except IOError as e:
	print 'I/O Error({0}): {1}'.format(e.errno, e.strerror)
	sys.exit()
except ValueError:
	print 'Decoding JSON has failed'
	sys.exit()
if data == []:
	print 'Decoded JSON is empty'
	sys.exit()

road = dict()
maxRecord = dict()
maxRecord['distinctMonth'] = 0
for datum in data:
	match = re.search(u'((?<=區).*大道)|((?<=區).*路)|((?<=區).*街)|((?<=區).*巷)', datum[u'土地區段位置或建物區門牌'])
	if match is not None:
		# Create new record 
		if road.get(match.group(0)) is None:
			road[match.group(0)] = dict() 
			road[match.group(0)]['maxTransaction'] = 0
			road[match.group(0)]['minTransaction'] = 99999999
		# Record every road's distinct year and month and update prices
		road[match.group(0)][datum[u'交易年月']] = True
		if road[match.group(0)]['maxTransaction'] < datum[u'總價元']:
			road[match.group(0)]['maxTransaction'] = datum[u'總價元']
		elif road[match.group(0)]['minTransaction'] > datum[u'總價元']:
			road[match.group(0)]['minTransaction'] = datum[u'總價元']
		if len(road[match.group(0)]) > maxRecord['distinctMonth']:
			result = dict()	# Clear result
			maxRecord['distinctMonth'] = len(road[match.group(0)])
			maxRecord['address'] = match.group(0)
			result[match.group(0)] = dict()
			result[match.group(0)]['address'] = datum[u'土地區段位置或建物區門牌']
			result[match.group(0)]['max'] = road[match.group(0)]['maxTransaction']
			result[match.group(0)]['min'] = road[match.group(0)]['minTransaction']
		elif len(road[match.group(0)]) == maxRecord['distinctMonth']:
			if match.group(0) in maxRecord['address']:
				result[match.group(0)]['max'] = road[match.group(0)]['maxTransaction']
				result[match.group(0)]['min'] = road[match.group(0)]['minTransaction']
			else:	# Update result
				maxRecord['address'] += match.group(0) + ","
				result[match.group(0)] = dict()
				result[match.group(0)]['address'] = datum[u'土地區段位置或建物區門牌']
				result[match.group(0)]['max'] = road[match.group(0)]['maxTransaction']
				result[match.group(0)]['min'] = road[match.group(0)]['minTransaction']
for k in result.keys():
	print u'{0}, 最高成交價: {1}, 最低成交價: {2}'.format(re.search(u'.*大道|.*路|.*街|.*巷', result[k]['address']).group(0), result[k]['max'], result[k]['min'])

