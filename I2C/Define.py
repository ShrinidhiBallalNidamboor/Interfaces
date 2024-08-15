import time
configuration=[8,2,3]

def configure(speed_data, length_data_index, packet_rate):
    configuration[0]=speed_data
    configuration[1]=length_data_index*8
    configuration[2]=packet_rate

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

def packagemessage(message):
    print('Packaging messages...')
    result=[]
    length=len(message)
    for i in range(0, length, configuration[2]):
        result.append(message[i:i+configuration[2]])
    length=len(result)
    for i in range(length):
        result[i]=configuration[0]+result[i]+parity(result[i])+configuration[1]
    return result

def setpin(bit, jumper):
    with open(jumper, 'w') as file:
        file.write(bit)
    time.sleep(configuration[3])

def sendpackets(packets, jumper):
    print('Sending packets...')
    number=0
    for packet in packets:
        for bit in packet:
            setpin(bit, jumper)
        print('Packet sent: ', number, packet)
        number+=1
        time.sleep(configuration[4])

def decrptMessage(message):
    length=len(message)
    string=''
    for i in range(0, length, 8):
        string+=chr(int(message[i:i+8],2))
    return string

def decryptpacket(buffer):
    start=''.join(buffer[:len(configuration[0])])
    stop=''.join(buffer[-len(configuration[1]):])
    data=''.join(buffer[len(configuration[0]):len(configuration[0])+configuration[2]])
    paritybit=buffer[-len(configuration[1])-1]
    if start==configuration[0] and stop==configuration[1]:
        return decrptMessage(data)
    return ''

def checkJumper(jumper, output):
    length=len(configuration[0])+len(configuration[1])+configuration[2]+1
    buffer=[]
    for i in range(length):
        buffer.append('1')
    while True:
        buffer.pop(0)
        with open(jumper, 'r') as jp:
            data=jp.read()
            buffer.append(data)
            print('Buffer data: ', ''.join(buffer))
            string=decryptpacket(buffer)
            print('Data packet:', string)
            with open(output, 'r') as out:
                data=out.read()
                data+=string
                with open(output, 'w') as out:
                    out.write(data)
        time.sleep(configuration[3])