import dbm

confirmed = list()
unconfirmed = list()

with dbm.open("passwords.dbm") as db:
    with dbm.open('registration.dbm', 'r') as reg:
        with dbm.open('email.dbm', 'r') as emails:
            username = db.firstkey()
            while username != None:
                if username in emails:
                    if username in reg:
                        unconfirmed.append(emails[username])
                    else:
                        confirmed.append(emails[username])
                username = db.nextkey(username)

print("Confirmed")
print("=========")
for email in confirmed:
    print(email)

print("Unconfirmed")
print("===========")
for email in unconfirmed:
    print(email)
