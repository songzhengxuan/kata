class TreeNode(object):

	def __init__(self, left=0, right=0, data=0):
		self.left = left;
		self.right = right;
		self.data = data;

class BTree(object):

	def __init__(self, root=0):
		self.root = root;
	
	def is_empty(self):
		if self.root is 0:
			return True
		else:
			return False
	
	def insert_node(self, newnode, rootnode):
		if newnode.data < rootnode.data:
			if rootnode.left is 0:
				rootnode.left = newnode
			else:
				self.insert_node(newnode, rootnode.left)
		elif newnode.data > rootnode.data:
			if rootnode.right is 0:
				rootnode.right = newnode
			else:
				self.insert_node(newnode, rootnode.right);

	def insert(self, newdata):
		treenode = TreeNode(data = newdata)
		if self.root is 0:
			self.root = treenode
			return
		else:
			self.insert_node(treenode, self.root)


	def create(self):
		while True:
			temp = raw_input('enter a value:')
			if temp is '#':
				return 0
			self.insert(temp)

	def inorder_node(self, node, outfile):
		if node.left is not 0:
			line = '%s -> %s;\n' % (node.data, node.left.data)
			outfile.write(line)
			print node.data, '->', node.left.data, ';'
			self.inorder_node(node.left, outfile)
		if node.right is not 0:
			line = '%s -> %s;\n' % (node.data, node.right.data)
			outfile.write(line)
			print node.data, '->', node.right.data, ';'
			self.inorder_node(node.right, outfile)

	def inorder(self):
		if self.root is 0:
			return
		outfile = open('output.dot', 'w')
		outfile.write('digraph Tree {\n');
		self.inorder_node(self.root, outfile)
		outfile.write('}\n');

bt = BTree()
bt.create()
bt.inorder();

