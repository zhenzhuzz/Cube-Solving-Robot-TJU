#include "config.h"
#include "Arduino.h"

int timegap = 1;            //步进电机转速调节
#define startgap 100        //步进电机起始转速
#define gapa 1              //步进电机加速度
#define range 12800 * 5 / 3 //步进电机转角范围

#define leftDir 0   //leftDir
#define leftMove 1  //leftMove
#define leftEn 2    //leftEn
#define rightDir 3  //rightDir
#define rightMove 4 //rightMove
#define rightEn 5   //rightEn

void motor_Init() //步进电机初始化
{
    pinMode(leftDir, OUTPUT); //控制方向
    pinMode(rightDir, OUTPUT);
    pinMode(leftMove, OUTPUT); //控制动力
    pinMode(rightMove, OUTPUT);
    pinMode(leftEn, OUTPUT);
    pinMode(rightEn, OUTPUT);
    digitalWrite(leftEn, 0);
    digitalWrite(rightEn, 0);
    delay(500);
    digitalWrite(leftEn, 1);
    digitalWrite(rightEn, 1);
}

void motorcl(bool lr, bool dir, int ang) //控制电机旋转，lr 0为左 1为右，dir 0为逆 1为顺，ang 旋转的角度
{
    int move;
    if (lr)
    {
        digitalWrite(rightDir, dir);
        move = rightMove;
    }
    else
    {
        digitalWrite(leftDir, dir);
        move = leftMove;
    }
    int count = 0;
    for (int gap = startgap; gap > timegap; gap -= gapa)
    {
        digitalWrite(move, HIGH);
        delayMicroseconds(gap);
        digitalWrite(move, LOW);
        delayMicroseconds(gap);
        count += 1;
    }
    for (int i = count; i < (ang * range - count); i++)
    {
        digitalWrite(move, HIGH);
        delayMicroseconds(timegap);
        digitalWrite(move, LOW);
        delayMicroseconds(timegap);
    }
    for (int gap = timegap; gap < startgap; gap += gapa)
    {
        digitalWrite(move, HIGH);
        delayMicroseconds(gap);
        digitalWrite(move, LOW);
        delayMicroseconds(gap);
    }
}

void motoroc(bool oc) //控制电机使能
{
    if (oc)
    {
        digitalWrite(leftEn, HIGH);
        digitalWrite(rightEn, HIGH);
    }
    else
    {
        digitalWrite(leftEn, LOW);
        digitalWrite(rightEn, LOW);
    }
}

void motorwt(bool lr, bool dir, int ang) //控制电机微调
{
    int move;
    if (lr)
    {
        digitalWrite(rightDir, dir);
        move = rightMove;
    }
    else
    {
        digitalWrite(leftDir, dir);
        move = leftMove;
    }
    for (int c = 0; ang > c; c += 1)
    {
        digitalWrite(move, HIGH);
        delayMicroseconds(3);
        digitalWrite(move, LOW);
        delayMicroseconds(3);
    }
}
