class TreeNode(object):
	def __init__(self, value):
		self.left = None
		self.right = None
		self.parent = None
		self.value = value

def insert(root, value):
	node = TreeNode(value)
	p = root
	q = root
	while p is not None:
		if value < p.value:
			q = p
			p = p.left
		else:
			q = p
			p = p.right
	if value < q.value:
		q.left = node
	else:
		q.right = node
	node.parent = q

def inorder2(root):
	downing = True
	c = root
	while c is not None:
	 	if downing:
	 		if c.left is not None:
	 			c = c.left
				continue
			else:
	 			print("-%d" % c.value)
				if c.right is not None:
	 				c = c.right
					continue
				else:
	 				downing = False
					continue
		else:
			if c.parent is None:
				return
			if c == c.parent.left:
				print("-%d" % c.parent.value)
				c = c.parent.right
				downing = True
			else:
				c = c.parent

def inorder(root):
	if root is None:
		return
	inorder(root.left)
	print("%s," % root.value)
	inorder(root.right)

def main():
	root = TreeNode(7)
	for value in [1,3,18, 4, 6]:
		insert(root, value)
	inorder(root)
	inorder2(root)

if __name__ == '__main__':
	main()

