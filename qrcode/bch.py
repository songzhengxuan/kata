def qr_check_format(fmt):
	g = 0x537
	for i in range(4, -1, -1):
		if fmt & (1 << (i+10)):
			fmt ^= g << i
	return fmt
