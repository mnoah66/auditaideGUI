from datetime import timedelta, date, time
import datetime


def convert24(str1):
        # Checking if last two elements of time
        # is AM and first two elements are 12
        if str1[-2:] == "AM" and str1[:2] == "12":
            hour = "0"
            minute = str1[3:-3]
            return int(hour), int(minute)   
        # remove the AM    
        elif str1[-2:] == "AM":
            if str1[0] == "0":
                hour = str1[1]
            else:
                hour = str1[:2]
            if str1[3] == "0":
                minute = str1[4]
            else:
                minute = str1[3:-3]
            
            #minute =  str1[3:-3]
            return int(hour), int(minute)
         
        # Checking if last two elements of time
        # is PM and first two elements are 12   
        elif str1[-2:] == "PM" and str1[:2] == "12":
            if str1[0] == "0":
                hour = str1[1]
            else:
                hour = str1[:2]
            if str1[3] == "0":
                minute = str1[4]
            else:
                minute = str1[3:-3]
            return int(hour), int(minute)
             
        else:
             
            # add 12 to hours and remove PM
            hour = int(str1[:2]) + 12
            
            if str1[3] == "0":
                minute = str1[4]
            else:
                minute = str1[3:-3]

            return int(hour), int(minute)
 
def flaggedWords(ws, my_list, results_list):
    for row in ws.iter_rows(row_offset=1):
        foundWords = []
        if row[0].value:
            for w in sorted(my_list):
                if w in str(row[0].value).lower():
                    foundWords.append(w)
            if len(foundWords) > 0:
                note = ''
                for l in foundWords:
                    left,sep,right = row[0].value.lower().partition(l)
                    note = note + "..." + left[-70:] + sep.upper() + right[:70] + "..." + ';'
                forCSV = ','.join(foundWords).upper()
                results_list.append([forCSV, row[1].value, str(row[2].value.strftime('%m/%d/%Y')),  row[3].value,note, row[4].value.strftime("%I:%M:%S %p"), row[5].value.strftime("%I:%M:%S %p"), row[6].value, row[7].value])
    return results_list
def flaggedWordsInverse(ws, my_list, results_list):
    for row in ws.iter_rows(row_offset=1):
        foundWords = []
        if row[0].value:
            for w in sorted(my_list):
                if w.lower() not in str(row[0].value).lower():
                    foundWords.append(w)
            if len(foundWords) > 0:
                note = str(row[0].value[:200]) + ' [. . .] ' + str(row[0].value[-200:])
                forCSV = ','.join(foundWords).upper()
                results_list.append(['Missing ' + forCSV, row[1].value, str(row[2].value.strftime('%m/%d/%Y')), row[3].value, note, row[4].value.strftime("%I:%M:%S %p"), row[5].value.strftime("%I:%M:%S %p"), row[6].value, row[7].value])
    return results_list
def oddDuration(ws, greaterthan, lessthan, results_list):
    for row in ws.iter_rows(row_offset=1):
        if row[0].value:
            if row[6].value:
                if row[6].value <= lessthan:# or row[6].value >= greaterthan:
                    note = str(row[0].value[:200]) + ' [. . .] ' + str(row[0].value[-200:])
                    results_list.append(['Duration < '+ str(lessthan), row[1].value, str(row[2].value.strftime('%m/%d/%Y')),  row[3].value, note, row[4].value.strftime("%I:%M %p"), row[5].value.strftime("%I:%M %p"), row[6].value, row[7].value])
                elif row[6].value >= greaterthan:
                    note = str(row[0].value[:200]) + ' [. . .] ' + str(row[0].value[-200:]) 
                    results_list.append(['Duration > '+ str(greaterthan), row[1].value, str(row[2].value.strftime('%m/%d/%Y')),  row[3].value, note, row[4].value.strftime("%I:%M %p"), row[5].value.strftime("%I:%M %p"), row[6].value, row[7].value])
            else:
                results_list.append(['No Duration or times entered', row[1].value, str(row[2].value.strftime('%m/%d/%Y')),  row[3].value, row[0].value, '', '', '', row[7].value])
    return results_list
def shortNote(ws, notelength, results_list):
    for row in ws.iter_rows(row_offset=1):
        if row[0].value:
            if len(row[0].value) < note_length:
                results_list.append(['NOTE LENGTH < ' + str(note_length), row[1].value, row[2].value.strftime('%m/%d/%Y'),  row[3].value, row[0].value, row[4].value.strftime("%I:%M %p"), row[5].value.strftime("%I:%M %p"), row[6].value, row[7].value])
    return results_list
def oddTimes(ws, startTimeAfter, startTimeBefore, results_list):

    after = convert24(startTimeAfter)
    afterHour = after[0]
    afterMin = after[1]
    before = convert24(startTimeBefore)
    beforeHour = before[0]
    beforeMin = before[1]
    for row in ws.iter_rows(row_offset=1):
        d = row[0] # The note
        e = row[1] # The name of the individual
        f = row[2] # Contact date
        g = row[3] # Program
        h = row[4] # Start time
        i = row[5] # end time
        j = row[6] # duration
        k = row[7] # Note writer
        if h.value:
            note = d.value.split('.')
            d = '.'.join(note[1:3]).lstrip() + ' [. . .] ' + d.value[-100:]
            
            if h.value > time(afterHour, afterMin):
                #self.csvWritee("START TIME AFTER " + startTimeAfter, e, h, i, f, d, g, j, k)
                this_list = ['START TIME AFTER ' + startTimeAfter, e.value, h.value, i.value, f.value, d, g.value, j.value, k.value]
                results_list.append(this_list)
            elif h.value < time(beforeHour, beforeMin):
                this_list = ['START TIME BEFORE ' + startTimeBefore, e.value, h.value, i.value, f.value, d, g.value, j.value, k.value]
                results_list.append(this_list)
                #self.csvWritee("START TIME Before " + startTimeBefore, e, h, i, f, d, g, j, k)
            #except (TypeError):
            #    this_list = ['12AM/Error', e.value, h.value, i.value, f.value, d, g.value, j.value, k.value]
            #    results_list.append(this_list)

    return results_list
def underUnits(ws, underUnits, results_list):

    units = int(underUnits) * 15
    from collections import defaultdict
    names = defaultdict(int)
    for row in ws.iter_rows(row_offset=1):
        d = row[0] # The note
        e = row[1] # The name of the individual
        f = row[2] # Contact date
        g = row[3] # Program
        h = row[4] # Start time
        i = row[5] # end time
        j = row[6] # duration
        k = row[7] # Note writer

        if j.value is None:
            pass
        else:
            names[e.value] += j.value
    for k, v in names.items():
        if names[k] < units:
            this_list = ['UNDER UNITS (' +str(underUnits) + ')', k, str(int(v)/15), '', '','', '', '', '', '']
            results_list.append(this_list)

def overlap(list_item, key, k, results_list):
    intervals = list_item
    overlapping = [ [s,e] for s in intervals for e in intervals if s is not e and s[1]>e[0] and s[0]<e[0] ]
    #duplicate = [ [s,e] for s in intervals for e in intervals if s is not e and s[0]==e[0] ]
    #unique_duplicate = [list(x) for x in set(tuple(x) for x in duplicate)]
    for x in overlapping:
        results_list.append(['OVERLAPPING', "{0} has overlapping notes on {1}".format(key, k.strftime('%m/%d/%y')),'', '','', '', '', '', '',''])
    #for y in unique_duplicate:
    #    results_list.append(["{0} has duplicated start times on {1}".format(key, k),'', '','', '', '', '', '','',''])
    
def overlapping_notes(ws, results_list):
    from collections import defaultdict
    people = defaultdict(dict)
    for row in ws.iter_rows(row_offset=1):
      p=row[1]
      l=row[2]
      s=row[4]
      e=row[5]
      if p.value:
        if p.value not in people:
            people[p.value] = defaultdict(list)
        people[p.value][l.value].append((s.value, e.value))
    for key, val in people.items():
        for k, v in val.items():
          overlap(v, key, k, results_list)
    

'''
def under7forResidential(self):
        example_dictionary = defaultdict(list)
        for row in ws:
            a = row[0]
            b = row[1]
            if a.value:
                example_dictionary[a.value].append(b.value)

        namesClean = {}

        for names, values in example_dictionary.items():
            namesClean[names] = set(values)

        for names, values in namesClean.items():
            if len(values) < 2:
                print(names + ' has less than two dates')

'''

def duplicate_notes(ws):
    import collections
    notes=[]
    for row in ws.iter_rows(row_offset=1):
        if row[0].value:
            notes.append(row[0].value)
    dupnotes = [item for item, count in collections.Counter(notes).items() if count > 1]
    for item in dupnotes:
        for row in ws.iter_rows(row_offset=1):
            d = row[0] # The note
            e = row[1] # The name of the individual
            f = row[2] # Contact date
            g = row[3] # Program
            h = row[4] # Start time
            i = row[5] # end time
            j = row[6] # duration
            k = row[7] # No
            if row[0].value:
                if item == row[0].value:
                    #outputWriter.writerow(['DUPLICATED NOTE', row[1].value, item, str(row[2].value.strftime('%m/%d/%Y')), str(row[7].value),'', '', '', '', '',''])
                    csvWritee('DUPLICATED NOTE',e, h, i, f, item, g, j, k)