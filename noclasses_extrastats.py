#!/usr/bin/python

import argparse
import re
import json

' function to parse through array of lines '
def placeInDict(mainPlayer, otherPlayer, damageNum, damageDict):
	if mainPlayer[0] in damageDict:
		if otherPlayer[0] in damageDict[mainPlayer[0]]['players']:
			damageDict[mainPlayer[0]]['players'][otherPlayer[0]]['da'] += damageNum
		else:
			damageDict[mainPlayer[0]]['players'].update({
					otherPlayer[0] : {
						'da' : damageNum,
						'pdata' : {
							'team' : otherPlayer[3],
							'steamid' : otherPlayer[2],
							'playernum' : otherPlayer[1]
						}
					}
				})
	else:
		damageDict.update({
			mainPlayer[0] : {
				'players' : {
					otherPlayer[0] : {
						'da' : damageNum,
						'pdata' : {
							'team' : otherPlayer[3],
							'steamid' : otherPlayer[2],
							'playernum' : otherPlayer[1]
						}
					}
				},
				'pdata' : {
					'team' : mainPlayer[3],
					'steamid' : mainPlayer[2],
					'playernum' : mainPlayer[1]
				}
			}
		})


' some variables '
damageG = dict()
damageR = dict()
inRound = False

' simple regex to find needed lines '
a = re.compile(".*triggered \"damage\" against.*")
b = re.compile(".*Round_Start.*")
c = re.compile(".*Round_Win.*")

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

	if a.match(l) and inRound:
		temp = l.split('"')[1::2]

		top = temp[0].translate(None, ">").split("<")
		bottom = temp[2].translate(None, ">").split("<")
		
		placeInDict(top, bottom, int(temp[3]), damageG)
		placeInDict(bottom, top, int(temp[3]), damageR)

' sorting by value '
' for play in damageG: '



' log the file to XML, to be parsed by PHP '
print json.dumps([['damage_given', damageG], ['damage_received', damageR]])

'''f = open('temp.txt', 'w')
f.write(json.dumps(['damage_given', damageG ]))
f.write(json.dumps(['damage_received', damageR ]))
f.close()'''