# (c) stonatm@gmail.com
# raspberry pi python simple
# driver for DLO1414
# alphanumeric inteligent display

class dlo1414:
  from gpiozero import LED
  import time

  D0 = None
  D1 = None
  D2 = None
  D3 = None
  D4 = None
  D5 = None
  D6 = None
  DATA_PINS = []

  A0 = None
  A1 = None
  ADDRESS_PINS = []

  WR = None
  
  DEBUG = False

  # initialize display pins
  def init(d0,d1,d2,d3,d4,d5,d6,a0,a1,wr):
    dlo1414.D0 = dlo1414.LED(d0)
    dlo1414.D1 = dlo1414.LED(d1)
    dlo1414.D2 = dlo1414.LED(d2)
    dlo1414.D3 = dlo1414.LED(d3)
    dlo1414.D4 = dlo1414.LED(d4)
    dlo1414.D5 = dlo1414.LED(d5)
    dlo1414.D6 = dlo1414.LED(d6)
    dlo1414.DATA_PINS = [dlo1414.D0,dlo1414.D1,dlo1414.D2,dlo1414.D3,dlo1414.D4,dlo1414.D5,dlo1414.D6]

    dlo1414.A0 = dlo1414.LED(a0)
    dlo1414.A1 = dlo1414.LED(a1)
    dlo1414.ADDRESS_PINS = [dlo1414.A0,dlo1414.A1]
    dlo1414.WR = dlo1414.LED(wr)
    dlo1414.WR.on()

  # write single char at given position
  def write_char(pos, char=" "):
    # check proper position range
    if pos<0 or pos>3:
      if dlo1414.DEBUG: print('write_char: invalid pos=',pos)
      return
    if not(char):
      if dlo1414.DEBUG: print('write_char: invalid char')
      char=" "
    # hold WR line HIGH
    dlo1414.WR.on()
    # set address lines on display
    for i in range(2):
      if pos & (1 << i):
        dlo1414.ADDRESS_PINS[i].on()
      else:
        dlo1414.ADDRESS_PINS[i].off()
    # set WR line LOW
    dlo1414.time.sleep(1/1000000)
    dlo1414.WR.off()
    ascii = ord(char)
    # set data lines on display
    for i in range(7):
      if ascii & (1 << i):
        dlo1414.DATA_PINS[i].on()
      else:
        dlo1414.DATA_PINS[i].off()
    # hold WR line HIGH
    dlo1414.time.sleep(1/1000000)
    dlo1414.WR.on() 

  def write_str(text="    "):
    # if text is empty
    if not(text):
      if dlo1414.DEBUG: print('write_str: invalid string')
      text = "    "
    text = str(text)
    # if text is amaler than 4 chars
    # add spaces before string
    if len(text)<4:
      for i in range(4-len(text)):
        if dlo1414.DEBUG: print('write_str: adding a space')
        text = " " + text
    # write string to display
    for i in range(4):
      dlo1414.write_char(3-i, text[i])

  def scroll_text(text, delay_ms=200):
    buffer = str(text) + "    "
    buffer = "    " + buffer
    for i in range(len(buffer)-4+1):
      dlo1414.time.sleep(delay_ms/1000)
      dlo1414.write_str(str(buffer[0+i:4+i]))

  def clear():
    for i in range(4):
      dlo1414.write_char(i, ' ')