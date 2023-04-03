import smtplib
from email.mime.text import MIMEText
'''
50 i mniej - 2
51 - 60 pkt - 3
61 – 70 pkt – 3.5
71 – 80 pkt - 4
81 - 90 pkt – 4.5
91 - 100 pkt – 5
'''
data = {}

def sendEMail(recieverEMail):
    student = data[recieverEMail]
    sender = ""
    msg = MIMEText(f"Dostałeś ocenę: {student['ocena']}")
    msg['Subject'] = "Ocena wystawiona!"
    msg['From'] = sender
    msg['To'] = ', '.join(recieverEMail)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, "")
    smtp_server.sendmail(sender, recieverEMail, msg.as_string())
    smtp_server.quit()
    student['status'] = "MAILED"

def getGrade(points):
    points = int(points)
    if points < 51:
        return 2
    elif points < 61:
        return 3
    elif points < 71:
        return 3.5
    elif points < 81:
        return 4
    elif points < 91:
        return 4.5
    else:
        return 5

FileName = "plik.txt"
with open(FileName,'r') as f:
    for line in f:
        lineData = line.split(",")
        data[lineData[0]] = {"imię" : lineData[1],
                             "nazwisko" : lineData[2],
                             "punkty" : lineData[3].replace("\n",''),
                             "ocena" : lineData[4].replace("\n",'') if len(lineData)>4 else getGrade(lineData[3]),
                             "status" : lineData[5].replace("\n",'') if len(lineData)>5 else "GRADED"
                             }
#print(data)
def updateData():
    for key in data.keys():
        student = data[key]
        if student["status"]!="GRADED" or student["status"]!="MAILED":
            student["ocena"] = getGrade(student["punkty"])
            sendEMail(key)

    with open(FileName, 'w') as f:
        text = ""
        for key in data.keys():
            text+=f"{key},{data[key]['imie']},{data[key]['nazwisko']},{data[key]['punkty']},{data[key]['ocena']},{data[key]['status']}\n"
        f.write(text)

command = None
while command != '-quit':
    command = input("Commands:\n-delete example@gmail.com\n-update example@gmail.com <imię> <nazwisko> <punkty>\n-quit")
    if not command.startswith("-"):
        print("Not a command")
        continue
    if command.startswith("-delete"):
