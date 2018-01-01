import png, array

# point = (2, 10) # coordinates of pixel to be painted red

def convert_dice(pixel):
	intervals = [20, 70, 120, 170, 220, 255]
	
	gray = pixel[0] # assuming pixel is grayscaled
	if gray < intervals[0]:
		return 6
	elif gray < intervals[1]:
		return 5
	elif gray < intervals[2]:
		return 4
	elif gray < intervals[3]:
		return 3
	elif gray < intervals[4]:
		return 2
	elif gray < intervals[5]:
		return 1
	else:
		raise Exception("WTF?")

def dice_image(pixels, dice_converter):
	res = []
	for col in pixels:
		res_col = []
		for pixel in col:
			res_col.append(dice_converter(pixel))
		res.append(res_col)
	return res

def convert_grayscale_lightness(pixel):
	return int((max(pixel) + min(pixel)) / 2)

def convert_grayscale_average(pixel):
	return int(sum(pixel) / 3)

def convert_grayscale_luminosity(pixel):
	R = pixel[0]
	G = pixel[1]
	B = pixel[2]
	return int(0.21 * R + 0.72 * G + 0.07 * B)

def get_average_of_pixels(pixels, grayscale_converter):
	sum_r = 0
	sum_g = 0
	sum_b = 0
	for pixel in pixels:
		sum_r += pixel[0]
		sum_g += pixel[1]
		sum_b += pixel[2]

	divident = len(pixels)
	pixels = [int(x/divident) for x in [sum_r, sum_g, sum_b]]
	
	grayscale = grayscale_converter(pixels)
	
	return [grayscale]*3

def grayscale_image(img_filename, grayscale_converter):	
	reader = png.Reader(filename=img_filename)
	w, h, pixels, metadata = reader.read_flat()
	pixel_byte_width = 4 if metadata['alpha'] else 3
	# pixel_position = point[0] + point[1] * w
	# new_pixel_value = (125, 0, 0, 0) if metadata['alpha'] else (255, 0, 0)
	print "Size: ", w, h
	birim = w / 15.0
	if not birim.is_integer():
		raise Exception("File size should be 15a X 20a!")
	birim = int(birim)

	res = []
	for j in range(20):
		row = []
		for i in range(15):
			block = []
			offset_x = i*birim
			offset_y = j*birim*w
			# print offset_x, offset_y
			for y in range(birim):
				for x in range(birim):
					pixel_position = offset_x + x + offset_y + y * w
					# print pixel_position,
					p = pixels[pixel_position * pixel_byte_width : 
						(pixel_position + 1) * pixel_byte_width]
					block.append([p[0], p[1], p[2]])
				# print "_"
			# print "finished"
			row.append(get_average_of_pixels(block, grayscale_converter))
		res.append(row)

	# printing pixels
	# for i in range(0, len(pixels), pixel_byte_width):
	#	 print pixels[i:i+pixel_byte_width]
	# pixels[
	#   pixel_position * pixel_byte_width :
	#   (pixel_position + 1) * pixel_byte_width] = array.array('B', new_pixel_value)

	# pixel_arrays = [[array.array('B', x) for x in res[y]] for y in range(len(res))]
	# print len(pixel_arrays)
	# output = open('composed.png', 'wb')
	# writer = png.Writer(15, 20, **metadata)
	# writer.write_array(output, pixel_arrays)
	# output.close()

	return res

res = grayscale_image("irem.png", convert_grayscale_luminosity)
dice_res = dice_image(res, convert_dice)

for row in dice_res:
	for pixel in row:
		print pixel,
	print