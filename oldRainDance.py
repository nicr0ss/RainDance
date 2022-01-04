import urllib.request
from datetime import datetime
import tkinter
#m = tkinter.Tk()
#w = tkinter.Button(m, text = 'start', width = '25')
#m.mainloop()
stop = 0
stationdict = {"dart":"46126-level-stage-i-15_min-m",
               "east lyn":"50150-level-stage-i-15_min-m",
               "east dart":"46123-level-2-i-15_min-m",
               "east okemont":"50195-level-stage-i-15_min-m",
               "upper ashburn":"46116-level-stage-i-15_min-mASD",
               "lower ashburn":"46115-level-stage-i-15_min-mASD",
               "mary tavy":"47135-level-stage-i-15_min-m",
               "tavistock":"47172-level-stage-i-15_min-m",
               "denham ludbrook":"47122-level-1-i-15_min-m"
               }
def timediff(t):
    realtime = str(datetime.now())
    differencehour = int(realtime[11:13])-int(t[0:2])
    differencemin = int(realtime[14:16])-int(t[3:5])
    if differencemin < 0:
        deltamin = 60 - differencemin
        deltatime = "The latest measurement was", str(differencehour), "hours and", str(deltamin), "minutes ago."
    else:
        deltatime = "The latest measurement was ", str(differencehour), " hours and ", str(differencemin), " minutes ago."
    answer = ""
    answer = answer.join(deltatime)
    return answer
print('Welcome to RainCatcher v1. A project to predict river levels based on historic trends and forecast predictions.')
#for keys in stationdict.items():
    #print(keys)
while stop == 0:
    river = input("Please enter the river name you would like: ")
    print("Searching for: ", river)
    rvr = river.lower()
    if rvr in stationdict:
        identifier = stationdict.get(rvr)
        link = ["http://environment.data.gov.uk/flood-monitoring/id/measures/", identifier, "/readings?latest"]
        final = ""
        final = final.join(link)
        print(final)
        web = urllib.request.Request(final)
        response = urllib.request.urlopen(web)
        the_page = response.read()
        value = bytes(the_page)
        s = value.decode()
        locationlevel = s.find("value")
        level = s[locationlevel+9:locationlevel+14] + "m"
        locationtime = s.find("dateTime")
        date = s[locationtime+13:locationtime+23]
        time = s[locationtime+24:locationtime+33]
        print("SUCCESS!")
        print("The ", river, "is recorded to be at", level)
        print("This recording was measured at:", time, "Date:", date)
        print(timediff(time))
    else:
        print("ERROR: River not recognised or not yet in database. Please try again.")
    again = input("Would you like to 1.Search again or 2.Stop programme")
    while again != '1' and again != '2':
        print("ERROR: Response not understood. Please check response format.")
        again = input("Would you like to 1.Search again or 2.Stop programme")
    if again == "1":
        stop = 0
    else:
        stop = 1
        print("Programme stopped")
