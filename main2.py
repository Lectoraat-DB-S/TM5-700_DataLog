# Z(TCP Value) 7358~7359 float R Dword
# FZ 7805~7806 float R Dword 

from ctypes.wintypes import DWORD               # data conversion
from pyModbusTCP.client import ModbusClient
from time import sleep
import csv
from time import ctime

#register 7358, 7359 is the Z (TCP Value). this is pre defined data and does not change when the cobot moves 
#register 7805, 7806 is the force in the Z direction
#register 7029, 7030 is the Z (tool coordinates)

# variables
registers = [7358,7359,7805,7806,7029,7030]                 # registers to get data from
valueable = []                                              # list to safe data to
for x in registers:
    valueable.append(x)
j = 0
ZC_word = 0                                                 # variable that contains end result after data conversion   (Z coordinate)
ZF_word = 0                                                 # variable that contains end result after data conversion   (Z force)
file_location = 'C:/Users/fz0132865/Documents/data.csv'     # data location (file must excist before running code)
data_interval = 0.05                                        # interval at which the data is gathered
fieldnames = ['Date + Time', 'ZF', 'ZC']                    # header names of the CSV

# pre defined function to convert 2 words in ieee-754 to a decimal number
def ieee745(N1, N2): # ieee-745 bits (max 32 bit)
    N = (N1 << 16) | N2
    a = (N & 2147483648) >> 31        # sign,     1 bit
    b = (N & 2139095040) >> 23        # sign,     1 bit
    c = N & 8388607                   # sign,     1 bit

    exponant = b - 127

    m=0

    for p in range(23):
        if((c >> p) & 1):
            m = m + (2**(-(23-p)))
    finalist = ((-1)**a)*(1+m)*(2**exponant)
    return finalist

# main function
try:
    # initialize csv writer
    f = open(file_location, 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    #initialize connection with cobot
    print("starting server")
    client = ModbusClient(host="10.38.4.36", port=502)
    client.open()
    print("server started")
    print ("checking initialisation status...")

    #start data gathering
    while True:
        j = 0
        for i in registers:
            status=client.read_input_registers(i)
            valueable[j] = status
            j = j+1
        ZF_word = ieee745(valueable[2][0], valueable[3][0])
        ZC_word = ieee745(valueable[4][0], valueable[5][0])
        print("Z force: ", ZF_word, "Z coordinate: ", ZC_word)
        data = [{'Date + Time': ctime(), 'ZF': ZF_word, 'ZC': ZC_word}]
        writer.writerows(data)
        sleep(data_interval)
        

#press ctrl+c to stop the user interface
except:
    print("client closed")
    client.close()
    f.close()
