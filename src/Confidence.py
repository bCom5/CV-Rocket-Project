import Constants
class Confidence:
	def __init__(self):
		self.confidenceRect = [[0,0,0,0]] # The rect in question
		self.confidence = [0] # The (0-100) Rating that is given to a contour which determines how likely it is to be the target
		self.tolerance = Constants.CONFIDENCE_TOLERANCE # To use confidenceRect when confidence is above this amount
		self.usingConfidence = False
		self.imageVals = []
	def getxy(self, cond):
		x = self.confidenceRect[0][0] - Constants.CONFIDENCE_WINDOW_WIDTH/2.0
		if x < cond: x = cond
		y = self.confidenceRect[0][1] - Constants.CONFIDENCE_WINDOW_HEIGHT/2.0
		if y < cond: y = cond
		w = self.confidenceRect[0][2] + Constants.CONFIDENCE_WINDOW_WIDTH

		h = self.confidenceRect[0][3] + Constants.CONFIDENCE_WINDOW_HEIGHT

		return x, y, w, h