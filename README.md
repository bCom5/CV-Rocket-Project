Computer Vision Rocket Project
By Adam Noworolski (Sc2ad)

The majority of important code is in the "Filter.py" and "picamTest.py"
If you want to run the code on your own computer, first clone the repo, then run the virtualenv by running this shell command: "source cv/bin/activate"
next, cd into cv/src and run the shell command: "python contourTest.py"
This will run the filter and display the varying outputs of each image that is listed in 'imgs' variable. NOTE: Place new images in cv/src/img/ folder.
If you get an error complaining about 'cv2', you need to download opencv onto your computer. Do a Google search for "Download OpenCV 2 in a virtualenv on (your OS)"

To build and run the code on the PI: Plug the PI in to the computer with the source code on it.
On the pi, run the shell script at "/home/pi/piip". THIS MUST BE DONE BEFORE YOU CAN SSH OR SCP TO THE PI.
If you are having problems logging into the pi, on the login screen press "CTRL+FN+F1" then type: "sudo startx"
After a short delay, the PI will login.
After logging in, copy over the entire repo (this repo) to the pi and place it in the Documents folder. You can name it whatever you want, but remember the name. Reccomended name would be RocketProject.
Make sure inside the 'RocketProject' folder there are all the virtualenv scripts, as well as the cv folder.
Most likely, when running the various scripts, you will encounter errors about cv2 and picamera. These modules need to be downloaded onto the PI. Instructions for this will be written soon.
For picamera, you can use sudo apt-get. (Picamera version 1.1)
For Opencv, make sure you install the correct version (version 2.4.9.1).
After running the shell script, go onto the computer and run the shell script at: "cv/src/copytopi" NOT TO BE CONFUSED WITH "cv/src/movetopi". There are 3 arguments that can be passed to movetopi.

1. Source directory: The directory of the source files to copy. Default: "/Users/jmn/.virtualenvs/cv/src"
2. Destination usr@IP: The Destination IP of the PI: Default: "root@192.168.1.2:/hom/pi/Documents/RocketProject/cv/src"
3. Filetype to copy: The extension of the file to copy to the pi. Default: "*.py"

Filter.py consists of three filters:

1. Simple Thresholding: If pixel is over a certain intensity, passes the filter.
2. Adaptie Thresholding: Thresholding with various options such as mean, otsu, etc.
3. (WHAT IS CURRENTLY USED) RGB Thresholding: If pixel's R, G, and B values are over certain values, it passes the filter.

Filter.py consists of 3 other custom made classes:

1. Constants: Where all the Filter.run(frame) constants are placed as well as RGB Filter constants. To change the actual filters, change the Constants values here, or add more Constants values and change the reference to the Constants value.
2. Confidence: Consists of the Rectangle and how confident the filter is that the rectangle contains the target. Helps speed up the filter by using less than 5% of the original image for another sample once it sees the baloon.
3. SaveableImage (Deprecated): Provides handling for saving, showing, and destroying images once the filter runs on them.

Filter.run(frame): Filters the contours that have already been found from 1 of the 3 filters as listed above.
Filter.run consists of several stages:

1. For each of the contours, runs through and tries to see how much it matches. If the contour passes every test (as listed in Constants.py), the contour is given a confidence of 100. Otherwise it is given a slightly smaller number depending on how many of the tests it passes.
2. Runs through all of the contours that passed the tests and got confidence values by selecting the highest confidence value contour, if there are two equally confident contours, it chooses the larger one.
3. Eliminates the remainder of the confidence rectangles, only leaving the ONE contour that has the highest confidence.
4. Changes the confidence rectangle to accomadate a slight window (in this case 25 pixels (can be changed in Constants) on all edges of the contour are included in the confidence rectangle)
5. When the RGB filter is next run, the confidence rectangle is used instead of the full image.
6. Draws the contours back onto the image. This is not important anymore, only for display purposes. Can be removed.

picamTest.py consists of a few key steps:

1. Runs indefinetly (until CTRL+C is pressed, or until numFrames is exceeded)
2. For each frame:
3. Converts to BGR Opencv image
4. Runs the RGB filter
5. Runs Filter.run
6. Clears the current image so the camera can continue sampling
7. When it ends, it outputs all the known information of time per frame and capture to the screen and to "cv/src/outputs.txt", where data from every test is collected.


That is essentially all that is needed to understand this code. If you have any questions, email me at adamznow@gmail.com.
