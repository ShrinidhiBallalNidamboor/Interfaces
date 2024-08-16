from Define import entermessage
from Define import sendpackets

while True:
    instruction=input('Send message (Y/N): ')
    if instruction=='Y':
        message=entermessage()
        print(message)
        sendpackets('Clock.txt', message, 'SDA.txt')
    else:
        break