import csv
import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import * #Scatter, Bar, Figure, Layout
import plotly.graph_objs as go
import plotly.plotly as py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

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

#############################################   TABLES READING PART   #################################################

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

#############################################   DATA SAVING INTO OBJECTS PART  #################################################

for row in rowsFromFile:
    columns = []
    [columns.append(x) for x in row.split(';')]

    newUser = User(columns[0],'','','')
    inOrNot = False
    sum = 0
    for i in range(1,len(columns)):
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
    # for i in range(0, 5):
    #     print("week: " + str(i+1) + " - " + str(user.week[i]))
    for i in range(28, 35):
        for t in range(0, len(user.days[i])):
            user.consumptionOnOneDay[t // 8] += float(user.days[i][t].replace(',', '.')) * 0.15
    # for i in range(0, 6):
    #     print("average consumption from " + str(i*4) + " to " + str(i*4+4) + " : " + str(user.consumptionOnOneDay[i]))

timeOfTheDay = ['0 to 4', '4 to 8', '8 to 12', '12 to 16', '16 to 20', '20 to 24']
weekNames = ['Week 20', 'Week 21', 'Week 22', 'Week 23', 'Now']

for user in users:
    for userInAll in allUsers:
        if user.id in userInAll.id:
            for i in range(0, len(userInAll.week)):
                user.weekConsumption.append(float(userInAll.week[i]) * 0.15)

#############################################   CALCULATION PART   #################################################

averageConsumptionPerWeek = []
bestConsumptionPerWeek = []

for week in range(0, 5):
    sumPerWeek = 0
    bestPerWeek = 0
    weekConsumptions = []
    for user in allUsers:
        sumPerWeek += user.week[week]
        if user.week[week]>0:
            weekConsumptions.append(user.week[week])
    averageConsumptionPerWeek.append(sumPerWeek/len(allUsers) * 0.15)
    weekConsumptions = sorted(weekConsumptions)
    for i in range(0, 10):
        bestPerWeek += weekConsumptions[i]
    bestConsumptionPerWeek.append(bestPerWeek/10 * 0.15)

#############################################   GRAPH DRAWING PART   #################################################

for user in users:
    trace = Bar(x=[timeOfTheDay[0], timeOfTheDay[1], timeOfTheDay[2], timeOfTheDay[3], timeOfTheDay[4],
                   timeOfTheDay[5]], y=[user.consumptionOnOneDay[0], user.consumptionOnOneDay[1],
                                        user.consumptionOnOneDay[2], user.consumptionOnOneDay[3],
                                        user.consumptionOnOneDay[4], user.consumptionOnOneDay[5]])
    data = [trace]
    layout = Layout(title='Energy consumption')
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, 'resources/img/' + user.firstName + ' ' + user.lastName + ' average in a day.png')

    userGraph = go.Scatter(
        x=weekNames,
        y=user.weekConsumption,
        mode='lines+markers',
        name='You'
    )

    averageGraph = go.Scatter(
        x=weekNames,
        y=averageConsumptionPerWeek,
        mode='lines+markers',
        name='Average'
    )

    bestGraph = go.Scatter(
        x=weekNames,
        y=bestConsumptionPerWeek,
        mode='lines+markers',
        name='Best 10%'
    )

    data = [userGraph, averageGraph, bestGraph]
    layout = Layout(title='Comparison in week in energy consumption')
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, 'resources/img/' + user.firstName + ' ' + user.lastName + ' average per week.png')

#############################################   EMAIL GENERATING PART  #################################################

user1 = users[0]
for user in users:

    msg = MIMEMultipart()
    msg["To"] = user.email
    msg["From"] = 'info@regnitzutilities.de'
    msg["Subject"] = 'Weekly energy consumption report'


    html = """\
    <html>
      <head></head>
      <body>
    <div style="font-size: 150%">
        <div style="float: right; margin-right: 3%">
             <img src="cid:regnitzLogo" style="height: 120px">
        </div>
        <div style="padding: 15px; border: 1px solid black; width: 200px; float: left">
            <b> """ + user.firstName + ' ' + user.lastName + """</b>
            <div> Customer ID: """ + user.id + """</div>
        </div>

        <div style="clear: both; margin-top: 30px; padding: 10px; border: 1px solid black; width: 95%">
            <div> Dear Customer,</div>
            <div> please find your consumption report for week 24</div>
        </div>

        <div style="margin-top: 10px; padding: 10px; border: 1px solid black; width: 95%; background-color: lightgrey">
            <b> How does your energy consumption change over time?</b>
        </div>

        <div style="margin-top: 10px; padding-right: 10px; border: 1px solid black; width: 250px; font-size: 90%; float: left">
            <ul>
                <li> You spent """ + "{:.2f}".format(user.weekConsumption[4]) + """€ this week. It is more than the week before. The rise costs you """ + "{:.2f}".format(user.weekConsumption[4] - user.weekConsumption[3]) + """ more euro.</li>
                <li style="margin-top:10px"> You are still below the average. But """ + "{:.2f}".format(user.weekConsumption[4] - bestConsumptionPerWeek[4]) + """€ separate you from the 10% of the customers that consume the less.</li>
                <li style="margin-top:10px"> The increase since the week 20 represents """ + "{:.2f}".format(user.weekConsumption[4] - user.weekConsumption[0]) + """€</li>
            </ul>
            <div>
                <img src="cid:rainingCloud" style="margin-left:30px; width: 50px">
                <img src="cid:greyCloud" style="width: 50px">
                <img src="cid:sun" style="width: 50px">
            </div>
        </div>

        <div style="float:right; z-index:-1">
             <img src="cid:week" style="width: 600px">
        </div>

        <div style="margin-top: 10px; clear: both; padding: 10px; border: 1px solid black; width: 95%; background-color: lightgrey">
            <b> Your average consumption in one day this week</b>
        </div>

        <div style="position: absolute; left: 0px; top: 500px; z-index: -1">
             <img src="cid:day" style="width: 100%">
        </div>

        <div style="margin-left: 50px; padding:10px; margin-top: 0px; border: 1px solid black; width: 80%; font-size: 90%; height: 220px">
            <div style="float: left; width: 50%">
                <b> How can you reduce your consumption?</b>
                <ul>
                    <li> Use energy-saving light bulbs</li>
                    <li> Be careful about the standby of your electric devices</li>
                    <li> Take shower rather than take a bath. This way you will consume on average 70% less hot water.</li>
                </ul>
            </div>
            <div style="float:right">
                <img src="cid:lightBulb" style="height: 200px">
            </div>
        </div>

        <div style="clear: both; margin-top: 20px; margin-left: 170px; font-size: 80%">
            <em> Report realized in collaboration with People are Power</em>
        </div>

        <div style="margin-top: 2px; margin-left: 310px">
            <img src="cid:pap" style="height: 90px">
        </div>

        <div style="margin-top: 0px; margin-left: 110px; font-size: 65%">
            <em> If you wish to stop receiving our emails or change your subscription options, please <a href="http://www.google.de">click here</a>.</em>
        </div>

    </div>
    </body>
    </html>
    """


    def addImage (fileName, imageID):
        fp = open(fileName, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', imageID)
        msg.attach(img)

    addImage('resources/img/regnitzLogo.png', '<regnitzLogo>')
    addImage('resources/img/rainingCloud.png', '<rainingCloud>')
    addImage('resources/img/greyCloud.png', '<greyCloud>')
    addImage('resources/img/sun.png', '<sun>')
    addImage('resources/img/' + user.firstName + ' ' + user.lastName + ' average per week.png', '<week>')
    addImage('resources/img/' + user.firstName + ' ' + user.lastName + ' average in a day.png', '<day>')
    addImage('resources/img/lightBulb.jpg', '<lightBulb>')
    addImage('resources/img/PAPLogo.png', '<pap>')

    #part1 = MIMEText(body, 'plain')
    part2 = MIMEText(html, 'html')

    #msg.attach(part1)
    msg.attach(part2)

    #server = smtplib.SMTP('smtp.gmail.com:587')
    server = smtplib.SMTP('mail.uni-bamberg.de')
    server.starttls()
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
    server.quit()