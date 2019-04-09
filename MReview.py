import pandas as pd

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
             frame = frame[frame.Emergency == 'No']
     if Pharmacology != 'All':
         if Pharmacology == True: 
             frame = frame[frame.Pharmacology == 'Yes']
         elif Pharmacology == False:
             frame = frame[frame.Pharmacology == 'No']
     
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
    print('\nThe questions were collected over {} days since {}.'.format((frame.Date.iloc[-1]-frame.Date.iloc[0]).days+1,
                                frame.Date.iloc[-1].strftime('%Y-%m-%d')))




