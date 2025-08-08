import csv

class Player:
    def __init__(self, name, expectedScores, year):
        self.name = name
        self.expectedScores = expectedScores
        self.year = year
        self.readableYear = "freshman" if year == 1 else "sophomore" if year == 2 else "junior" if year == 3 else "senior"
    
    def __str__(self):
        return f"{self.name} ({self.expectedScores}, {self.readableYear})"
    
    def __repr__(self):
        return self.name

# import csv from data.csv file
def read_players_from_csv(file_path):
    with open(file_path, mode='r') as file:
        players = []
        reader = csv.reader(file)
        for row in reader:
            # row is empty or a comment, skip it
            if not row:
                continue
            if row[0].startswith('#'):
                continue

            # parse the row
            name = row[0]
            expected_scores = list(map(float, row[1:6]))
            year = int(row[6])
            players.append(Player(name, expected_scores, year))
    return players

# playerList = read_players_from_csv('data.csv')