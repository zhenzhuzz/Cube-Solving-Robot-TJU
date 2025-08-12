import time
import serial
import kociemba
from msvcrt import getch

color_ex = {
    "U": "241335662",
    "B": "454412266",
    "L": "565163122",
    "F": "325554414",
    "D": "133426311",
    "R": "623341556",
}


class CubeSolver:
    def __init__(self, serialPort="COM5", baudRate=115200, timegap=1, msp=100, mtp=70):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.SerialUSB = serial.Serial(serialPort, baudRate, timeout=0.5)
        print("-----" * 9)
        if not self.SerialUSB.is_open:
            print("cannot open {}!".format(self.serialPort))
            quit()
        print("Successfully open {}!".format(self.serialPort))
        self.SerialUSB.write(
            (
                "[start"
                + "("
                + str(timegap)
                + ")"
                + "("
                + str(msp)
                + ")"
                + "("
                + str(mtp)
                + ")"
                + "]"
            ).encode("utf-8")
        )
        for i in range(4):
            print(self.detectString(self.SerialUSB))

    def run(self, color):
        start_time = time.time()
        print("-----" * 27)
        try:
            step = self.get_step(self.color_switch(color))

        except ValueError:
            print("魔方无解，颜色识别错误")
            return False
        else:
            print('识别完成，按下回车开始！')
            while True:
                Input = getch()
                if Input == b'\r':
                    break
            self.SerialWrite('c')
            time.sleep(1)
            self.SerialWrite(step)
            self.SerialWrite("end")
            self.time_record(start_time)
            print("-----" * 9)
            return True

    def color_switch(self, color):
        sequence = (
            color["U"] + color["R"] + color["F"] + color["D"] + color["L"] + color["B"]
        ).lower()
        U, R, F, D, L, B = sequence[4:53:9]
        dic = {U: "U", R: "R", F: "F", D: "D", L: "L", B: "B"}
        for char in dic:
            sequence = sequence.replace(char, dic[char])
        return sequence

    def get_step(self, sequence):
        SolveSteps = kociemba.solve(sequence)
        SolveSteps = SolveSteps.split(" ")
        l = len(SolveSteps)
        for i in range(l):
            if len(SolveSteps[i]) == 1:
                SolveSteps[i] = SolveSteps[i] + "1"
        print("SolveSteps:")
        print(SolveSteps)
        return self.step_switch(SolveSteps)

    def step_switch(self, Steps):
        stepNum = len(Steps)
        for k in range(stepNum):
            if Steps[k][0] == "R":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "U":
                        Steps[j] = "R" + Steps[j][1]
                    elif Steps[j][0] == "R":
                        Steps[j] = "D" + Steps[j][1]
                    elif Steps[j][0] == "D":
                        Steps[j] = "L" + Steps[j][1]
                    elif Steps[j][0] == "L":
                        Steps[j] = "U" + Steps[j][1]
            elif Steps[k][0] == "U":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "U":
                        Steps[j] = "D" + Steps[j][1]
                    elif Steps[j][0] == "R":
                        Steps[j] = "L" + Steps[j][1]
                    elif Steps[j][0] == "D":
                        Steps[j] = "U" + Steps[j][1]
                    elif Steps[j][0] == "L":
                        Steps[j] = "R" + Steps[j][1]
            elif Steps[k][0] == "L":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "U":
                        Steps[j] = "L" + Steps[j][1]
                    elif Steps[j][0] == "R":
                        Steps[j] = "U" + Steps[j][1]
                    elif Steps[j][0] == "D":
                        Steps[j] = "R" + Steps[j][1]
                    elif Steps[j][0] == "L":
                        Steps[j] = "D" + Steps[j][1]
            elif Steps[k][0] == "B":
                for j in range(k + 1, stepNum):
                    if Steps[j][0] == "F":
                        Steps[j] = "B" + Steps[j][1]
                    elif Steps[j][0] == "R":
                        Steps[j] = "L" + Steps[j][1]
                    elif Steps[j][0] == "B":
                        Steps[j] = "F" + Steps[j][1]
                    elif Steps[j][0] == "L":
                        Steps[j] = "R" + Steps[j][1]
            elif Steps[k][0] in ["F", "D"]:
                None
            else:
                print("{} goes wrong, please check!".format(Steps[k][0]))
                quit()
        print("SwitchSteps:")
        print(Steps)
        return Steps

    def detectString(self, com):
        while not com.in_waiting:
            continue
        rstr = str(com.readline(), encoding="utf-8")
        if rstr[0] == "[" and rstr[-3] == "]":
            return rstr[1:-3]
        else:
            print("Please check arduino!")
            return False

    def SerialWrite(self, Steps):
        if isinstance(Steps, str):
            self.SerialUSB.write(("[" + Steps + "]").encode("utf-8"))
            if self.detectString(self.SerialUSB):
                return True
            else:
                return False
        for step in Steps:
            self.SerialUSB.write(("[" + step + "]").encode("utf-8"))
            print(step, "successfully sent!")

    def time_record(self, start_time):
        while 1:
            step = self.detectString(self.SerialUSB)
            if step == "end":
                print("还原结束，总用时:", format(time.time() - start_time, ".3f"))
                break
            print(step, "用时:", format(time.time() - start_time, ".3f"))

    def close(self):
        self.SerialUSB.write("[close]".encode("utf-8"))
        print(self.detectString(self.SerialUSB))
        self.SerialUSB.close()
        print("-----" * 9)

'''
test = cube_solve(serialPort="COM5", timegap=1, msp=100, mtp=70)
test.SerialWrite("c")
time.sleep(3)
while 1:
    if not test.run(color_ex, 1):
        print("重新识别")
    else:
        break
test.close()
'''