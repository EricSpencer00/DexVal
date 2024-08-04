Here's how to name your .env file to work with the codebase:

```
DEXCOM_USERNAME=yourusernamehere
DEXCOM_PASSWORD=yourpasswordhere

email_username=email@gmail.com
```
Note, the code allows you to use any domain where the smtp server is the same as the domain address.
```
email_password=xxxyxxxyxxxyxxxy
```
For gmail accounts, you will need to create a 16 digit app password after you enable 2FA. Read more here: https://support.google.com/mail/answer/185833?hl=en

```
receiver_email=9995559999@txt.att.net
```
AT&T supports emailing a phone number to receive a text message, find out if your service supports this at: https://www.notepage.net/smtp.htm

```
sql_host=localhost
sql_user=username
sql_password=password
sql_database=database
```
The SQL host is localhost for simplicity