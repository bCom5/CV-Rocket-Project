class Confidence:
	def __init__(self):
		self.confidenceRect = [] # The rect in question
		self.confidence = [] # The (0-100) Rating that is given to a contour which determines how likely it is to be the target
		self.tolerance = 80 # To use confidenceRect when confidence is above this amount
	def update(self, confidence, confidenceRect):
		self.confidence = confidence
		self.confidenceRect = confidenceRect