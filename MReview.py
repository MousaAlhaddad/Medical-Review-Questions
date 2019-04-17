import pandas as pd
import numpy as np
import os

file = 'Clinical Questions.csv'

def importDataFrame(file):
    if file.split('.')[1] == 'csv':
        return pd.read_csv(file,parse_dates=['Date'])
    else:
        return pd.ExcelFile(file).parse(0,parse_dates=['Date'])

def sliceQuestions(frame, Exclude = [], Specialty= 'All', Diagnosis = 'All',
                    Emergency = 'All', Pharmacology = 'All'):
    # Date = 'All' 
    if Specialty != 'All': 
        frame = frame[frame.Specialty.isin(Specialty.split(','))]
    if Diagnosis != 'All':
        frame = frame[frame.Diagnosis.isin(Specialty.split(','))]
    if Emergency != 'All':
        if Emergency == True: 
            frame = frame[frame.Emergency == 'Yes']
        elif Emergency == False:
            frame = frame[frame.Emergency != 'Yes']
    if Pharmacology != 'All':
        if Pharmacology == True: 
            frame = frame[frame.Pharmacology == 'Yes']
        elif Pharmacology == False:
            frame = frame[frame.Pharmacology != 'Yes']
    
    questions = [x for x in list(frame.index) if x not in Exclude]    
    return (questions)
     
def descriptiveStatistics(frame):
    print('Our database has {} questions.'.format(len(frame)))
    print('The questions cover {} different specialties.'.format(len(frame.Specialty.value_counts())),end='\n\n')
    print('Here are the numbers of questions of the top ten specialties:')
    for x in frame.Specialty.value_counts()[0:10].index:
        print ("    ",x,": ",frame.Specialty.value_counts().loc[x], 
               " ({} Emergency".format(len(frame[(frame.Specialty==x)&(frame.Emergency=='Yes')])),
               " and {} Pharmacology)".format(len(frame[(frame.Specialty==x)&(frame.Pharmacology=='Yes')])), sep='')
    print('\nThe questions were collected over {} days between {} and {}.'.format((frame.Date.iloc[-1]-frame.Date.iloc[0]).days+1,
                                frame.Date.iloc[0].strftime('%Y-%m-%d'),frame.Date.iloc[-1].strftime('%Y-%m-%d')))

def text(df):
    Text="Questions:\n"
    for x in df.index:
        Text += str(x) + ". " + df.Question.loc[x] + "\n"

    Text += "\nAnswers:"
    for x in df.index:
        Text += "\n" + str(x) + "\n" + df.Answer.loc[x]+'\n'
    return Text

# Initialization
df = importDataFrame(file)
Solved=[]
Emergency = sliceQuestions(df, Emergency = True)

# Running this part will get you a new set of questions containing 3 Emergency, 2 Oncology and 5 Medicine questions each time
if 'Solved.txt' in os.listdir(): 
    with open('Solved.txt','r') as Input:
        Solved = [int(x) for x in Input.read().split('\n')[:-1]]
Oncology = sliceQuestions(df, Specialty= 'Oncology,Hematology,Stem Cells,Pathology', Emergency=False, Exclude=Solved)
Medicine = sliceQuestions(df, Specialty= 'Cardiology,Pulmonology,Intensive Care,Gastroenterology,Nephrology,Endocrinology,' + 
                           'Infectious Diseases,Immunology,Rheumatology,Family Medicine', Emergency=False,Exclude=Solved)
random = sorted(list(np.random.choice(Emergency,3,replace=False)))
random += sorted(list(np.random.choice(Oncology,2,replace=False)))
random += sorted(list(np.random.choice(Medicine,5,replace=False)))
Solved += random
with open('Solved.txt','w') as Output: 
    for x in Solved: Output.write(str(x)+'\n')
newQuestions = df.loc[random,['Question','Answer']]
Text=text(newQuestions)

from datetime import date 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
me = "<Your Email>@gmail.com"
you = "<Sent to this email>@gmail.com"
msg = MIMEMultipart()
msg['Subject'] = "MReview {}".format(date.today())
msg['From'] = me
msg['To'] = you
msg.attach(MIMEText(Text))
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
mail.login(me,'<Your Password>')
mail.sendmail(me, you, msg.as_string())
