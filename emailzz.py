import smtplib
from flask import Flask

app = Flask(__name__)

my_email = 'hashcode123@outlook.com'
my_password = 'trialtestt123.'

@app.route('/')
def send_email():
    with smtplib.SMTP("smtp.office365.com", port=587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs='appbrewery132@yahoo.com',
            msg=f"Subject:Happy Birthday!\n\nTesting email"
        )
        connection.close()
    return '<p>email send successfully</p>'

if __name__=="__main__":
    app.run(debug=True)