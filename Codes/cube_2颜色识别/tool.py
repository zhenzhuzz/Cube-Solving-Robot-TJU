import numpy as np
import win32gui, win32ui, win32con, win32api
from pywintypes import error as WindowCaptureError
import cv2 as cv
from time import time

def window_capture():

	hwnd_title = {}
	def get_all_hwnd(hwnd, mouse):
		if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
			hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

	win32gui.EnumWindows(get_all_hwnd, 0)
	for hwnd_, title in hwnd_title.items():
		if title[:3]=='OBS' :
			hwnd = hwnd_
			break

	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()
	saveBitMap = win32ui.CreateBitmap()
	left, top, right, bot = win32gui.GetWindowRect(hwnd)
	w = right - left
	h = bot - top
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
	saveDC.SelectObject(saveBitMap)
	saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
	signedIntsArray = saveBitMap.GetBitmapBits(True)
	img = np.frombuffer(signedIntsArray, dtype='uint8')
	img.shape = (h,w,4) 
	img = img[::,::,:3:]
	return img 

if __name__ == '__main__':
	img = window_capture()
	cv.imwrite('cube_fin.jpg', img)