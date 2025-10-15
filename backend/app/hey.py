import smtplib

s = db_smtps[0]  # pick a working one
password = s.encrypted_password  # use plain text if needed
server = smtplib.SMTP(s.host, s.port)
if s.port == 587:
    server.starttls()
server.login(s.username, password)
print("Login success")
server.quit()
