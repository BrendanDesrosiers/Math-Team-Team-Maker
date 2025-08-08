from itertools import combinations
from players import *

# call the function to read players from csv
players = read_players_from_csv('data.csv')

class Round:
    def __init__(self, players, roundNumber):
        self.players = players
        self.roundNumber = roundNumber
        self.expectedScore = sum(player.expectedScores[roundNumber-1] for player in players)

    def __str__(self):
        return f"Round(number={self.roundNumber}, expectedScore={self.expectedScore}, players={self.players})"
    
    def __repr__(self):
        return f"Round(number={self.roundNumber}, expectedScore={self.expectedScore}, players={self.players})"

class Team:
    def __init__(self, players):
        self.players = players
        self.expectedScore = None
        self.rounds = []

    def isAllowed(self):
        # check if team has at most 2 seniors and at least 1 underclassman
        numSeniors = 0
        numUnderclassmen = 0
        for player in self.players:
            if player.year == 4:
                numSeniors += 1
            elif player.year < 3:
                numUnderclassmen += 1
        return numSeniors <= 2 and numUnderclassmen >= 1
    
    def findBestCombo(self):
        # map players to rounds
        # a player must participate in three rounds
        # each round must have three players
        
        # generate all possible combinations of players for rounds
        playerCombos = list(combinations(self.players, 3))
        
        # generate all possible combinations of combinations of players for the team
        roundCombos = list(combinations(playerCombos, 5))
        
        # filter out invalid round combinations
        i = 0
        while i < (len(roundCombos)):
            if not self.roundComboAllowed(roundCombos[i]):
                roundCombos.pop(i)
                i -= 1
            i += 1
        # create list of Round objects for each valid round combination
        possibleCombos = []
        for combo in roundCombos:
            foo = [Round(list(roundPlayers), roundNumber+1) for roundNumber, roundPlayers in enumerate(combo)]
            possibleCombos.append(foo)

        # calculate expected score for each valid round combination and return maximum
        bestOption = None
        bestScore = -1
        for combo in possibleCombos:
            score = sum(round.expectedScore for round in combo)
            if score > bestScore:
                bestScore = score
                bestOption = combo
        return bestOption, bestScore

    def roundComboAllowed(self, combo):
        # check that each player plays exactly 3 rounds
        playersInRounds = [player for round in combo for player in round]
        for player in playersInRounds:
            # if the number of times a player appears in rounds is not 3, return false
            if playersInRounds.count(player) != 3:
                return False
        return True

    def __str__(self):
        return f"Team(expectedScore={self.expectedScore}, players={self.players})"

def findBestTeam(players):
    bestTeam = None
    bestScore = -1
    # generate all combinations of players for the team
    for combo in combinations(players, 5):
        # create a Team object for each combination
        team = Team(list(combo))
        # check if the team is allowed and if so, find the best combination of rounds
        if team.isAllowed():
            rounds, score = team.findBestCombo()
            # if the score is better than the best score, update the best team to be this one with this combination of rounds
            team.expectedScore = score
            if score > bestScore:
                bestScore = score
                bestTeam = team
                bestTeam.rounds = rounds
    # return the best team and its expected score
    return bestTeam

# let the user know what the program is doing
print("Finding best team...")
# call the function to find the best team
bestTeam = findBestTeam(players)
# let the user know what the best team is
print(f"The best team is {bestTeam.players} with expected score {bestTeam.expectedScore}")
# print the rounds for the best team
print("Rounds:")
for round in bestTeam.rounds:
    print(round)