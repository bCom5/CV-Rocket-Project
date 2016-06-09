from SaveableImage import SaveableImage as si
import numpy as np
import cv2

class Filter:

	def __init__(self, image, display=True, consts={}):
		self.image = image
		self.original = image
		self.moments = []
		self.contours = None
		self.saveable = si(image)
		self.display = display
		self.consts = consts
		self.allContours = []
		self.acceptedContours = []
	def getContours(self, approx, threshLow=127, threshHigh=255, finalThreshVal=0):
		blur = self.blur()
		r, t = cv2.threshold(blur,threshLow,threshHigh,finalThreshVal)
		thresh = t
		cv2.imshow('thresh', thresh)
		i, cont, h = cv2.findContours(t, cv2.RETR_TREE, approx)
		self.setContours(cont)
		return r, thresh, i, cont, h
	def adaptiveGet(self, approx, threshHigh=255, size=11, c=2, filterType=cv2.ADAPTIVE_THRESH_MEAN_C):
		blur = self.blur()
		t = cv2.adaptiveThreshold(blur,threshHigh,filterType,cv2.THRESH_BINARY,size,c)
		thresh = np.copy(t)
		cv2.imshow('thresh', thresh)
		i, cont, h = cv2.findContours(t, cv2.RETR_TREE, approx)
		self.setContours(cont)
		return thresh, i, cont, h
	def rgbGet(self, approx, consts={}):
		# [131,202,9,90] --> B
		blur = cv2.GaussianBlur(self.image, (5,5), 0)
		B, G, R = cv2.split(blur)
		B[B > consts['rgbBlueMax']] = 0
		B[B < consts['rgbBlueMin']] = 0
		G[B == 0] = 0
		R[B == 0] = 0
		B[B > 0] = 255
		G[B > 0] = 255
		R[B > 0] = 255
		end = cv2.merge([B, G, R])
		grayimg = cv2.cvtColor(end, cv2.COLOR_BGR2GRAY)
		thresh = np.copy(grayimg)
		i, cont, h = cv2.findContours(grayimg, cv2.RETR_TREE, approx)
		self.setContours(cont)
		return thresh, i, cont, h
	def setContours(self, contours):
		self.contours = contours
	def blur(self):
		grayimg = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(grayimg,(5,5),0)
		return blur
	def run(self, Image, color=(0,255,0)):
		# RETURNS ORIGINAL IMAGE WITH CONTOURS THAT PASS THE FILTER DRAWN IN
		# FILTER:
		self.original = np.copy(Image)
		#self.original = Image
		index = 0
		for item in self.contours:
			image2 = np.copy(self.original)
			# MOMENTS
			M = cv2.moments(item)
			# Draw Contours
			cv2.drawContours(image2, [item], 0, color, 2)
			try:
				# Center X
				cx = int(M['m10']/M['m00'])
				# Center Y
				cy = int(M['m01']/M['m00'])
			except ZeroDivisionError:
				# Area  is 0
				#IGNORE ME
				cx = 0
				cy = 0
			# Area
			A = cv2.contourArea(item)

			# Perimeter
			P = cv2.arcLength(item, True)

			# Actual convex
			hull = cv2.convexHull(item,returnPoints=False)

			# Is Convex?
			k = cv2.isContourConvex(item)

			# Normal Bounding Rect
			x, y, w, h = cv2.boundingRect(item)
			cv2.rectangle(image2, (x,y), (x+w,y+h), (0,255,0), 2)

			# Angled Rect
			rect = cv2.minAreaRect(item)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			cv2.drawContours(image2,[box], 0, (255,0,0), 2)

			# Circle
			(x,y), radius = cv2.minEnclosingCircle(item)
			center = (int(x),int(y))
			radius = int(radius)
			image2 = cv2.circle(image2, center, radius, (0,255,255), 2)

			try:
				# Ellipse

				ellipse = cv2.fitEllipse(item)
				image2 = cv2.ellipse(image2, ellipse, (255,255,0), 2)

				# Orientation
				(x,y), (MA,ma), angle = cv2.fitEllipse(item)

			except:
				# NOT FIVE OR MORE POINTS
				angle = 0
				MA = 1
				ma = 1
				pass
			try:
				# Line
				rows, cols = image2.shape[:2]
				[vx, vy, x, y] = cv2.fitLine(item, cv2.DIST_L2,0,0.01,0.01)
				lefty = int((-x*vy/vx) + y)
				righty = int(((cols-x)*vy/vx)+y)
				image2 = cv2.line(image2, (cols-1,righty),(0,lefty),(0,255,0),2)
			except OverflowError:
				pass

			# Aspect Ratio
			aspect_ratio = float(w)/h

			# Extent
			rect_area = w*h
			extent = float(A)/rect_area

			try:
				# Solidity
				hull_area = cv2.contourArea(hull)
				solidity = float(A)/hull_area
			except:
				solidity = 1.0

			# Equivalent Diameter
			eD = np.sqrt(4*A/np.pi)

			# Mask + Pixel Points
			grayimg = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
			mask = np.zeros(grayimg.shape,np.uint8)
			cv2.drawContours(mask,[item],0,255,-1)
			pixelPoints = cv2.findNonZero(mask)

			# Maximum and Minimum
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(grayimg,mask=mask)

			# Mean Color/Intensity
			mean = cv2.mean(image2, mask=mask)

			# Extreme Points
			leftMost = tuple(item[item[:,:,0].argmin()][0])
			rightMost = tuple(item[item[:,:,0].argmax()][0])
			topMost = tuple(item[item[:,:,1].argmin()][0])
			bottomMost = tuple(item[item[:,:,1].argmax()][0])

			self.saveable.image = image2
			# Add to moments
			self.moments.append({
				'cx': cx,
				'cy': cy,
				'A': A,
				'P': P,
				'k': k,
				'w': w,
				'h': h,
				'hull': hull,
				'ratio': aspect_ratio,
				'extent': extent,
				'solidity': solidity,
				'eD': eD,
				'angle': angle,
				'majorAxis': MA,
				'minorAxis': ma,
				'mask': mask,
				'pixelPoints': pixelPoints,
				'maxVal': max_val,
				'maxLocation': max_loc,
				'minVal': min_val,
				'minLocation': min_loc,
				'mean': mean,
				'leftMost': leftMost,
				'rightMost': rightMost,
				'topMost': topMost,
				'bottomMost': bottomMost
				})
			if self.display:
				pass
				#self.saveable.showRaw("Item "+str(index))
				#self.saveable.testKey()
			index += 1

		# BEGIN FILTER TEST
		acceptances = []
		index = 0
		for item in self.moments:
			contourStuff = []
			if item['A'] < self.consts['maxArea']: 
				contourStuff.insert(0,"GOOD maxArea\t")
			if item['A'] > self.consts['minArea']:
				contourStuff.insert(1,"GOOD minArea\t")
			if item['P'] < self.consts['maxPerimeter']:
				contourStuff.insert(2,"GOOD maxPerimeter\t")
			if item['P'] > self.consts['minPerimeter']:
				contourStuff.insert(3,"GOOD minPerimeter\t")
			if item['w'] < self.consts['maxWidth']:
				contourStuff.insert(4,"GOOD maxWidth\t")
			if item['w'] > self.consts['minWidth']:
				contourStuff.insert(5,"GOOD minWidth\t")
			if item['h'] < self.consts['maxHeight']:
				contourStuff.insert(6,"GOOD maxHeight\t")
			if item['h'] > self.consts['minHeight']:
				contourStuff.insert(7,"GOOD minHeight\t")
			if item['ratio'] < self.consts['maxRatio']:
				contourStuff.insert(8,"GOOD maxRatio\t")
			if item['ratio'] > self.consts['minRatio']:
				contourStuff.insert(9,"GOOD minRatio\t")
			if item['extent'] < self.consts['maxExtent']:
				contourStuff.insert(10,"GOOD maxExtent\t")
			if item['extent'] > self.consts['minExtent']:
				contourStuff.insert(11,"GOOD minExtent\t")
			if item['solidity'] < self.consts['maxSolidity']:
				contourStuff.insert(12,"GOOD maxSolidity\t")
			if item['solidity'] > self.consts['minSolidity']:
				contourStuff.insert(13,"GOOD minSolidity\t")
			if item['mean'][0] < self.consts['maxMean']:
				contourStuff.insert(14,"GOOD maxMean\t")
			if item['mean'][0] > self.consts['minMean']:
				contourStuff.insert(15,"GOOD minMean\t"+str(item['mean']))
			if len(item['pixelPoints']) < self.consts['maxVerticies']:
				contourStuff.insert(16,"GOOD maxVerticies\t")
			if len(item['pixelPoints']) > self.consts['minVerticies']:
				contourStuff.insert(17,"GOOD minVerticies\t"+str(len(item['pixelPoints'])))
			if item['angle'] < self.consts['maxAngle']:
				contourStuff.insert(18,"GOOD maxAngle\t")
			if item['angle'] > self.consts['minAngle']:
				contourStuff.insert(19,"GOOD minAngle\t")
			if item['w'] / float(image2.shape[0]) < self.consts['maxRatioWidthtoSize']:
				contourStuff.insert(20,"GOOD maxRatioWidthtoSize\t")
			if item['w'] / float(image2.shape[0]) > self.consts['minRatioWidthtoSize']:
				contourStuff.insert(21,"GOOD minRatioWidthtoSize\t")
			if item['h'] / float(image2.shape[1]) < self.consts['maxRatioHeighttoSize']:
				contourStuff.insert(22,"GOOD maxRatioHeighttoSize\t")
			if item['h'] / float(image2.shape[1]) > self.consts['minRatioHeighttoSize']:
				contourStuff.insert(23,"GOOD minRatioHeighttoSize\t")
			acceptance = len(contourStuff)
			acceptances.append(acceptance)
			if acceptance >= self.consts['tolerance']:
				# CONTOUR PASSES FILTER
				if self.display: print "ACCEPTED CONTOUR "+str(index)
				self.acceptedContours.append(index)
			contourStuff.insert(0,index)
			self.allContours.append(contourStuff)
			index += 1
		for item in self.allContours:
			if self.display: print "\nContour: ", item[0]
			for item2 in item:
				if self.display: print item2,
		image2 = np.copy(self.original)
		print 
		print acceptances
		#image2 = cv2.imread(filename)
		for item in self.acceptedContours:
			cv2.drawContours(image2, [self.contours[item]], -1, color, 3)
			try:
				defects = cv2.convexityDefects(self.contours[item],self.moments[item]['hull'])
			except:
				defects = cv2.convexityDefects(self.contours[item],cv2.convexHull(self.contours[item],returnPoints=False))
			try:
				for i in range(defects.shape[0]):
				    s,e,f,d = defects[i,0]
				    start = tuple(self.contours[item][s][0])
				    end = tuple(self.contours[item][e][0])
				    far = tuple(self.contours[item][f][0])
				    cv2.line(image2,start,end,[0,255,255],2)
			    #cv2.circle(image2,far,5,[255,0,255],-1)
			except AttributeError:
				print "CAUGHT ONE!"
				continue
		return image2