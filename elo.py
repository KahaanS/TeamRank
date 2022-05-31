import math
file_name = 'EPL_set.csv'

matchdata=[]
teams=[]

text = open(file_name).read()
for line in text.split('\n'):
    match = []
    data = line.split(',')

    if len(data)<2:
        continue
    if data[1] == 'date':
        continue

    if data[2] not in teams:
        teams.append(data[2])

    if int(data[4])>int(data[5]):
        match.append(data[2])
        match.append(data[3])
        match.append(int(data[4])-int(data[5]))
        matchdata.append(match)
    elif int(data[5])>int(data[4]):
        match.append(data[3])
        match.append(data[2])
        match.append(int(data[5])-int(data[4]))
        matchdata.append(match)
    else:
        match.append(data[2])
        match.append(data[3])
        match.append(0.5)
        matchdata.append(match)

        match=[]
        match.append(data[3])
        match.append(data[2])
        match.append(0.5)
        matchdata.append(match)

teams = sorted(teams)
print('Teams',len(teams))
print('Matches',len(matchdata))

def Probability(r1,r2):
    return 1.0*1.0/(1 + 1.0*math.pow(10,1.0*(r1-r2)/400))

def EloChange(team1,team2,rating_dict):
    k=10
    p_t1 = Probability(rating_dict[team1],rating_dict[team2])
    p_t2 = Probability(rating_dict[team2],rating_dict[team1])

    rating_dict[team1] = rating_dict[team1]+k*(1-p_t1)
    rating_dict[team2] = rating_dict[team2]+k*(0-p_t2)

ratings = dict()
for team in teams:
    ratings[team] = 1500

for match in matchdata:
    EloChange(match[0],match[1],ratings)

print(sorted(ratings.items(), key=lambda x: x[1], reverse=True))
