public class BubbleSorter {
	private int operations = 0;
	private int length = 0
	private SortHandle itsSortHandle = null;

	public BubbleSorter(SortHandle handle) {
		itsSortHandle = handle;
	}

	public int sort(Object array) {
		itsSortHandle.setArray(array);
		length = itsSortHandle.length();
		operations = 0;

		while (1) {
			boolean hasOutOfOrder = false;
			for (int i = 0; i < length - 1; ++i) {
				if (itsSortHandle.outOfOrder(i)) {
					hasOutOfOrder = true;
					itsSortHandle.swap(i);
					++operations;
				}
			}
		}

		return operations;
	}
}
