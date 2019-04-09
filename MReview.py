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
     
     





