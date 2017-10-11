#!/bin/python
import sys, random, math, operator

try:
	from PIL import Image, ImageChops, ImageDraw
except:
	print("Python Image Library not found, install it with `pip install Pillow`")
	exit(1)

#@profile
def main():
	sys.argv += [False]*4

	if not sys.argv[1]:
		print("Usage: python convert.py image.png [iterations] [circle radius] [output filename]")
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

	#@profile
	def polydraw(image):
		# get random x and y within image
		x = random.randint(0, img.size[0]-1)
		y = random.randint(0, img.size[1]-1)

		# draw within the image using a color from unique set
		draw = ImageDraw.Draw(image)
		draw.ellipse((x-r, y-r, x+r, y+r), fill=random.choice(colors))
	
	#@profile
	def compare(im1, im2):
		# uses root mean squared analysis
		# see http://code.activestate.com/recipes/577630-comparing-two-images/
		diff = ImageChops.difference(im1, im2)
		h = diff.histogram()
		sq = (value*(idx**2) for idx, value in enumerate(h))
		sum_of_squares = sum(sq)
		rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
		return rms

	rounds = int(sys.argv[2] or 2500)
	for x in range(rounds):
		# draw a random polygon in image1
		polydraw(image1)

		# compare them to source (img)

		# this is what takes the most time, maybe by spawning two subprocceses can we double the speed

		compareQueue = Queue.Queue(maxsize=2) # two comparisons , two threads

		a = compare(img, image1)
		b = compare(img, image2)

		# if image1 is more similar, copy it to image2
		if a <= b:
			image2 = image1.copy()
		else:
			image1 = image2.copy()

		# report progress every 100 iterations
		if x % 100 == 0 and x != 0:
			print("%d/%d iterations performed, %.02f%% done" % (x, rounds, round(float(x)/rounds*100)))

	filename = sys.argv[4] or "output.png"
	image1.save(filename)
	print("Done, resulting image saved to %s" % filename)

if __name__ == "__main__":
    main()