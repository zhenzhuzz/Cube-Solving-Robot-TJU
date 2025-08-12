from cube import Cube 
from msvcrt import getch
import sys
from tool import window_capture
from getopt import getopt
from pywintypes import error as WindowCaptureError

serialUSB = 'COM3'
baudRate = 115200
mode = None
timegap=1
msp=100
mtp=70

try:
	opts, arg = getopt(args=sys.argv[1:], shortopts='ihs:b:', longopts=['mode=','msp','mtp','timegap'])
except getopt.GetoptError:
	print('参数设置错误，使用:\n"python main.py -h"\n查看用法')
	sys.exit()

assert opts != [] , '请输入参数，使用:\n"python main.py -h"\n查看用法'

def init():
	with open('./models/cnn_model.txt', 'w') as file:
		file.write('./models/cnn.h5')
	with open('./models/stacking_model.txt', 'w') as file:
		file.write('./models/StackingClassifier.pkl')

for opt, arg in opts:
	if opt == '-i':
		init()
	if opt == '-h':
		helper = '''使用方法：
python main.py --mode mode [-s serialUSB -b baudRate -i]
其中，mode为运行模式，train为训练模式，run为使用模式
serialUSB为Arduino端口，默认为com5
baudRate为Arduino波特率，默认为115200
i将初始化模型使用
请务必不要最小化OBS窗口'''
		print(helper)
		sys.exit()
	if opt == '--mode':
		mode = arg
	if opt == '-s':
		serialUSB = arg
	if opt == '-b':
		baudRate = int(arg)
	if opt == '--timegap':
		timegap =int(arg)
	if opt == '--msp':
		msp = int(msp)
	if opt == '--mtp':
		mtp = int(mtp)

assert mode in ['run', 'train', 'test'] , 'mode参数有误，使用:\n"python main.py -h"\n查看用法'

try:
	window_capture()
except WindowCaptureError:
	print('请打开OBS，使用:\n"python main.py -h"\n查看用法')
	sys.exit()

if mode == 'train':
	print('放置完成后，按下回车开始训练！')
	while True:
		Input = getch()
		if Input == b'\r':
			break

	cube = Cube(train=True, test=False, serialPort=serialUSB, baudRate=baudRate, timegap=timegap, msp=msp, mtp=mtp)
	cube.run()

if mode == 'run':
	'''
	print('所有模块加载完成，按下回车开始！')
	while True:
		Input = getch()
		if Input == b'\r':
			break
	'''
	cube = Cube(train=False, test=False, serialPort=serialUSB, baudRate=baudRate, timegap=timegap, msp=msp, mtp=mtp)
	cube.run()


if mode == 'test':
	print('所有模块加载完成，按下回车开始！')
	while True:
		Input = getch()
		if Input == b'\r':
			break

	cube = Cube(train=False, test=True, serialPort=serialUSB, baudRate=baudRate, timegap=timegap, msp=msp, mtp=mtp)
	cube.run()