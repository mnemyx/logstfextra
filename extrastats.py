#!/usr/bin/python

import argparse
import re
import json

' some global variables '
damageG = dict()
damageR = dict()
classes = dict()
inRound = False

' simple regex to find needed lines '
a = re.compile(".*triggered \"damage\" against.*")
b = re.compile(".*Round_Start.*")
c = re.compile(".*Round_Win.*")
d = re.compile(".*changed role to.*")

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

		player = temp[0].translate(None, ">").split("<")

		if player[0] in classes:
			classes[player[0]] = temp[1]
		else:
			classes.update({ player[0] : temp[1] })


	if a.match(l) and inRound:
		temp = l.split('"')[1::2]

		top = temp[0].translate(None, ">").split("<")
		bottom = temp[2].translate(None, ">").split("<")
		'top = temp[0].split("<")[1::2].split(">")[1::2]'
		'bottom = temp[2].split("<")[1::2].split(">")[1::2]'
		
		if top[0] in damageG:
			if bottom[0] in damageG[top[0]]['players']:
				damageG[top[0]]['players'][bottom[0]]['da'] += int(temp[3])
			else:
				damageG[top[0]]['players'].update({
					bottom[0] : {
						'da' : int(temp[3]),
						'pdata' : {
							'team' : bottom[3],
							'steamid' : bottom[2],
							'playernum' : bottom[1]
						}
					}
				})
		else:
			damageG.update({
				top[0] : {
					'players' : {
						bottom[0] : {
							'da' : int(temp[3]),
							'pdata' : {
								'team' : bottom[3],
								'steamid' : bottom[2],
								'playernum' : bottom[1]
							}
						}
					},
					'pdata' : {
						'team' : top[3],
						'steamid' : top[2],
						'playernum' : top[1]
					}
				}
			})


		if bottom[0] in damageR:
			if top[0] in damageR[bottom[0]]['players']:
				damageR[bottom[0]]['players'][top[0]]['da'] += int(temp[3])
			else:
				damageR[bottom[0]]['players'].update({
					top[0] : {
						'da' : int(temp[3]),
						'pdata' : {
							'team' : top[3],
							'steamid' : top[2],
							'playernum' : top[1]
						}
					}
				})
		else:
			damageR.update({
				bottom[0] : {
					'players' : {
						top[0] : {
							'da' : int(temp[3]),
							'pdata' : {
								'team' : top[3],
								'steamid' : top[2],
								'playernum' : top[1]
							}
						}
					},
					'pdata' : {
						'team' : bottom[3],
						'steamid' : bottom[2],
						'playernum' : bottom[1]
					}
				}
			})

' log the file to XML, to be parsed by PHP '
print json.dumps([['damage_given', damageG], ['damage_received', damageR]])

'''f = open('temp.txt', 'w')
f.write(json.dumps(['damage_given', damageG ]))
f.write(json.dumps(['damage_received', damageR ]))
f.close()'''