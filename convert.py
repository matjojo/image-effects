#!/usr/bin/python

import sys, random, math, operator, queue, threading
from datetime import datetime
try:
	from PIL import Image, ImageChops, ImageDraw
except:
	print("Python Image Library not found, install it with `pip install Pillow`")
	exit(1)
timestart = str(datetime.now())
print(timestart)

#@profile
def main():
	lastcompareresult = False
	sys.argv += [False]*5

	if not sys.argv[1]:
		print("Usage: python convert.py [image filename] [output filename] [iterations] [shape ('line', 'ellipse', 'pieslice')] [line length minimum or ellipse radius] [line length maximum] [line width] ")
		exit(1)

	# open image
	img = Image.open(sys.argv[1])
	pixels = img.convert("RGBA")

	# get unique pixel colors
	colors = list(set(img.getdata()))

	# make two new images
	image1 = Image.new(img.mode, img.size, "white")
	image2 = Image.new(img.mode, img.size, "white")

	lilengthmin_or_elli_rad = int(sys.argv[5] or 1)
	lilengthmax = int(sys.argv[6] or 5)
	liwidth = int(sys.argv[7] or 5)

	if sys.argv[4] == "ellipse":
#		@profile
		def polydraw(image):
			# get random x and y within image
			x1 = random.randint(0, img.size[0]-1)
			y1 = random.randint(0, img.size[1]-1)

			# draw within the image using a color from unique set
			colour = random.choice(colors)
			ImageDraw.Draw(image).ellipse((x-lilengthmin_or_elli_rad, y-lilengthmin_or_elli_rad, x, y), fill=colour)

	elif sys.argv[4] == "line":
#		@profile
		def polydraw(image):
			# get random x and y within image
			LTx = random.randint(0, img.size[0]-1)
			LTy = random.randint(0, img.size[1]-1)

			RBx = LTx + lilengthmax
			RBy = LTy + lilengthmax

			# RBx = random.randint(LTx, (LTx+lilengthmax,img.size[0]-1)[LTx+lilengthmax>img.size[0]-1]) # result = (on_false, on_true)[condition] since bool goes to 0 or 1 when used as index in tuple
			# RBy = random.randint(LTy, (LTy+lilengthmax,img.size[1]-1)[LTx+lilengthmax>img.size[1]-1])

			# draw within the image using a color from unique set
			colour = random.choice(colors)
			ImageDraw.Draw(image).line((LTx, LTy, RBx, RBy), width=liwidth, fill=colour) # after maybe split out the random and see if that can be made faster


#	@profile
	def compare(im1, im2):
		# uses root mean squared analysis
		# see http://code.activestate.com/recipes/577630-comparing-two-images/
		diff = ImageChops.difference(im1, im2)
		h = diff.histogram()
		sq = (value*(idx*idx) for idx, value in enumerate(h))
		sum_of_squares = sum(sq)
		rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
		return rms

	# setup compare with white image as the first comparison
	lastcompareresult = compare(img, image2)

	rounds = int(sys.argv[3] or 2500)
	for x in range(rounds):
		# draw a random polygon in image1
		polydraw(image1)


		# compare them to source (img)
		a = compare(img, image1)

		# if image1 is more similar, copy it to image2
		if a <= lastcompareresult:
			image2 = image1.copy()
			lastcompareresult = a
		else:
			image1 = image2.copy()
			# lastcompareresult = lastcompareresult

		# report progress every 100 iterations
		if x % 100 == 0 and x != 0:
			print("%d/%d iterations performed, %.02f%% done" % (x, rounds, round(float(x)/rounds*100)))		


	filename = sys.argv[2] or str("output_" + str(rounds) + "_" + str(r) + ".png")
	image1.save(filename)
	print("Done, resulting image saved to %s" % filename)
	print("Starting time was: %s" % timestart)
	print("Current time is: %s" % str(datetime.now()))

if __name__ == "__main__":
	main()