import csv
import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly.plotly as py

plotly.tools.set_credentials_file(username='stanislavL', api_key='g4vubtu1nr')


class User(object):
    id = 0
    firstName = ""
    lastName = ""
    email = ""

    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.days = []
        self.week = []
        self.weekConsumption = []

with open('resources/csv/customer_data.csv') as csvFile:
    userReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    users = []
    rowsFromFile = []
    started = True
    for row in userReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False

for row in rowsFromFile:
    columns = []
    [columns.append(x) for x in row.split(';')]
    newUser = User(columns[0], columns[1], columns[2], columns[3])
    users.append(newUser)

with open('resources/csv/smd_week1.csv') as csvFile:
    weekReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    rowsFromFile = []
    started = True
    for row in weekReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False
with open('resources/csv/smd_week2.csv') as csvFile:
    weekReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    started = True
    for row in weekReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False
with open('resources/csv/smd_week3.csv') as csvFile:
    weekReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    started = True
    for row in weekReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False
with open('resources/csv/smd_week4.csv') as csvFile:
    weekReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    started = True
    for row in weekReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False
with open('resources/csv/smd_week5.csv') as csvFile:
    weekReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    started = True
    for row in weekReader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False

allUsers = []

for row in rowsFromFile:
    columns = []
    [columns.append(x) for x in row.split(';')]

    newUser = User(columns[0],'','','')
    inOrNot = False
    sum = 0
    for i in range(1,len(columns)):
        #print(i, columns[i])
        if not ("NA" in columns[i]):
            sum += float(columns[i].replace(',', '.'))
    newUser.week.append(sum)
    for user in allUsers:
        if user.id == newUser.id:
            inOrNot = True
            user.week.append(sum)
    if not inOrNot:
        allUsers.append(newUser)

    for user in users:
        if columns[0] == '"' + user.id + '"':
            user.week.append(row)
            for day in range((len(user.week)-1)*7, len(user.week)*7):
                user.days.append([])
                dayOfTheWeek = day % 7
                for i in range(1+dayOfTheWeek*48, 49+dayOfTheWeek*48):
                    user.days[day].append(columns[i])

for user in users:
    print('id: ' + user.id)
    print('name: ' + user.firstName + ' ' + user.lastName)
    print('email: ' + user.email)
    user.consumptionOnOneDay = [0, 0, 0, 0, 0, 0]
    for i in range(0, 5):
        print("week: " + str(i+1) + " - " + str(user.week[i]))
    for i in range(28, 35):
        for t in range(0, len(user.days[i])):
            user.consumptionOnOneDay[t // 8] += float(user.days[i][t].replace(',', '.'))
    for i in range(0, 6):
        print("average consumption from " + str(i*4) + " to " + str(i*4+4) + " : " + str(user.consumptionOnOneDay[i]))

timeOfTheDay = ['0 to 4', '4 to 8', '8 to 12', '12 to 16', '16 to 20', '20 to 24']
weekNames = ['Week 21', 'Week 22', 'Week 23', 'Now']

for user in users:
    for userInAll in allUsers:
        if user.id in userInAll.id:
            for i in range(0, len(userInAll.week)):
                user.weekConsumption.append(userInAll.week[i])

for user in users:

    trace = Bar(x=[timeOfTheDay[0], timeOfTheDay[1], timeOfTheDay[2], timeOfTheDay[3], timeOfTheDay[4],
                   timeOfTheDay[5]], y=[user.consumptionOnOneDay[0], user.consumptionOnOneDay[1],
                                        user.consumptionOnOneDay[2], user.consumptionOnOneDay[3],
                                        user.consumptionOnOneDay[4], user.consumptionOnOneDay[5]])
    data = [trace]
    layout = Layout(title='Your average consumption in one day this week')
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, user.firstName + ' ' + user.lastName + ' average in a day.png')

    trace = Bar(x=[weekNames[0], weekNames[1], weekNames[2], weekNames[3]], y=[user.weekConsumption[0], user.weekConsumption[1],
                                        user.weekConsumption[2], user.weekConsumption[3]])
    data = [trace]
    layout = Layout(title='Comparison in week in energy consumption')
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, user.firstName + ' ' + user.lastName + ' average per week.png')
