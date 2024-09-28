from sympy import Symbol, solve
import telnetlib
import socket

def main():

  HOST='192.168.100.153'
  PORT=8231 
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST,PORT))
  s.settimeout(5)

  x=Symbol('x')
  equation = ""
  rData = ""
  while True:
    try:
      rData=s.recv(1024).decode()
    except socket.timeout:
      t = telnetlib.Telnet()
      t.sock = s
      t.interact()
      s.close()      
      return 0;
      
      
    print(rData)
    if ("No. " in rData):
    
      # x=Symbol('x')
      # 1. (x-1)(x-2)(x-2)
      # 2. (x-1)(x^2 - 4x + 4)
      # 3. x^3 - 5x^2 + 8x - 4
      # equation = "x**3 - 5*x**2 + 8*x - 4"
      
      rData = "".join(rData.split(" ")[2:-4])
      rData = rData.replace("x", "*x")
      equation = rData.replace("^", "**")
      print("[Parsed][ " + equation + " ]")
      
      ansArr = solve(equation)
      lenArr = len(ansArr)
      rst = ""
      
      if (lenArr == 1):
        rst = repr(ansArr[0]) + ", " + repr(ansArr[0]) + ", " + repr(ansArr[0]) + "\n"
        s.send(rst.encode())
        print("[Sended] " + rst)
        
      elif (lenArr == 2):
        prifix = int(equation.split("*x**3")[0])
        emt1 = ansArr[0]
        emt2 = ansArr[1]
        eCase1 = prifix*(x -1*emt1)**2 * (x -1*emt2)
        eCase2 = prifix*(x -1*emt2)**2 * (x -1*emt1)
        # print(eCase1)
        # print(eCase2)
        if (eCase1.equals(equation)):
          rst = repr(emt1) + ", " + repr(emt1) + ", " + repr(emt2) + "\n"
          s.send(rst.encode())
          print("[Sended] " + rst)
        elif (eCase2.equals(equation)):
          rst = repr(emt1) + ", " + repr(emt2) + ", " + repr(emt2) + "\n"
          s.send(rst.encode())
          print("[Sended] " + rst)
        else:
          rst = repr(emt1) + ", " + repr(emt2) + "\n"
          s.send(rst.encode())
          print("[Sended] " + rst)
      elif (lenArr == 3):
        rst = repr(ansArr[0]) + ", " + repr(ansArr[1]) + ", " + repr(ansArr[2]) + "\n"
        s.send(rst.encode())
        print("[Sended] " + rst)
  
if __name__ == "__main__":
  main()
