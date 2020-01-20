import csv
import datetime
import time
import os

data = []
header = []
index_map = {}
color_map = []
dates = {}

def cls():
    # Clears previous notifications
    os.system('cls' if os.name=='nt' else 'clear')

def read_csv(path):
    # Read csv
    global data, header
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            data.append(row)
            
    header = data[0]

def build_index():
    # Build index from number to trash types
    global index_map, dates
    for i in range(len(header)):
        index_map[i] = header[i]
        dates[i] = []

def type_trash():
    # Attribute trash dates to correct trash type
    global data, dates
    for i in range(1, len(data)):
        for j in range(0, len(header)):
            if data[i][j] == '':
                continue
            else:
                dates[j].append(data[i][j])

def trash_today():
    # Check if there's trash due today
    today = datetime.date.today().strftime('%d.%m.%Y')
    due_trash = []
    for i in range(len(header)):
        if today in dates[i]:
            due_trash.append(index_map[i])
    return due_trash

def trash_tomorrow():
    # Check if there's trash due tomorrow
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
    due_trash = []
    for i in range(len(header)):
        if tomorrow in dates[i]:
            due_trash.append(index_map[i])
    return due_trash

def trash_print(timeframe, due_trash):
    # Print which trash will get taken in timeframe
    time_rn = datetime.datetime.now().time()
    string = "[{:d}:{:02d}]\t".format(time_rn.hour, time_rn.minute)
    if len(due_trash) == 0:
        string += f'{timeframe} wird kein Müll abgeholt.'
    elif len(due_trash) == 1:
        string += f'{timeframe} wird {due_trash[0]} abgeholt.'
    elif len(due_trash) == 2:
        string += f'{timeframe} wird {", ".join(due_trash)} abgeholt.'
    elif len(due_trash) > 2:
        string += f'{timeframe} wird {", ".join(due_trash[0:-1])} und {due_trash[-1]} abgeholt.'
    print(string)

def setup(file):
    read_csv(file)
    build_index()
    type_trash()
    
def check_for_trash_today():
    today = trash_today()
    trash_print('Heute', today)

def check_for_trash_tomorrow():
    tomorrow = trash_tomorrow()
    trash_print('Morgen', tomorrow)

def main():
    setup('muelldaten.csv')
    today = datetime.date.today()
    last_checked = None
    while True:
        if last_checked != today:
            cls()
            check_for_trash_today()
            check_for_trash_tomorrow()
            last_checked = today
        else:
            time.sleep(3600)
            

if __name__ == "__main__":
    main()
