import Constants
class Confidence:
	def __init__(self):
		self.confidenceRect = [0,0,0,0] # The rect in question
		self.confidence = [0] # The (0-100) Rating that is given to a contour which determines how likely it is to be the target
		self.tolerance = Constants.CONFIDENCE_TOLERANCE # To use confidenceRect when confidence is above this amount