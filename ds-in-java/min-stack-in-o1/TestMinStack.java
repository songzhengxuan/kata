import junit.framework.TestCase;

public class TestMinStack extends TestCase {
    MinStack<Long> mStack;

    public void setUp() {
        mStack = new MinStack<Long>();
    }

    public void tearDown() {
        mStack = null;
    }

    public void testTest() {
        mStack.push(Long.valueOf(3));
        mStack.push(Long.valueOf(1));
        mStack.push(Long.valueOf(-1));
        mStack.push(Long.valueOf(2));
        mStack.push(Long.valueOf(3));
        mStack.push(Long.valueOf(1));
        assertEquals(Long.valueOf(-1), mStack.getMin());
        assertEquals(Long.valueOf(1), mStack.peek());
    }

}
