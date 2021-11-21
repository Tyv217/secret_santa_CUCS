import random
import random
import smtplib
from email import encoders
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    return lines

def write_back(santas, names_to_emails):
    with open('readme.txt', 'w') as f:
        for key in santas:
            person1 = key + ", " + names_to_emails[key]
            person2 = santas[key] + ", " + names_to_emails[santas[key]]
            f.write(person1 + ": " + person2 + "\n")

def send_email(santas, names_to_emails):
    password = input("Password: ")
    for x in santas:
        fromaddr = "admin@cucs.com.hk"
        toaddr = names_to_emails[x]
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "SECRET EMAIL FOR SECRET SANTA!"
        body1 = "Hello, "+ x
        body2 = '''!\nThis is an automated email from CUCS's Secret Santa Program for the Bridgemas Formal.\n\nYou drew\n.......\n........\n........\n'''+ santas[x] +"!!\n\nRule Number 1: Please do not tell anyone!\n"
        body3 = "Rule Number 2: The budget is 5-10 pounds but you are welcome to go over this!\n"
        body4 = "Rule Number 3: Please bring along the gift with " + santas[x] + "\'s name on the gift so they know they have a gift.\n"
        body5 = "Lastly, please be reminded that the date of the event is 25/11/2021, and the location is Newnham College. The formal will start at 19:30, but please come at 19:00 to put your gift down. We are looking forward to seeing all of you!\n\nWhat are you waiting for? Go ahead and get something nice for "+ santas[x] +"!\n\n\n"
        body = body1+body2+body3+body4+body5
        msg.attach(MIMEText(body, "plain"))
        
        filename = "secret_santa.png"
        attachment = open(filename, "rb")
    
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
        msg.attach(part)

        text = msg.as_string()
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("admin@cucs.com.hk", password)
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

def main():
    names = get_lines('names.txt')
    emails = get_lines('emails.txt')
    names_to_emails = {}
    for x in range(len(emails)):
        names_to_emails[names[x]] = emails[x]
    random.shuffle(names)
    offset = random.randint(1,int((len(names) - 1)/5))
    santas = {}
    print(names)
    print(offset)
    for x in range(len(names)):
        santas[names[x]] = names[(x + offset) % len(names)]
    print(santas)
    write_back(santas,names_to_emails)
    send_email(santas,names_to_emails)

if __name__ == '__main__' :
    main()
