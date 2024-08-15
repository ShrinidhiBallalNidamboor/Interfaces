from Define import entermessage
from Define import packagemessage
from Define import sendpackets

while True:
    instruction=input('Send message (Y/N): ')
    if instruction=='Y':
        message=entermessage()
        packets=packagemessage(message)
        sendpackets(packets, 'T1-R2.txt')
    else:
        break