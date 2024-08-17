clock='Clock.txt'
sda='SDA.txt'
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
    if state1=='1' and state2=='0' and tempstate2=='1':
        mode='0'
    state1=tempstate1
    state2=tempstate2
    with open('Type.txt', 'w') as tp:
        tp.write(mode)