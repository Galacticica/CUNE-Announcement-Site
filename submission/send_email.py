import requests
import os
def send_simple_message():
    response = requests.post(
        "https://api.mailgun.net/v3/sandboxc96b221050bb4ddb8cea645eaf9a6c62.mailgun.org/messages",
        auth=("api", os.getenv('EMAIL_KEY', 'EMAIL_KEY')),
        data={"from": "Mailgun Sandbox <postmaster@sandboxc96b221050bb4ddb8cea645eaf9a6c62.mailgun.org>",
              "to": "Reagan Zierke <reaganzierke@gmail.com>",
              "subject": "Hello Reagan Zierke",
              "text": "Congratulations Reagan Zierke, you just sent an email with Mailgun! You are truly awesome!"}
    )
    if response.status_code == 200:
        print("Email sent successfully:", response.json().get("message"))
        return True
    else:
        print("Failed to send email:", response.text)
        return False
    

if __name__ == "__main__":
	send_simple_message()