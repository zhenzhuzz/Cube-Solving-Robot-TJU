extern int timegap;     //步进电机转速调节
extern int mspausetime; //开关手的时间间隔
extern int mtpausetime; //电机的时间间隔
//步进电机控制
void motor_Init();                        //步进电机初始化
void motorcl(bool lr, bool dir, int ang); //控制电机旋转，lr 0为左 1为右，dir 0为逆 1为顺，ang 旋转的角度
void motoroc(bool oc);                    //控制电机使能
void motorwt(bool lr, bool dir, int ang); //控制电机微调
//mos管控制
void mos_Init();                            //mos管初始化
void grabcl(bool lr, bool oc, bool dl = 1); //控制手爪开闭，lr 0为左 1为右，oc 1为关 0为开
//还原步骤
void twist(bool lr, bool dir, int ang); //控制手爪拧魔方，lr 0为左 1为右，dir 0为逆 1为顺（由魔方看向），ang 旋转的角度
void spin(bool lr, bool dir, int ang);  //控制手爪旋转魔方，lr 0为左 1为右，dir 0为逆 1为顺（由魔方看向），ang 旋转的角度
//串口通信
void serial_Init(); //串口初始化
void pos_Init();    //位置初始化
void serial_test(); //串口测试
void waitcmd();     //等待命令
