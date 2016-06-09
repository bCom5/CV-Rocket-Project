#Saveable Image Handler
import numpy as np
import cv2
class SaveableImage:
	def __init__(self,imageArray):
		self.image = imageArray
		self.title = ''
		self.saved = False
	def showRaw(self, title):
		self.title = title
		cv2.imshow(title,self.image)
	def waitRaw(self, ticks):
		return cv2.waitKey(ticks) & 0xFF
	def destroyAll(self):
		cv2.destroyAllWindows()
	def destroy(self, title=''):
		cv2.destroyWindow(title)
	def testKey(self, saveKey='s', quitKey='q', outputName='img/output.png'):
		k = waitRaw(0)
		if k == ord(saveKey):
			cv2.imwrite(outputName,self.image)
			self.saved = True
		elif k == ord(quitKey):
			if self.saved:
				destroyAll()
			else:
				k = waitRaw(0)
				if k == ord(saveKey):
					cv2.imwrite(outputName,self.image)
					self.saved = True
				destroyAll()
		else:
			testKey()