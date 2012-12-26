import java.util.Stack;

public class MinStack<E extends Comparable<? super E>> {
    private Stack<E> mElements = new Stack<E>();
    private Stack<E> mMinValues = new Stack<E>();

    public void push(E newValue) {
        mElements.push(newValue);

        if (mMinValues.isEmpty()) {
            mMinValues.push(newValue);
            return;
        }

        if (mMinValues.peek().compareTo(newValue) >= 0) {
            mMinValues.push(newValue);
        }
    }

    public E peek() {
        E result = mElements.peek();
        return result;
    }

    public E getMin() {
        return mMinValues.peek();
    }

    public void pop() {
        E result = mElements.pop();
        if (mMinValues.peek().compareTo(result) == 0) {
            mMinValues.pop();
        }
    }

    public boolean isEmpty() {
        return mElements.isEmpty();
    }
}
