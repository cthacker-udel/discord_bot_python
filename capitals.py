import random
state_to_capital_dictionary = {"Alabama": "Montgomery", "Alaska": "Juneau", "Arizona" : "Phoenix", "Arkansas" : "Little Rock", "California" : "Sacramento", "Colorado": "Denver", "Connecticut": "Hartford", "Delaware": "Dover", "Florida": "Tallahassee", "Georgia": "Atlanta", "Hawaii": "Honolulu", "Idaho": "Boise", "Illinois": "Springfield", "Indiana": "Indianapolis", "Iowa": "Des Moines", "Kansas": "Topeka", "Kentucky": "Frankfort", "Louisiana": "Baton Rouge", "Maine": "Augusta", "Maryland": "Annapolis", "Massachusetts": "Boston", "Michigan": "Lansing", "Minnesota": "St.Paul", "Mississippi": "Jackson", "Missouri": "Jefferson City","Montana": "Helena", "National(U.S.)": "Washington D.C", "Nebraska": "Lincoln", "Nevada": "Carson City", "New Hampshire": "Concord", "New Jersey": "Trenton", "New Mexico": "Santa Fe", "New York": "Albany", "North Carolina": "Raleigh", "North Dakota": "Bismarck", "Ohio": "Columbus", "Oklahoma": "Oklahoma City", "Oregon": "Salem", "Pennsylvania": "Harrisburg", "Rhode Island": "Providence", "South Carolina": "Columbia", "South Dakota": "Pierre", "Tennessee": "Nashville", "Texas": "Austin","Utah": "Salt Lake City", "Vermont": "Montpelier", "Virginia": "Richmond", "Washington": "Olympia", "West Virginia": "Charleston", "Wisconsin": "Madison", "Wyoming": "Cheyenne"}
states = [x for x in state_to_capital_dictionary.keys()]
capitals = [x for x in state_to_capital_dictionary.values()]
capital_to_state_dictionary = {}
for i in range(len(capitals)):
    capital_to_state_dictionary[capitals[i]] = states[i]


def get_random_state(states_list):
    return random.choice(states)

def get_random_capital(capitals_list):
    return random.choice(capitals)


if __name__ == '__main__':
    get_random_state(states)