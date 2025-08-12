#include "config.h"
#include "Arduino.h"

#define leftOpen 8  //leftOpen MOS1
#define rightOpen 9 //rightOpen MOS2
#define cubeput 10  //put MOS3

bool loc = 0;
bool roc = 0;
int mspausetime = 100; //开关手的时间间隔

void mos_Init() //mos管初始化
{
    pinMode(leftOpen, OUTPUT);  //控制左爪开闭 HIGH开LOW闭
    pinMode(rightOpen, OUTPUT); //控制右爪开闭 HIGH开LOW闭
    digitalWrite(leftOpen, 0);
    digitalWrite(rightOpen, 0);
}

void grabcl(bool lr, bool oc, bool dl) //控制手爪开闭，lr 0为左 1为右，oc 1为关 0为开
{
    if (lr)
    {
        if (oc != roc)
        {
            digitalWrite(rightOpen, oc);
            if (dl)
                delay(mspausetime);
            roc = oc;
        }
    }
    else
    {
        if (oc != loc)
        {
            digitalWrite(leftOpen, oc);
            if (dl)
                delay(mspausetime);
            loc = oc;
        }
    }
}
