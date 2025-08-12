#include "config.h"
#include "Arduino.h"

int mtpausetime = 70; //电机的时间间隔

void twist(bool lr, bool dir, int ang) //控制手爪拧魔方，lr 0为左 1为右，dir 0为逆 1为顺（由魔方看向），ang 旋转的角度
{
  motorcl(lr, dir, ang);
  if (ang % 2)
  {
    grabcl(lr, 0);
    motorcl(lr, !dir, 1);
    delay(mspausetime);
    grabcl(lr, 1);
  }
}

void spin(bool lr, bool dir, int ang) //控制手爪旋转魔方，lr 0为左 1为右，dir 0为逆 1为顺（由魔方看向），ang 旋转的角度
{
  grabcl(!lr, 0);
  motorcl(lr, dir, ang);
  delay(mspausetime);
  grabcl(!lr, 1);
  if (ang % 2)
  {
    grabcl(lr, 0);
    motorcl(lr, !dir, 1);
    delay(mspausetime);
    grabcl(lr, 1);
  }
}
