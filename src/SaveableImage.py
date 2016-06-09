#Saveable Image Handler
import numpy as np
import cv2
class SaveableImage:
	def __init__(self,imageName):
		try:
			self.image = cv2.imread(imageName)
		except:
			self.image = imageName
		self.title = ''
		self.saved = False
	def save(self, outputName):
		cv2.imwrite(outputName,self.image)
		self.display("Image has been saved as: "+str(outputName))
		self.saved = True
	def showRaw(self, title=''):
		if title != '':
			self.title = title
		self.display("Image has been displayed as: '"+self.title+"'")
		cv2.imshow(self.title,self.image)
	def waitRaw(self, ticks=0):
		self.display("Waiting for: "+str(ticks)+" ticks")
		return cv2.waitKey(ticks) & 0xFF
	def destroyAll(self):
		cv2.destroyAllWindows()
		self.display("ALL Windows have been destroyed")
	def destroy(self, title=''):
		if title != '':
			self.title = title
		self.display("Window with title: '"+self.title+"' has been destroyed")
		cv2.destroyWindow(self.title)
	def shape(self):
		return self.image.shape
	def testKey(self, saveKey='s', quitKey='q', outputName=''):
		k = self.waitRaw()
		if k == ord(saveKey):
			if outputName == '':
				outputName = raw_input("Name of file to save image:\n>>> ")
			self.save(outputName)
		elif k == ord(quitKey):
			if self.saved:
				self.display("Already saved! Quitting ALL Windows...")
			else:
				self.display("Not saved! Press '"+saveKey+"' to save the image or press any other key to quit without saving")
				k = self.waitRaw()
				if k == ord(saveKey):
					if outputName == '':
						outputName = raw_input("Name of file to save image:\n>>> ")
					self.save(outputName)
			self.destroyAll()
		else:
			self.testKey()
	def display(self, message=''):
		print message
	def openImage(self, inputName='img/input.jpg'):
		self.image = cv2.imread(inputName)