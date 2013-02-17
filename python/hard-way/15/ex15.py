from sys import argv

# get the file name
script, filename = argv

# open a new file
txt = open(filename)

print "Here's your file %r:" % filename
print txt.read()
txt.close()

print "I'll also ask you to type it again:"
file_again = raw_input("> ")

txt_again = open(file_again)

print txt_again.read()
txt_again.close()
