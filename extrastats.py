#!/usr/bin/python

import argparse
import re
import json
import operator

' function to parse through array of lines '
def placeInDict(mainPlayer, otherPlayer, damageNum, damageDict, curClass):
	if mainPlayer[0] in damageDict:
		if curClass[mainPlayer[0]] in damageDict[mainPlayer[0]]['classes']:
			' seriously overkill and way too complicated...oh well '
			if otherPlayer[0] in damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players']:
				if curClass[otherPlayer[0]] in damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'][otherPlayer[0]]['classes']:
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'][otherPlayer[0]]['classes'][curClass[otherPlayer[0]]]['da'] += damageNum
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'][otherPlayer[0]]['total_da'] += damageNum
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['total_da'] += damageNum
					damageDict[mainPlayer[0]]['total_da'] += damageNum
				else:
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'][otherPlayer[0]]['classes'].update({
						curClass[otherPlayer[0]] : {
							'da' : damageNum,
						},
					})
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'][otherPlayer[0]]['total_da'] += damageNum
					damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['total_da'] += damageNum
					damageDict[mainPlayer[0]]['total_da'] += damageNum
			else:
				damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['players'].update({
					otherPlayer[0] : {
						'classes' : {
							curClass[otherPlayer[0]] : {
								'da' : damageNum,
							}
						},
						'total_da' : damageNum,
						'pdata' : {
							'team' : otherPlayer[3],
							'pname' : otherPlayer[2],
							'pnum' : otherPlayer[1]
						}
					}
				})
				damageDict[mainPlayer[0]]['classes'][curClass[mainPlayer[0]]]['total_da'] += damageNum
				damageDict[mainPlayer[0]]['total_da'] += damageNum
		else:
			damageDict[mainPlayer[0]]['classes'].update({
				curClass[mainPlayer[0]] : {
					'players' : {
						otherPlayer[0] : {
							'classes' : {
								curClass[otherPlayer[0]] : {
									'da' : damageNum,
								}
							},
							'total_da' : damageNum,
							'pdata' : {
								'team' : otherPlayer[3],
								'pname' : otherPlayer[2],
								'pnum' : otherPlayer[1]
							}
						}
					},
					'total_da' : damageNum
				}
			})
			damageDict[mainPlayer[0]]['total_da'] += damageNum
	else:
		damageDict.update({
			mainPlayer[0] : {
				'classes' : {
					curClass[mainPlayer[0]] : {
						'players' : {
							otherPlayer[0] : {
								'classes' : {
									curClass[otherPlayer[0]] : {
										'da' : damageNum,
									}
								},
								'total_da' : damageNum,
								'pdata' : {
									'team' : otherPlayer[3],
									'pname' : otherPlayer[2],
									'pnum' : otherPlayer[1]
								}
							}
						},
						'total_da' : damageNum
					}
				},
				'total_da' : damageNum,
				'pdata' : {
					'team' : mainPlayer[3],
					'pname' : mainPlayer[2],
					'pnum' : mainPlayer[1]
				}
			}
		})


' some variables '
damageG = dict()
damageR = dict()
classes = dict()
inRound = False

' simple regex to find needed lines '
a = re.compile(".*triggered \"damage\" against.*")
b = re.compile(".*Round_Start.*")
c = re.compile(".*Round_Win.*")
d = re.compile(".*changed role to.*|.*spawned as.*")

playernumstr = '<[0-9]+>'
steamidstr = '<STEAM_[0-9]+:[0-9]+:[0-9]+>'
pteamstr = '<[Red|Blue|unknown]+>'

' parses command line argument '
parser = argparse.ArgumentParser()
parser.add_argument("file", help="please input the log's name")
args = parser.parse_args()

' used for internal testing '
' fileLoc = "C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\\tf\logs\\" + args.file + ".log" '

' used for server '
fileLoc = args.file

' opens files '
with open(fileLoc) as f:
	data = f.read().splitlines()
f.close()

' read through data and store damage given/received when IN a round '
for l in data:
	if b.match(l):
		inRound = True

	if c.match(l):
		inRound = False

	' keeps their classes up to date... '
	if d.match(l):
		temp = l.split('"')[1::2]

		player = [temp[0][re.search(steamidstr, temp[0]).start()+1:re.search(pteamstr, temp[0]).start()-1],
			temp[0][re.search(playernumstr, temp[0]).start()+1:re.search(steamidstr, temp[0]).start()-1],
			temp[0][0:re.search(playernumstr, temp[0]).start()], 
			temp[0][re.search(pteamstr, temp[0]).start()+1:int(len(temp[0])-1)]]

		if player[0] in classes:
			classes[player[0]] = temp[1]
		else:
			classes.update({ player[0] : temp[1] })

	' stores data in dictionaries accordingly '
	if a.match(l) and inRound:
		temp = l.split('"')[1::2]

		'i hate regex sometimes'
		top = [temp[0][re.search(steamidstr, temp[0]).start()+1:re.search(pteamstr, temp[0]).start()-1],
			temp[0][re.search(playernumstr, temp[0]).start()+1:re.search(steamidstr, temp[0]).start()-1],
			temp[0][0:re.search(playernumstr, temp[0]).start()], 
			temp[0][re.search(pteamstr, temp[0]).start()+1:int(len(temp[0])-1)]]

		bottom = [temp[2][re.search(steamidstr, temp[2]).start()+1:re.search(pteamstr, temp[2]).start()-1],
			temp[2][re.search(playernumstr, temp[2]).start()+1:re.search(steamidstr, temp[2]).start()-1],
			temp[2][0:re.search(playernumstr, temp[2]).start()], 
			temp[2][re.search(pteamstr, temp[2]).start()+1:int(len(temp[2])-1)]]
		
		placeInDict(top, bottom, int(temp[3]), damageG, classes)
		placeInDict(bottom, top, int(temp[3]), damageR, classes)


' print out the results in a json string '
print json.dumps([['damage_given', damageG], ['damage_received', damageR]])

'''f = open('debug.txt', 'w')
f.write(json.dumps([['damage_given', damageG], ['damage_received', damageR]], indent=4, separators=(',', ': ')))
f.close()'''