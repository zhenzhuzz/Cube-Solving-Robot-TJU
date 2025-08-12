/*
由开发板向手臂看去，左边的为左臂，右边的的为右臂
由左臂向魔方看去，上面为U面，下面为F面
*/
#include "config.h"

void setup()
{
  motor_Init();
  mos_Init();
  serial_Init();
}

void loop()
{
  waitcmd();
}
