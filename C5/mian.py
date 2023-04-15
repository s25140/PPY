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
    try:
        sender = "" #here write your e-mail
    except TypeError:
        print("Exception: Add your e-mail in line 16")
        raise SystemExit
    msg = MIMEText(f"Dostałeś ocenę: {student['ocena']}")
    msg['Subject'] = "Ocena wystawiona!"
    msg['From'] = sender
    msg['To'] = ', '.join(recieverEMail)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try:
        smtp_server.login(sender, "")#here write App password
    except TypeError:
        print("Exception: Add your e-mail App password in line 26")
        raise SystemExit
    smtp_server.sendmail(sender, recieverEMail, msg.as_string())
    smtp_server.quit()
    student['status'] = "MAILED"
    print("E-mail sent")

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
        data[lineData[0]] = {"imie" : lineData[1],
                             "nazwisko" : lineData[2],
                             "punkty" : lineData[3].replace("\n",''),
                             "ocena" : lineData[4].replace("\n",'') if len(lineData)>4 else getGrade(lineData[3]),
                             "status" : lineData[5].replace("\n",'') if len(lineData)>5 else "GRADED"
                             }
#print(data)
def updateData(): # write grade, send mail, set MAILED and write to file
    for key in data.keys():
        student = data[key]
        if student["status"]!="GRADED" and student["status"]!="MAILED":
            student["ocena"] = getGrade(student["punkty"])
        elif student["status"]!="MAILED":
            sendEMail(key)

    with open(FileName, 'w') as f:
        text = ""
        for key in data.keys():
            text+=f"{key},{data[key]['imie']},{data[key]['nazwisko']},{data[key]['punkty']},{data[key]['ocena']},{data[key]['status']}\n"
        f.write(text)

command = None
while command != '-quit':
    command = input("Commands:\n-delete example@gmail.com\n-update example@gmail.com <imię> <nazwisko> <punkty>\n-add example@gmail.com <imię> <nazwisko> <punkty>\n-quit\n")
    if not command.startswith("-"):
        print("Not a command")
        continue
    if command.startswith("-quit"):
        raise SystemExit
    Email = command.split(" ")[1]
    if command.startswith("-delete") and len(command.split(" "))==2:
        data.pop(Email)
        updateData()
        print(f"{Email} removed")
    elif command.startswith("-update") or command.startswith("-add") and len(command.split(" "))==5:
        args = command.split(" ")
        data[Email] = {
            "imie": args[2],
            "nazwisko": args[3],
            "punkty": args[4].replace("\n", ''),
            "ocena": getGrade(args[4]),
            "status": "GRADED"
        }
        print (f"Added/Updated: {data[Email]}")
        updateData()
    else:
        print("Wrong command")
