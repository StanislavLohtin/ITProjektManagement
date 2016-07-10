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
import random

# Use this for plotly further features plotly.tools.set_credentials_file(username='stanislavL', api_key='g4vubtu1nr')

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
    for i in range(28, 35):
        for t in range(0, len(user.days[i])):
            user.consumptionOnOneDay[t // 8] += float(user.days[i][t].replace(',', '.')) * 0.15

timeOfTheDay = ['0:00 to 4:00', '4:00 to 8:00', '8:00 to 12:00', '12:00 to 16:00', '16:00 to 20:00', '20:00 to 24:00']
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
    userCount = 0
    weekConsumptions = []
    for user in allUsers:
        sumPerWeek += user.week[week]
        if user.week[week]>0:
            weekConsumptions.append(user.week[week])
            userCount += 1
    averageConsumptionPerWeek.append(sumPerWeek/userCount * 0.15)
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
    layout = Layout(title='Energy consumption', yaxis=dict(title='€'))
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, 'resources/img/' + user.id + ' ' + user.firstName + ' ' + user.lastName + ' average in a day.png')

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
    layout = Layout(title='Comparison in week in energy consumption', yaxis=dict(title='€'))
    fig = Figure(data=data, layout=layout)

    py.image.save_as(fig, 'resources/img/' + user.id + ' ' + user.firstName + ' ' + user.lastName + ' average per week.png')

#############################################   EMAIL GENERATING PART  #################################################

tips = ['What about new appliance which use less energy? E.g. smart washing machine which starts automatically (during the night).',
        'Do everything important during the day. Your light bulbs will use less energy during evenings.',
        'Use the exact amount of water that you need during the kettle heating.',
        'What about using energy-saving light bulbs?',
        'Be careful about the standby of your electric devices.',
        'Try to take shower than take a bath next time. Did you know that you will consume on average <span style="color:red">70% LESS</span> hot water?']

user1 = users[0]
for user in users:
    randomTips = []
    while True:
        tip = random.choice(tips)
        if tip not in randomTips:
            randomTips.append(tip)
        if len(randomTips) == 3:
            break
    biggestConsumption = 0
    lowestConsumption = user.consumptionOnOneDay[0]
    lowestConsumptionText = timeOfTheDay[0]
    biggestConsumptionText = timeOfTheDay[4]
    for i in range(0,6):
        if biggestConsumption < user.consumptionOnOneDay[i]:
            biggestConsumption = user.consumptionOnOneDay[i]
            biggestConsumptionText = timeOfTheDay[i]
        if lowestConsumption > user.consumptionOnOneDay[i]:
            lowestConsumption = user.consumptionOnOneDay[i]
            lowestConsumptionText = timeOfTheDay[i]
    msg = MIMEMultipart()
    msg["To"] = user.email
    msg["From"] = 'info@regnitz-utilities.de'
    msg["Subject"] = 'Weekly energy consumption report'

    html = """
    <html>
      <head></head>
      <body>
    <div style="font-size: 150%">
        <div style="float: right; margin-right: 8%">
             <img src="cid:regnitzLogo" style="height: 150px">
        </div>
        <div style="padding: 15px; border: 1px solid black; width: 20%; float: left">
            <b> """ + user.firstName + ' ' + user.lastName + """</b>
            <div> Customer ID: """ + user.id + """</div>
        </div>

        <div style="clear: both; margin-top: 30px; padding: 10px; border: 1px solid black; width: 90%">
            <div> Dear """ + user.firstName + """, </div>
            <div> We are here with your weekly report! How was your energy consumption for this week?</div>
            <div> Here we go!</div>
        </div>

        <div style="margin-top: 10px; padding: 10px; border: 1px solid black; width: 90%; background-color: lightgrey">
            <b> How does your energy consumption change over time?</b>
        </div>

        <div style="margin-top: 10px; padding: 10px; border: 1px solid black; width: 90%; font-size: 90%;">
            <ul>
                <li> You spent <span style="color:red">""" + "{:.1f}".format(user.weekConsumption[4]) + """€</span> this week. """

    differenceLastWeek = user.weekConsumption[4] - user.weekConsumption[3]
    weatherIconFileName = ""
    if differenceLastWeek <= -0.5:
        html += """It is less than the week before. You saved this week <span style="color:red">""" + "{:.1f}".format(-differenceLastWeek) + """€</span>.</li>"""
        weatherIconFileName = 'resources/img/sunActive.png'
    if (-0.5 < differenceLastWeek) & (differenceLastWeek <= 0.5):
        html += """It is the same as the week before. </li>"""
        weatherIconFileName = 'resources/img/cloudActive.png'
    if differenceLastWeek > 0.5:
        html += """It is more than the week before. The rise costs you <span style="color:red">""" + "{:.1f}".format(differenceLastWeek) + """€</span> more.</li>"""
        weatherIconFileName = 'resources/img/rainyCloudActive.png'

    differenceToAverage = user.weekConsumption[4] - averageConsumptionPerWeek[4]
    if differenceToAverage <= -0.5:
        if differenceLastWeek > 0.5:
            html += """<li>BUT! You are still below the average. And <span style="color:red">""" + "{:.1f}".format(user.weekConsumption[4] - bestConsumptionPerWeek[4]) + """€</span> separate you from the BEST 10% of consumers.</li>"""
        else:
            html += """<li>You are still below the average. And <span style="color:red">""" + "{:.1f}".format(user.weekConsumption[4] - bestConsumptionPerWeek[4]) + """€</span> separate you from the BEST 10% of consumers.</li>"""
    if (-0.5 < differenceToAverage) & (differenceToAverage <= 0.5):
        html += """<li>Your consumption is on average level. </li>"""
    if differenceToAverage > 0.5:
        html += """<li>You are above average. You spend <span style="color:red">""" + "{:.1f}".format(differenceToAverage) + """€</span> more than other consumers.</li>"""

    differenceToWeek20 = user.weekConsumption[4] - user.weekConsumption[0]
    if differenceToWeek20 <= -0.5:
        html += """<li>The decrease since the week 20 represents <span style="color:red">""" + "{:.1f}".format(-differenceToWeek20) + """€</span>. That is what you saved! Well done!</li>"""
    if (-0.5 < differenceToWeek20) & (differenceToWeek20 <= 0.5):
        html += """<li>Your consumption is on the same level as during the week 20. </li>"""
    if differenceToWeek20 > 0.5:
        html += """<li>The increase since the week 20 represents <span style="color:red">""" + "{:.1f}".format(differenceToWeek20) + """€</span>.</li>"""

    html += """
            </ul>
            <div>
                <img src="cid:weatherIcon" style="margin-left:500px; width: 50px">
            </div>
        </div>

        <div style=" z-index:-1">
             <img src="cid:week" style="width: 90%">
        </div>

        <div style="clear: both; padding: 10px; border: 1px solid black; width: 90%; background-color: lightgrey">
            <b> Your average consumption in one day this week</b>
        </div>

        <div style="position: absolute; left: 0px; top: 500px; z-index: -1">
             <img src="cid:day" style="width: 100%">
        </div>

        <div style="clear: both; padding: 10px; border: 1px solid black; width: 90%">
            <ul>
                <li> From """ + biggestConsumptionText + """ your consumption was the biggest. </li>
                <li> You can try to consume less energy during this time and start using it from """ + lowestConsumptionText + """ because energy is cheaper in this time period.</li>
            </ul>
        </div>

        <div style="padding:10px; margin-top: 30px; border: 1px solid black; width: 90%; font-size: 90%; height: 220px">
            <div style="float: left; width: 70%">
                <b> Are you curious how you can reduce your consumption?</b>
                <ul>
                    <li> """ + randomTips[0] + """ </li>
                    <li> """ + randomTips[1] + """ </li>
                    <li> """ + randomTips[2] + """ </li>
                </ul>
            </div>
            <div style="float:right">
                <img src="cid:lightBulb" style="height: 200px">
            </div>
        </div>

        <div style="clear: both; margin-top: 30px; padding: 10px; border: 1px solid black; width: 90%">
            <div> For more information, follow these links <a href="google.de">www.regnitz-utilities.de</a>
                <img src="cid:facebook" style="margin-left: 10px">
                <img src="cid:twitter" style="margin-left: 10px">
                <img src="cid:yt" style="margin-left: 10px">
                <img src="cid:in" style="margin-left: 10px">
            </div>
        </div>

        <div style="clear: both; margin-top: 30px; padding: 10px; border: 1px solid black; width: 90%">
            <div style="margin-left:200px"> Thank you for participating in this program!</div>
            <div> We appreciate that you think of spending less energy. You save your money but you also save our planet! Together we can build a better place to live. Because <a href="google.de">People are Power</a>. </div>
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
    addImage(weatherIconFileName, '<weatherIcon>')
    addImage('resources/img/' + user.id + ' ' + user.firstName + ' ' + user.lastName + ' average per week.png', '<week>')
    addImage('resources/img/' + user.id + ' ' + user.firstName + ' ' + user.lastName + ' average in a day.png', '<day>')
    addImage('resources/img/greenbulb.png', '<lightBulb>')
    addImage('resources/img/PAPLogo.png', '<pap>')
    addImage('resources/img/in.png', '<in>')
    addImage('resources/img/twitter.png', '<twitter>')
    addImage('resources/img/yt.png', '<yt>')
    addImage('resources/img/facebook.png', '<facebook>')

    #############################################   EMAIL SENDING PART  #################################################

    emailText = MIMEText(html, 'html')

    msg.attach(emailText)

    # Use server = smtplib.SMTP('smtp.gmail.com:587') to connect to gmail server
    server = smtplib.SMTP('mail.uni-bamberg.de')
    server.starttls()
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
    server.quit()