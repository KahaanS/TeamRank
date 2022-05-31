import numpy as np
import math
import operator
from operator import itemgetter
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

    if data[2] == 'Middlesboro':
        data[2] = 'Middlesbrough'

    if data[3] == 'Middlesboro':
        data[3] = 'Middlesbrough'

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

teamlosses=dict()
for team in teams:
    teamlosses[team] = []

for match in matchdata:
    winner = [match[0],match[2]]
    teamlosses[match[1]].append(winner)

givedict=dict()
for team in teams:
    givedict[team] = dict()

for team in teams:
    total = 0
    for loss in teamlosses[team]:
        if loss[0] not in givedict[team].keys():
            givedict[team][loss[0]] = 0

        givedict[team][loss[0]] = givedict[team][loss[0]]+loss[1]
        total = total+loss[1]

    givedict[team]['Total'] = total

arrlist = []
for team in teams:
    teamlist = []
    teamdict = givedict[team]
    for team in teams:
        try:
            teamlist.append(teamdict[team]/teamdict['Total'])
        except:
            teamlist.append(0)
    arrlist.append(teamlist)

adjmat = np.matrix(arrlist)
adjmat = np.transpose(adjmat)

def pagerank(matrix, stopval):
    #Assert: matrix is a schocastic matrix, stopval is a float
    diff=stopval+1
    i=1
    n = matrix.shape[1]
    eigenv = np.random.rand(n,1) #Generating a random vector with n entries
    eigenv = eigenv/np.linalg.norm(eigenv,1) #Here we normalise it to make sure the entries add up to 1 i.e. it is a possible result
    #INV: i>=1, diff>stopval, eigenv_i = matrix x eigenv_i-1
    while diff>stopval:
        oldv = eigenv
        eigenv = matrix @ eigenv #numpy inbuilt matrix multiplication operator is '@'
        changev = oldv-eigenv
        diff = np.mean(np.absolute(changev)) #Again using numpy inbuilt operations to calculate the average change between 2 iterations
        print(i, diff) #Printing to see how fast it converges
        i=i+1
    #Assert: diff<= stopval, eigenv = eigenv_i
    return eigenv

ranks = pagerank(adjmat,math.pow(10,-20))
print('')
i=0
finaldict = dict()
for rank in ranks:
    finaldict[teams[i]] = rank.item(0)
    i=i+1

sort_dict= dict(sorted(finaldict.items(), key=operator.itemgetter(1), reverse=True))
for item,value in sort_dict.items():
    print(item,value)
