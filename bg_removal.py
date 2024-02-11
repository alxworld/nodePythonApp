import os
import numpy as np
import cv2
from PIL import Image
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# from matplotlib.widgets import Slider  # import the Slider widget

DATA_DIR = '/home/alex/nodePythonApp/images/'
DEST_DIR = os.path.join(DATA_DIR, 'OUTPUT')

# Get all files in directory
dir_list = os.listdir(DATA_DIR)

# Count the number of files in Source Directory
def getnumber(list):
    count = 0
    for element in list:
        count += 1
    return count


# Replace file extension to png
def replace(image):
	base = os.path.splitext(image)[0]
	post=os.path.splitext(image)[1]
	#print('The file name is ' + base + ' the extension is ' + post)
	# ima = os.rename(image, base + ".png")
	ima = image.replace(post,'.png')
	#print(image)
	return ima

Numfiles = getnumber(dir_list)

#print('Creating destination directory')

#Create destination directory
#print(DEST_DIR)
if not os.path.exists(DEST_DIR):
	#print ('Creating Dest Folder: ',DEST_DIR)
	os.makedirs(DEST_DIR)
	print('Output directory %s created' % DEST_DIR)

#threshold = input("Enter a number between 1 and 400: ")

i=0
while i!= Numfiles:
  # Get file name
	image=dir_list[i]
	# folder location and image
	src_path = os.path.join(DATA_DIR, image)
	#print(src_path,DEST_DIR)
	if src_path != DEST_DIR:
		img=cv2.imread(src_path)
		#print('Read image successfully')
		
		# *******REMOVE BACKGROUND*******
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY )
		blurred = cv2.GaussianBlur(gray, (7, 7), 0)
		_, threshed = cv2.threshold(blurred, 150, 210, cv2.THRESH_BINARY_INV)
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))
		morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
		
		cnts = cv2.findContours(morphed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
		cnt = sorted(cnts, key=cv2.contourArea)[-1]
		mask = cv2.drawContours(threshed, cnt, 0, (0, 255, 0), 0)
		masked_data = cv2.bitwise_and(img, img, mask=mask)
		x, y, w, h = cv2.boundingRect(cnt)
		dst = masked_data[y: y + h, x: x + w]
		
		# cv2.imshow('DST masked image', dst)
		# cv2.waitKey(0)
		
		dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
		
		# cv2.imshow('DST gray image', dst_gray)
		# cv2.waitKey(0)
		
		_, alpha = cv2.threshold(dst_gray, 0, 255, cv2.THRESH_BINARY)
		b, g, r = cv2.split(dst)
		rgba = [r, g, b, alpha]
		dst = cv2.merge(rgba, 4)
		
		# cv2.imshow('DST image', dst)
		# cv2.waitKey(0)
		
		#print(image)
		#print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
		#print('Writing file to Disk')
		#print(DEST_DIR)
		im = replace(image)
		#print (image,im)
		cv2.imwrite(os.path.join(DEST_DIR,im),dst)
		cv2.waitKey(0)
		#print('Image processing successful')
		#print('____________________________________________________')

	i += 1



# #DISPLAY BOTH SOURCE & BACKGRND REMOVED IMAGES
# # concatanate image Horizontally
# Hori = np.concatenate((img, dst), axis=1)
  
# # concatanate image Vertically
# Verti = np.concatenate((img, dst), axis=0)

# cv2.imshow('HORIZONTAL', Hori)
# cv2.imshow('VERTICAL', Verti)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print('Image Processing Completed.')