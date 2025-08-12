#include "config.h"
#include "Arduino.h"

#define SerialUSB Serial

void serial_Init() //串口初始化
{

    SerialUSB.begin(115200);
    Serial1.begin(19200, SERIAL_8N1);
}

void serial_test() //串口测试
{
    while (1)
        if (SerialUSB.available())
            SerialUSB.print(SerialUSB.read());
}

void pos_Init() //位置初始化
{
    Serial1.print(0xe18000, HEX);
}

String detectString()
{
    while (SerialUSB.read() != '[')
        ;
    return (SerialUSB.readStringUntil(']'));
}

void cube_switch(String step);

void waitcmd() //等待命令
{
    String str;
    while (1)
    {
        if (SerialUSB.available())
        {
            str = detectString();
            if (str.substring(0, 5) == "start")
            {
                int i, s, e;
                int len = str.length();
                int c = 0;
                for (i = 5; i < len; i++)
                {
                    if (str[i] == '(')
                        s = i;
                    if (str[i] == ')')
                    {
                        e = i;
                        switch (c)
                        {
                        case 0:
                            timegap = str.substring(s + 1, e).toInt();
                            SerialUSB.println("[timegap:" + str.substring(s + 1, e)+']');
                            c += 1;
                            break;
                        case 1:
                            mspausetime = str.substring(s + 1, e).toInt();
                            SerialUSB.println("[mspausetime:" + str.substring(s + 1, e)+']');
                            c += 1;
                            break;
                        case 2:
                            mtpausetime = str.substring(s + 1, e).toInt();
                            SerialUSB.println("[mtpausetime:" + str.substring(s + 1, e)+']');
                            c += 1;
                            break;
                        }
                    }
                }
                SerialUSB.println("[Start cube switch!]");
                while (1)
                {
                    str = detectString();
                    if (str == "close")
                    {
                        SerialUSB.println("[Serial close!]");
                        break;
                    }
                    else if (str == "end")
                    {
                        cube_switch("o");
                        SerialUSB.println("[end]");
                    }
                    else
                    {
                        cube_switch(str);
                        SerialUSB.println("[cube " + str + ']');
                    }
                }
                break;
            }
        }
    }
}

void cube_switch(String step)
{
    if (step == "test")
    {
        pos_Init();
    }
    else if (step == "o")
    {
        grabcl(0, 0, 0);
        grabcl(1, 0, 0);
        motoroc(1);
    }
    else if (step == "c")
    {
        grabcl(0, 1, 0);
        grabcl(1, 1, 0);
        motoroc(0);
    }
    else if (step == "mo")
        motoroc(1);
    else if (step == "mc")
        motoroc(0);
    else if (step == "lc")
        grabcl(0, 1, 0);
    else if (step == "rc")
        grabcl(1, 1, 0);
    else if (step == "lz")
        spin(0, 1, 1);
    else if (step == "rz")
        spin(1, 1, 1);
    else if (step == "lt")
        motorwt(0, 0, 100);
    else if (step == "rt")
        motorwt(1, 0, 100);
    //还原步骤
    else if (step == "F1")
        twist(0, 0, 1);
    else if (step == "F'")
        twist(0, 1, 1);
    else if (step == "F2")
        twist(0, 1, 2);
    else if (step == "D1")
        twist(1, 0, 1);
    else if (step == "D'")
        twist(1, 1, 1);
    else if (step == "D2")
        twist(1, 1, 2);
    else if (step == "L1")
    {
        spin(0, 1, 1);
        twist(1, 0, 1);
    }
    else if (step == "L'")
    {
        spin(0, 1, 1);
        twist(1, 1, 1);
    }
    else if (step == "L2")
    {
        spin(0, 1, 1);
        twist(1, 1, 2);
    }
    else if (step == "R1")
    {
        spin(0, 0, 1);
        twist(1, 0, 1);
    }
    else if (step == "R'")
    {
        spin(0, 0, 1);
        twist(1, 1, 1);
    }
    else if (step == "R2")
    {
        spin(0, 0, 1);
        twist(1, 1, 2);
    }
    else if (step == "B1")
    {
        spin(1, 1, 2);
        twist(0, 0, 1);
    }
    else if (step == "B'")
    {
        spin(1, 1, 2);
        twist(0, 1, 1);
    }
    else if (step == "B2")
    {
        spin(1, 1, 2);
        twist(0, 1, 2);
    }
    else if (step == "U1")
    {
        spin(0, 1, 2);
        twist(1, 0, 1);
    }
    else if (step == "U'")
    {
        spin(0, 1, 2);
        twist(1, 1, 1);
    }
    else if (step == "U2")
    {
        spin(0, 1, 2);
        twist(1, 1, 2);
    }
}
