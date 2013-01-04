from sys import argv

script, first, second, third = argv

print "The script is called:", script
print "Your first varibable is:", first;
print "Your second varibable is:", second;
print "Your third varibable is:", third;

extra_input = raw_input('Enter your extra input, enter "q" to quit:')
count = 3
while extra_input != 'q':
    count += 1
    print 'Your %d input is %s' % (count, extra_input)
    extra_input = raw_input('Enter your extra input, enter "q" to quit:')
    
