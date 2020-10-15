# from twilio.rest import Client

# # the following line needs your Twilio Account SID and Auth Token

# client = Client("AC10bfeb488d3d078c7b84d00c60279e20", "c5c763e2eee34a0127a3c6f2068a305c")

# # change the "from_" number to your Twilio number and the "to" number
# # to the phone number you signed up for Twilio with, or upgrade your
# # account to send SMS to any phone number

# client.messages.create(to="+16099032880",
#                        from_="+16515659512",
#                        body="Hello from Python!")

from py_imessage import imessage
import time

phone = "Bench Boys"

if not imessage.check_compatibility(phone):
    print("Not an iPhone")

guid = imessage.send(phone, "Test program to auto send whenever matt dc  says \"nice\"")

# Let the recipient read the message
time.sleep(5)
resp = imessage.status(guid)

print(f'Message was read at {resp.get("date_read")}')