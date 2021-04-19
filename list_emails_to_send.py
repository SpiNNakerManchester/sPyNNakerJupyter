import dbm

confirmed = list()
unconfirmed = list()

with dbm.open('passwords.dbm', 'r') as db:
    with dbm.open('registration.dbm', 'r') as reg:
        with dbm.open('email.dbm', 'r') as emails:
            username = db.firstkey()
            while username != None:
                if username in emails:
                    if username in reg:
                        unconfirmed.append((username, emails[username]))
                    else:
                        confirmed.append((username, emails[username]))
                username = db.nextkey(username)

emails = ""
for username, email in confirmed:
    emails += email.decode("utf-8") + "; "
for username, email in unconfirmed:
    emails += email.decode("utf-8") + "; "

print(emails)

