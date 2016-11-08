import os
import glob
import json

holeInserts = open("script_generated\\holeInserts.sql", 'w')



holeInserts.write("--Hole Inserts Generated by Eric's Python Script\n\n\n")

def readScoreCard(data, player_id):
	for i in range(0, len(data["scorecard"])):
		if(str(data["scorecard"][i]["total"]) == "0"): #players total score for the tournament is 0 -> they withdrew.
			holeInserts.write("--Player " + str(player_id) + " did not complete round " + str(i + i) + "\n")
			#holeInserts.write("update statistic set num_wd = num_wd + 1 where player_id = " + str(player_id) + ";\ncommit;\n")
			return
		
		for j in range(0, 18):
			score = data["scorecard"][i]["holes"][j]["strokes"]
			course_id = data["scorecard"][i]["course_id"]
			
			if(str(score) == ""):
				return
			
			if(str(course_id) == "800" or str(course_id) == ""): #handle corrupted data for tournament r047, 
				course_id = 538
			
			holeInserts.write('insert into player_hole_score values(' + str(player_id) + ',' + str(course_id) + ',' + str(j + 1) + ',' + str(i+1) + ',' + str(score) + ');\n')

def gatherField(field, tournament_id):
	file = open(field)
	data = json.load(file)
	
	num_players = len(data["players"])
	
	for i in range(0, num_players):
		player_id = data["players"][i]["pid"]
		fieldInserts.write("insert into field (player_id, tournament_id) values(" + str(player_id) + ",'" + str(tournament_id) + "');\n")

		
for dir in glob.glob('*/'):
	if(str(dir) != "script_generated\\"):
		tournament_id = dir.replace("\\", '')
		#gatherField(dir + "field.json", tournament_id)
		
		holeInserts.write("-- NEW TOURNAMENT\n\n\n")
		for subdir in glob.glob(dir + "scorecards"):
			for scorecard in glob.glob(subdir + '/*.json'): #*//scorecards/*.json
				with open(scorecard) as json_file:
					filename = scorecard.replace(subdir, '')
					filename = filename.replace("\\", '')
					filename = filename.replace('.json', '')
				
					data = json.load(json_file)
					player_id = str(filename)
					
					readScoreCard(data, player_id)
		holeInserts.write("-- END TOURNAMENT\n\n\n")
		
holeInserts.close()