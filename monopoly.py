# Import modules
import random
import sys
import math

# Simulate a player rolling dice
def roll():
    return random.randint(1, 6)

# Display progress bar
def progress(complete, total):
    bar = math.floor((complete / total) * 25)
    sys.stdout.write('\r[' + ('#' * bar) + ('-' * (25 - bar)) + '] ' + str(round((complete / total) * 100)) + '%' + ' complete')

# Simulate a player
def simulate():
    # Init counting variable for number of stops per tile and number of rounds
    stops = [0] * 40
    rounds = 0

    # Init current variables for stop, doubles and jail
    currentStop = 0
    doubles = 0
    jail = False

    # Player turns
    while True:
        # Roll the dice
        dice1 = roll()
        dice2 = roll()

        # Check for jail
        if not jail and dice1 == dice2:
            if doubles >= 2:
                jail = True
                currentStop = 10
            else:
                doubles += 1

                # Increment currentStop
                currentStop += dice1 + dice2
        elif currentStop == 30:
                jail = True
                currentStop = 10
        else:
            doubles = 0
            jail = False

            # Increment currentStop
            currentStop += dice1 + dice2
        
        # Increment round count when passing go
        if currentStop >= 40:
            currentStop -= 40
            rounds += 1
        
        # Increment stop count when landing on it
        stops[currentStop] += 1

        # Terminate on go
        if currentStop == 0:
            return {
                "stops": stops,
                "rounds": rounds
            }

# Store all stops
stopLists = []
totalStops = [0] * 40

# Store round count
totalRounds = 0

iterations = int(sys.argv[1]) if int(sys.argv[1]) else 1000

for i in range(iterations):
    results = simulate()
    stopLists.append(results["stops"])
    totalRounds += results["rounds"]
    progress(i + 1, iterations)

# Combine all stopCounts
for i in stopLists:
    for j in range(40):
        totalStops[j] += i[j]

# Find float chance to land
stopChance = [round(x * 100 / sum(totalStops), 2) for x in totalStops]

if __name__ == "__main__":
    print('\nRounds: ' + str(totalRounds))
    print('Percentage Chance Per Square: ' + str(stopChance))