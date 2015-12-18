def qr_check_format(fmt):
	g = 0x537
	for i in range(4, -1, -1):
		if fmt & (1 << (i+10)):
			print "fmt %s." % format(fmt, "#0b")
			fmt ^= g << i
	return fmt

def hamming_weight(x):
	weight = 0
	while x > 0:
		weight += x & 1
		x = x>>1
	return weight

def qr_decode_format(fmt):
	best_fmt = -1
	best_dist = 15
	for test_fmt in range(0, 32):
		test_code = (test_fmt<<10) ^ qr_check_format(test_fmt<<10)
		test_dist = hamming_weight(fmt ^ test_code)
		if test_dist < best_dist:
			best_dist = test_dist
			best_fmt = test_fmt
		elif test_dist == best_dist:
			best_fmt = -1
	return best_fmt

def gf_add(x, y):
	return x ^ y

def gf_sub(x, y):
	return x ^ y # in bin

def cl_mus(x, y):
	z = 0
	i = 0
	while (y>>i) > 0:
		if y & (1<<i):
			z ^= x<<i
		i += 1
	return z

def gf_mult_noLUT(x, y, prim=0):
	'''Multiplication in Galois Fields without using a precomputed look-up table 
	(and thus it's slower) 
		by  using the standard carry-less multiplication + modular reduction using an 
	irreducible prime polynomial'''

	### Define bitwise carry-less operations as inner functions ###
	def cl_mult(x,y):
		'''Bitwise carry-less multiplication on integers'''
		z = 0
		i = 0
		while (y>>i) > 0:
			if y  & (1<<i):
				z ^= x<<i
			i += 1
		return z
	
	def bit_length(n):
		''' Compute the position of the most signification bit (1) of an integer.
		Equivalent to int.bit_length()'''
		bits = 0
		while n>>bits : bits += 1
		return bits
	
	def cl_div(dividend, divisor=None):
		''' Bitwise carry-less long division on integers and returns the remainder'''
		# Compute the position of the most significant bit for each integers
		dl1 = bit_length(dividend)
		dl2 = bit_length(divisor)
		# If the dividend is smaller the the divisor, just exit
		if dl1 < dl2:
			return dividend 
		# Else, align the most signification 1 of the divisor to the most significant 1 of the dividend (by shifting the divisor)
		for i in range(dl1 - dl2, -1, -1):
			if dividend & (1 << i + dl2 - 1):
				# If divisible, then shift the divisor to align the most si
				dividend ^= divisor << i
		return dividend

	### Main GF multiplication routine ###

	# Mulitply the gf Numbers
	result = cl_mult(x,y)
	# Then do a modular reduction (ie, remainder from division) with an irreducible primitive polynomial so that is stays inside GF bounds
	if prim > 0:
		result = cl_div(result, prim)
	return result




