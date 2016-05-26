import csv


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
    newUser = User(columns[0],columns[1],columns[2],columns[3])
    users.append(newUser)
for user in users:
    print('id: ' + user.id)
    print('name: ' + user.firstName + ' ' + user.lastName)
    print('email: ' + user.email)
with open('resources/csv/smd_week1.csv') as csvFile:
    week1Reader = csv.reader(csvFile, delimiter=' ', quotechar='|')
    week1Data = []
    rowsFromFile = []
    started = True
    for row in week1Reader:
        if not started:
            rowsFromFile.append(row[0])
        else:
            started = False
    #print(rowsFromFile)
for row in rowsFromFile:
    columns = []
    [columns.append(x) for x in row.split(';')]
    for user in users:
        if columns[0] == '"' + user.id + '"':
            user.days = []
            user.week1 = row
            print(row)
            for day in range(0,7):
                user.days.append([])
                for i in range(1+day*48,48+day*48):
                    user.days[day].append(columns[i])
                print(user.days[day])