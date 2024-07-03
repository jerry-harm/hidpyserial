import numpy as np
import scipy
import serial.tools.list_ports
import matplotlib.pyplot as plt

if __name__ == '__main__':

    ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

    com = input("请输入串口号：")

    ser = serial.Serial(com, 9600)  # 串口号和波特率
    ser.bytesize = serial.EIGHTBITS  # 数据位长度为8位
    ser.parity = serial.PARITY_NONE  # 无奇偶校验
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1  # 读取超时时间为1秒

    datas = []
    i = 0
    while i < 500:
        data = ser.read(1)
        print(data, '\n')
        if data.decode('utf-8') == " " or data.decode('utf-8') == '-':
            d = ser.read(5).decode('utf-8')
            print(d)
            if data.decode('utf-8') == " ":
                datas.append(float(d))
            else:
                datas.append(-float(d))
            i += 1
    x = np.linspace(0, 1, len(datas))
    datas = np.array(datas)
    module= scipy.interpolate.make_smoothing_spline(x,datas,lam=0.00001)
    plt.plot(x, datas , label='temperature')
    plt.plot(x,module(x), label='smoothed')
    plt.ylabel('temperature')
    plt.title('datas captured')
    plt.legend()
    plt.savefig('data.png')
