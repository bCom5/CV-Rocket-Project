from SaveableImage import SaveableImage as si
import numpy as np
import cv2

class Filter:
	# Class to handle ALL dealings with any and all thresholds and images, works with video as well
	def __init__(self, image, display=True, consts={}):
		# Image (as an object, NOT a filename)
		# Display: Boolean to display unnescessary details
		# Consts: Constants that are nescessary for filtering the correct contours
		self.image = image
		self.original = image
		self.moments = []
		self.contours = None # Sets contours later
		self.saveable = si(image) # Creates SaveableImage object
		self.display = display
		self.consts = consts
		self.allContours = [] # List of all contours and what they passed in terms of the filter
		self.acceptedContours = [] # List of the indexes of the contours that passed the filter
	def blur(self):
		# Blurs the image, as well as makes it grayscale
		grayimg = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) # Converts image to grayscale
		blur = cv2.GaussianBlur(grayimg,(5,5),0) # Blurs the image 5x5 Averaging Gaussian
		return blur # Returns blurred image
	def setContours(self, contours):
		self.contours = contours # Sets class contours to the contours passed to it
	def getContours(self, approx, threshLow=127, threshHigh=255, finalThreshVal=0):
		# Approx: How the contours should be approximated as: See 'contourTest.py' for more details
		# ThreshLow: Pixel must be above this to pass threshold
		# ThreshHigh: Pixel must be below this to pass threshold
		# FinalThreshVal: Type of thresholding to be done (OTSU VS BINARY) See 'contourTest.py' for more details
		blur = self.blur() # Blurs the image
		r, t = cv2.threshold(blur,threshLow,threshHigh,finalThreshVal) # Standard threshold
		thresh = np.copy(t) # Creates a copy of the threshold to do contour drawing on it
		i, cont, h = cv2.findContours(t, cv2.RETR_TREE, approx) # Finds contours of the filtered result
		self.setContours(cont) # Sets the contours
		return r, thresh, i, cont, h # Returns Ret, Thresholded Image, Image with contours, Hiearchy
	def adaptiveGet(self, approx, threshHigh=255, size=11, c=2, filterType=cv2.ADAPTIVE_THRESH_MEAN_C):
		# Approx: How the contours should be approximated as: See 'contourTest.py' for more details
		# ThreshHigh: High threshold ending value
		# Size: Size of the adaptive threshold
		# C: Amount toi subtract from the average of the pixels when thresholding is complete
		# FilterType: Type of filter to use: See 'contourTest.py' for more details
		blur = self.blur() # Blurs the image
		t = cv2.adaptiveThreshold(blur,threshHigh,filterType,cv2.THRESH_BINARY,size,c) # Does Adaptive threshold on the image
		thresh = np.copy(t) # Copies threshold result
		i, cont, h = cv2.findContours(t, cv2.RETR_TREE, approx) # Finds contours on threshold result
		self.setContours(cont) # Sets contours
		return thresh, i, cont, h # Returns Thresholded Image, Image with contours, Hiearchy
	def rgbGet(self, approx, consts={}):
		# Approx: How the contours should be approximated as: See 'contourTest.py' for more details
		# Consts: Dictionary of constants for the RGB filter: See 'contourTest.py' for more detials
		blur = cv2.GaussianBlur(self.image, (5,5), 0) # Blurs without converting to gray image
		B, G, R = cv2.split(blur) # Splices the image into the Blue Green and Red pixel values
		B[B > consts['rgbBlueMax']] = 0 # Blue pixels above the threshold turn to 0
		B[B < consts['rgbBlueMin']] = 0 # Blue pixels below the threshold turn to 0
		G[B == 0] = 0 # Green pixels that share the same index as Blue pixels that are 0 also become 0
		R[B == 0] = 0 # Same with Red
		B[B > 0] = 255 # Remaining Pixels get converted to White (255,255,255)
		G[B > 0] = 255
		R[B > 0] = 255
		end = cv2.merge([B, G, R]) # Merges results back together into one image
		grayimg = cv2.cvtColor(end, cv2.COLOR_BGR2GRAY) # Converts to grayscale binary image (so contours works on it)
		thresh = np.copy(grayimg) # Copies the Binary image
		i, cont, h = cv2.findContours(grayimg, cv2.RETR_TREE, approx) # Finds the contours on the binary image after the RGB filter
		self.setContours(cont) # ...
		return thresh, i, cont, h # ...
	def run(self, Image, color=(0,255,0)):
		# Image: image object to pass through to the function: allows filter to work with video frames
		# Color: Color to draw contours in (not any of the other contour related things, however)
		# RETURNS ORIGINAL IMAGE WITH CONTOURS THAT PASS THE FILTER DRAWN IN
		# FILTER:
		self.original = np.copy(Image) # Sets the original image to the image just passed through
		index = 0 # Resets index to 0
		for item in self.contours: # For each contour
			image2 = np.copy(self.original) # Copies the original image (image2 is image that everything gets drawn on)
			# MOMENTS
			M = cv2.moments(item) # Moments matrix of the contour, everything the contour is
			# Draw Contours
			cv2.drawContours(image2, [item], 0, color, 2) # Draws the contour on the image
			try:
				# Center X
				cx = int(M['m10']/M['m00'])
				# Center Y
				cy = int(M['m01']/M['m00'])
			except ZeroDivisionError:
				# Area  is 0
				cx = 0
				cy = 0
			# Area
			A = cv2.contourArea(item)

			# Perimeter
			P = cv2.arcLength(item, True)

			# Actual convex polygon
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
			try:
				# Line
				rows, cols = image2.shape[:2]
				[vx, vy, x, y] = cv2.fitLine(item, cv2.DIST_L2,0,0.01,0.01)
				lefty = int((-x*vy/vx) + y)
				righty = int(((cols-x)*vy/vx)+y)
				image2 = cv2.line(image2, (cols-1,righty),(0,lefty),(0,255,0),2)
			except OverflowError:
				# Line exists outside of the image, numbers are too small
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
				solidity = float(A)

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
				}) # The dictionary of all the contour information- most time consuming, but is not nescessary
			# Not all of the information is currently used, jsut there for reference

			if self.display:
				# Don't display anything because video feeds make it annoyingly slow (when displaying stuff in this loop)
				pass
				#self.saveable.showRaw("Item "+str(index))
				#self.saveable.testKey()
			index += 1 # Increments index of contour (only needed for display purposes, deprecated)

		# BEGIN FILTER TEST
		acceptances = []
		index = 0 # Resets index to 0
		for item in self.moments: # For all of the contour information, check if they pass the conditionals with the constants passed in the initialization:
			# Check self.consts and current item to see if it passes the filtering threshold for each value
			# Add an item representing that to 'contourStuff' if it does
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
			acceptance = len(contourStuff) # Acceptance calculated by length of 'contourStuff', how much stuff got put into it
			acceptances.append(acceptance) # All Possibilities are appended to acceptances
			if acceptance >= self.consts['tolerance']: # If the acceptance exceeds the tolerance, accept the contour
				# CONTOUR PASSES FILTER
				if self.display: print "ACCEPTED CONTOUR "+str(index)
				self.acceptedContours.append(index)
			contourStuff.insert(0,index) # Insert the index (readability)
			self.allContours.append(contourStuff)
			index += 1 # Indecrement the index
		for item in self.allContours:
			if self.display: print "\nContour: ", item[0] # Prints out the contour information, how much each contour matched
			for item2 in item:
				if self.display: print item2,
		image2 = np.copy(self.original)
		print 
		print acceptances # Print the acceptance values of all the contours
		#image2 = cv2.imread(filename)
		for item in self.acceptedContours:
			cv2.drawContours(image2, [self.contours[item]], -1, color, 3) # Draw the accepted contours
			try:
				defects = cv2.convexityDefects(self.contours[item],self.moments[item]['hull']) # Try to draw the convex hull
			except:
				defects = cv2.convexityDefects(self.contours[item],cv2.convexHull(self.contours[item],returnPoints=False)) # Otherwise, tries with a reobtaining of the hull
			try:
				for i in range(defects.shape[0]): # Tries to draw the defects of the convex hull
				    s,e,f,d = defects[i,0]
				    start = tuple(self.contours[item][s][0])
				    end = tuple(self.contours[item][e][0])
				    far = tuple(self.contours[item][f][0])
				    cv2.line(image2,start,end,[0,255,255],2)
			    #cv2.circle(image2,far,5,[255,0,255],-1)
			except AttributeError: # If it fails print it out
				print "Attribute Failure!"
		return image2 # Returns image with accepted contours drawn on it