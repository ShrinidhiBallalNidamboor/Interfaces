import time
configuration=[2]

def configure(speed_data):
    configuration[0]=speed_data

def entermessage():
    message=input('Enter message: ')
    array=[]
    for i in message:
        value=[]
        temp=ord(i)
        for j in range(8):
            if temp%2==0:
                value.append('0')
            else:
                value.append('1')
            temp//=2
        array+=value[::-1]
    return ''.join(array)

def setpin(bit, jumper):
    with open(jumper, 'w') as file:
        file.write(bit)
    time.sleep(configuration[0])

def synchronize(clock):
    with open(clock, 'r') as clk:
        temp=clk.read()
        while True:
            with open(clock, 'r') as clk:
                data=clk.read()
                if data!=temp:
                    break
def start(clock, sda):
    while True:        
        with open(clock, 'r') as file:
            data=file.read()
            if data=='1':
                time.sleep(configuration[0]//2)
                with open(sda, 'w') as file:
                    file.write('0')
                time.sleep(configuration[0]//2)
                break

def end(clock, sda):
    while True:        
        with open(clock, 'r') as file:
            data=file.read()
            if data=='1':
                time.sleep(configuration[0]//2)
                with open(sda, 'w') as file:
                    file.write('1')
                time.sleep(configuration[0]//2)
                break

def toggleclock(clock):
    with open(clock, 'w') as file:
        file.write('1')
    value='1'
    while True:
        with open(clock, 'w') as file:
            file.write(value)
        if value=='1':
            value='0'
        else:
            value='1'
        time.sleep(configuration[0])

def sendpackets(clock, message, sda):
    print('Sending packets...')
    synchronize(clock)
    start(clock, sda)
    for bit in message:
        setpin(bit, sda)
    end(clock, sda)
    
def decrptMessage(message):
    print(message)
    message=''.join(message)
    length=len(message)
    string=''
    for i in range(0, length, 8):
        string+=chr(int(message[i:i+8],2))
    return string

def checkJumper(clock, sda, output):
    buffer=[]
    with open(clock, 'r') as file:
        state1=file.read()
    with open(sda, 'r') as file:
        state2=file.read()
    mode='0'
    while True:
        with open(clock, 'r') as file:
            tempstate1=file.read()
        with open(sda, 'r') as file:
            tempstate2=file.read()
        if state1=='1' and state2=='1' and tempstate2=='0':
            mode='1'
            time.sleep(configuration[0]//2)
        if state1=='1' and state2=='0' and tempstate2=='1':
            mode='0'
            time.sleep(configuration[0]//2)
        state1=tempstate1
        state2=tempstate2
        if mode=='0':
            if buffer!=[]:
                data=decrptMessage(buffer)
                with open(output, 'w') as out:
                    out.write(data)
                buffer=[]
        else:
            with open(sda, 'r') as jp:
                data=jp.read()
                buffer.append(data)
            time.sleep(configuration[0])