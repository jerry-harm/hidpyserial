import serial
import serial.tools.list_ports
import time

spkeytable={'!':[0x1e,2],' ':[0x2c,0],'.':[37,0]}


def convert(letter):
    if letter in spkeytable:
        return spkeytable[letter]
    if letter>='a' and letter<='z':
        return [ord(letter)-ord('a')+4,0]
    if letter>='A' and letter<='Z':
        return [ord(letter)-ord('A')+4,2]
    if letter>='0' and letter<='9':
        return [ord(letter)-ord('0')+0x1E,0]


ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        
com = input("请输入串口号：")
    
ser = serial.Serial(com, 115200)  # 串口号和波特率
ser.bytesize = serial.EIGHTBITS  # 数据位长度为8位  
ser.parity = serial.PARITY_NONE   # 无奇偶校验  
ser.stopbits = serial.STOPBITS_ONE  
ser.timeout = 1             # 读取超时时间为1秒



while 1:
    for i in input("请输入指令：\n"):
        cmd = convert(i)
        # 发送数据
        ser.write(bytearray([0,0,0,cmd[0],cmd[1]]) )
        time.sleep(0.1)
        ser.write(bytearray([0,0,0,0x28,0]) )
        # # 接收数据
        # data = ser.read(8)
        # print(data)

ser.close()

