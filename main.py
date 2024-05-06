import serial
import serial.tools.list_ports
import time
import signal
import time
import sys

spkeytable={'!':[0x1e,2],'@':[0x1f,2],'#':[0x20,2],'$':[0x21,2],
            '%':[0x22,2],'^':[0x23,2],'&':[0x24,2],'*':[0x25,2],
            '(':[0x26,2],')':[0x27,2],'enter':[0x28,0],'delete':[0x2a,0],
            'tab':[0x2b,0],'-':[0x2d,0],'=':[0x2e,0],'+':[0x2e,2],'_':[0x2d,2],
            '[':[0x2f,0],'{':[0x2f,2],
            ']':[0x30,0], '}':[0x30,2],'\\':[0x31,0],'|':[0x31,2],
            ';':[0x33,0],':':[0x33,2],'/':[0x38,0],'?':[0x38,2],
            '<':[0x36,2],',':[0x36,0],
            '>':[0x37,2],'.':[0x37,0],'\'':[0x34,0],'"':[0x34,2]
            ,' ':[0x2c,0],'F1':[0x3a,0],'F2':[0x3b,0],'F3':[0x3c,0],'F4':[0x3d,0],
            'F5':[0x3e,0],'F6':[0x3f,0],'F7':[0x40,0],'F8':[0x41,0],'F9':[0x42,0],
            'F10':[0x43,0],'F11':[0x44,0],'F12':[0x45,0],
            'up':[0x52,0],'down':[0x51,0],'left':[0x50,0],'right':[0x4f,0],
            'esc':[0x29,0],'power':[0x66,0]
            }


def convert(letter):
    if letter in spkeytable:
        return spkeytable[letter]
    if letter>='a' and letter<='z':
        return [ord(letter)-ord('a')+4,0]
    if letter>='A' and letter<='Z':
        return [ord(letter)-ord('A')+4,2]
    if letter>='1' and letter<='9':
        return [ord(letter)-ord('1')+0x1e,0]
    if letter=='0':
        return [0x27,0]
    else:
        print("Invalid key")
        return [0,0]


def signal_handler(signal, frame):
    print('Caught Ctrl+C / SIGINT signal')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

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
    cmd = input("请输入指令：\n")
    if cmd in spkeytable:
        times = input("请输入次数：\n") 
        code = spkeytable[cmd]
        
        # 发送数据
        for i in range(int(times)):
            ser.write(bytearray([0]))
            ser.write(bytearray([code[0],code[1]]))
            data = ser.read(4)
            print(i)
            time.sleep(0.01)
            
    else:
        for i in cmd:
            code = convert(i)
            
            # 发送数据
            ser.write(bytearray([0]))
            ser.write(bytearray([code[0],code[1]]) )
            data = ser.read(4)
            
            time.sleep(0.01)

            # 接收数据


ser.close()

