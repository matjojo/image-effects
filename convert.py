#!/bin/python
import sys, random, math, operator, queue, threading
from datetime import datetime
try:
	from PIL import Image, ImageChops, ImageDraw
except:
	print("Python Image Library not found, install it with `pip install Pillow`")
	exit(1)

print(str(datetime.now()))

#@profile
def main():
	sys.argv += [False]*4

	if not sys.argv[1]:
		print("Usage: python convert.py [image filename] [iterations] [circle radius] [output filename]")
		exit(1)

	# open image
	img = Image.open(sys.argv[1])
	pixels = img.convert("RGBA")

	# get unique pixel colors
	colors = list(set(img.getdata()))

	# make two new images
	image1 = Image.new(img.mode, img.size, "white")
	image2 = Image.new(img.mode, img.size, "white")

	r = int(sys.argv[3] or 25)

#	@profile
	def polydraw(image):
		# get random x and y within image
		x = random.randint(0, img.size[0]-1)
		y = random.randint(0, img.size[1]-1)

		# draw within the image using a color from unique set
		colour = random.choice(colors)
		ImageDraw.Draw(image).ellipse((x-r, y-r, x+r, y+r), fill=colour) # after maybe split out the random and see if that can be made faster

#	@profile
	def compare(im1, im2, threadID, result_queue):
		# uses root mean squared analysis
		# see http://code.activestate.com/recipes/577630-comparing-two-images/
		diff = ImageChops.difference(im1, im2)
		h = diff.histogram()
		sq = (value*(idx**2) for idx, value in enumerate(h))
		sum_of_squares = sum(sq)
		rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
		result_queue.put((threadID, rms))

	rounds = int(sys.argv[2] or 2500)
	for x in range(rounds):
		# draw a random polygon in image1
		polydraw(image1)

		# compare them to source (img)
		compareQueue = queue.Queue(maxsize=2) # two comparisons , two threads
		threads = [threading.Thread(target=compare, args=(img, image1, 0, compareQueue), daemon=True), threading.Thread(target=compare, args=(img, image2, 1, compareQueue), daemon=True)]
		
		for th in threads:
			th.start()
		
		# report progress every 100 iterations
		if x % 100 == 0 and x != 0:
			print("%d/%d iterations performed, %.02f%% done" % (x, rounds, round(float(x)/rounds*100)))
													# micro-optimization, since we are waiting anyway, why not write the results for the first one and print already		
		results = [0, 0]
		results[0] = compareQueue.get()
		
		resultssorted = [0, 0]
		resultssorted[results[0][0]] = results[0][1] # we sort the results by making use of the fact that the first [0] slot in the table is the threadID, this ID we then use to determine

		results[1] = compareQueue.get()
		resultssorted[results[1][0]] = results[1][1] # the spot it gets in the sorted table, thus making sure that the first [0] slot in that table is the one from the first [0] thread


		a = resultssorted[0]
		b = resultssorted[1]

		# if image1 is more similar, copy it to image2
		if a <= b:
			image2 = image1.copy()
		else:
			image1 = image2.copy()



	filename = sys.argv[4] or str("output_" + str(rounds) + "_" + str(r) + ".png")
	image1.save(filename)
	print("Done, resulting image saved to %s" % filename)

if __name__ == "__main__":
	main()