## CONSTANTS FILE: FOR EASY ACCESS TO ANY AND ALL CONSTANTS FOR CONTOUR MAPPINGS AND VIDEO MAPPINGS
PHOTOS_CONTOUR_FILTER_CONSTANTS_1 = {
# CLOSE FILTER
	'minArea' : 5,
	'maxArea' : 20000,
	'minPerimeter' : 5,
	'maxPerimeter' : 3000,
	'minWidth' : 2,
	'maxWidth' : 600,
	'minHeight' : 3,
	'maxHeight' : 300,
	'minRatio' : 0.0,
	'maxRatio' : 1000.0,
	'minExtent' : 0.27,
	'maxExtent' : 0.9,
	'minSolidity' : 0.390,
	'maxSolidity' : 1000.0,
	'minMean' : 0.0,
	'maxMean' : 255.0,
	'minVerticies' : 10,
	'maxVerticies' : 10200,
	'minAngle' : -360.0,
	'maxAngle' : 360.0,
	'minRatioWidthtoSize' : 0.02,
	'maxRatioWidthtoSize' : 0.4,
	'minRatioHeighttoSize' : 0.02,
	'maxRatioHeighttoSize' : 0.4,
	'tolerance' : 24 # Number of above conditions to be met for successful contour observation
}
PHOTOS_CONTOUR_FILTER_CONSTANTS_2 = {
# FAR FILTER
	'minArea' : 2,
	'maxArea' : 1300,
	'minPerimeter' : 2,
	'maxPerimeter' : 800,
	'minWidth' : 1,
	'maxWidth' : 300,
	'minHeight' : 1,
	'maxHeight' : 200,
	'minRatio' : 0.0,
	'maxRatio' : 1000.0,
	'minExtent' : 0.21,
	'maxExtent' : 0.8,
	'minSolidity' : 0.390,
	'maxSolidity' : 1000.0,
	'minMean' : 0.0,
	'maxMean' : 255.0,
	'minVerticies' : 5,
	'maxVerticies' : 10000,
	'minAngle' : -360.0,
	'maxAngle' : 360.0,
	'minRatioWidthtoSize' : 0.015,
	'maxRatioWidthtoSize' : 0.25,
	'minRatioHeighttoSize' : 0.01,
	'maxRatioHeighttoSize' : 0.25,
	'tolerance' : 24 # Number of above conditions to be met for successful contour observation
}
PHOTOS_RGB_FILTER_CONSTANTS_1 = {
# CLOSE FILTER
	'rgbRedMin' : 104,
	'rgbRedMax' : 255,
	'rgbGreenMin' : 0,
	'rgbGreenMax' : 101,
	'rgbBlueMin' : 0,
	'rgbBlueMax' : 130
}
PHOTOS_RGB_FILTER_CONSTANTS_2 = {
# FAR FILTER
	'rgbRedMin' : 166,
	'rgbRedMax' : 255,
	'rgbGreenMin' : 0,
	'rgbGreenMax' : 166,
	'rgbBlueMin' : 0,
	'rgbBlueMax' : 170
}