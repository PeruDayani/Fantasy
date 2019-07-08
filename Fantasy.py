#!/usr/bin/env python

import urllib.request
import pandas as pd
import time
import os
from bs4 import BeautifulSoup

team1 = []
team2 = []
GAMEOVER = False

def test(current_url):
	page = urllib.request.urlopen(current_url);	
	soup = BeautifulSoup(page, "html.parser");
	good_html = soup.prettify()
	print(" The URL is valid.")

def draft_players(current_url):

	global team1
	global team2

	page = urllib.request.urlopen(current_url);
	soup = BeautifulSoup(page, "html.parser");
	good_html = soup.prettify()

	all_names = []

	for row in soup.find_all("tr", class_=lambda x : x!='highlight'):
		
		cells = row.find_all('td', {'class' : ['name','pts','plusminus','reb','ast','3pt']} )
		len_cells = len(cells)

		if(len_cells != 6 or cells[0].text=="TEAM"):
			continue

		all_names.append(cells[0].find(text=True))
	
	print("Lets draft:")
	current_player = 1
	total_players = len(all_names)

	while(total_players>0):
		
		index = 0

		for name in all_names:
			print(str(index) + " : " + name)
			index += 1

		draft_pic = int(input("Player " + str(current_player) + " picks: "))
		total_players -= 1
		
		if (current_player == 1):
			current_player = 2
			team1.append(all_names[draft_pic])
		else :
			current_player = 1
			team2.append(all_names[draft_pic])

		print("Player picked: " + all_names.pop(draft_pic))
		print()
		print()

	print("Draft Complete")
	print()
	print()
	print("Player 1's Team: ")
	print(team1)
	print()
	print()
	print("Player 2's Team: ")
	print(team2)
	print()
	print()

	save_data = input("Save teams ? (y/n)")
	if (save_data == "y"):
		#team1.to_csv("Player1_team", sep='/t')
		df = pd.DataFrame(team1)
		df.to_csv('player1team.csv', index=False)
		#team2.to_csv("Player2_team", sep='/t')
		df = pd.DataFrame(team2)
		df.to_csv('player2team.csv', index=False)

	print()
	print()

def play_fantasy(current_url):

	global GAMEOVER
	global team1
	global team2

	page = urllib.request.urlopen(current_url);
	soup = BeautifulSoup(page, "html.parser");
	good_html = soup.prettify()

	team1_A =[]
	team1_B =[]
	team1_C =[]
	team1_D =[]
	team1_E =[]
	team1_F =[]

	team2_A =[]
	team2_B =[]
	team2_C =[]
	team2_D =[]
	team2_E =[]
	team2_F =[]

	i = 1;

	for row in soup.find_all("span", {'class' : ['game-time status-detail','status-detail']}):
		if row.text == "Final":
			GAMEOVER = True

	for row in soup.find_all("tr", class_=lambda x : x!='highlight'):
		
		cells = row.find_all('td', {'class' : ['name','pts','plusminus','reb','ast','3pt']} )
		len_cells = len(cells)

		if(len_cells != 6 or cells[0].text=="TEAM"):
			continue

		try:
			name = cells[0].find(text=True)

			if (name in team1):  
				
				team1_A.append(name)
				team1_B.append(int(cells[1].text[0]))
				team1_C.append(int(cells[2].text))
				team1_D.append(int(cells[3].text))
				team1_E.append(int(cells[4].text))
				team1_F.append(int(cells[5].text))

			elif (name in team2):

				team2_A.append(name)
				team2_B.append(int(cells[1].text[0]))
				team2_C.append(int(cells[2].text))
				team2_D.append(int(cells[3].text))
				team2_E.append(int(cells[4].text))
				team2_F.append(int(cells[5].text))
		except:
			print("Player " + name + " has not played yet.")
			continue

	team1_df=pd.DataFrame(team1_A,columns=['Name'])
	team1_df['3pt']=team1_B
	team1_df['reb']=team1_C
	team1_df['ast']=team1_D
	team1_df['plus/minus']=team1_E
	team1_df['pts']=team1_F

	team2_df=pd.DataFrame(team2_A,columns=['Name'])
	team2_df['3pt']=team2_B
	team2_df['reb']=team2_C
	team2_df['ast']=team2_D
	team2_df['plus/minus']=team2_E
	team2_df['pts']=team2_F

	print(team1_df)
	print()
	print()
	print(team2_df)
	print()
	print()

	team1_3pt = team1_df['3pt'].sum(axis=0)
	team1_reb = team1_df['reb'].sum(axis=0)
	team1_ast = team1_df['ast'].sum(axis=0)
	team1_pm = team1_df['plus/minus'].sum(axis=0)
	team1_points = team1_df['pts'].sum(axis=0)

	team2_3pt = team2_df['3pt'].sum(axis=0)
	team2_reb = team2_df['reb'].sum(axis=0)
	team2_ast = team2_df['ast'].sum(axis=0)
	team2_pm = team2_df['plus/minus'].sum(axis=0)
	team2_points = team2_df['pts'].sum(axis=0)

	player1_adv = 0
	if(team1_3pt > team2_3pt): player1_adv+=1
	if(team1_reb > team2_reb): player1_adv+=1
	if(team1_ast > team2_ast): player1_adv+=1
	if(team1_pm > team2_pm): player1_adv+=1
	if(team1_points > team2_points): player1_adv+=1

	results = pd.DataFrame(['team1', 'team2'],columns=['Name'])
	results['3pt']=[team1_3pt, team2_3pt]
	results['reb']=[team1_reb, team2_reb]
	results['ast']=[team1_ast, team2_ast]
	results['plus/minus']=[team1_pm, team2_pm]
	results['pts']=[team1_points,team2_points]
	print(results)
	print()
	print()

	if(GAMEOVER):
		
		if(player1_adv > 3):
			print("Player 1 wins!")
		else:
			print("Player 2 wins!")

		print()
		print()
		print("Thank you for playing")

	else:
		
		if(player1_adv > 3):
			print("Player 1 is in the lead")
		else:
			print("Player 2 is in the lead")

		print()
		print()

		time.sleep(30)
		
		play_fantasy(current_url)

def main():
	
	global team1
	global team2
	
	current_url_boxscore = input("Input URL: ")
	
	read_team1 = input("Upload saved teams ? (y/n)")

	if (read_team1 == "y"):

		team1_path = input("Team 1 path: ")
		team2_path = input("Team 2 path: ")
	
		team1 = pd.read_csv(team1_path, sep='/t', header = None, index_col=False, engine='python')
		team1 = team1.values.flatten()
		team2 = pd.read_csv(team2_path, sep='/t', header = None, index_col=False, engine='python')
		team2 = team2.values.flatten()

		print("Player 1's Team: ")
		print(team1)
		print()
		print()
		print("Player 2's Team: ")
		print(team2)
		print()
		print()

		play_fantasy(current_url_boxscore)

	else:

		draft_players(current_url_boxscore)
		play_fantasy(current_url_boxscore)




if __name__ == '__main__':
    main()
