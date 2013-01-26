import java.awt.*;
import java.util.ArrayList;

public class Obstacles {
	private static final int BOX_LENGTH = 12;

	private ArrayList boxes;
	private WormChase wcTop;

	public Obstacles(WormChase wc) {
		boxes = new ArrayList();
		wcTop = wc;
	}

	synchronized public void add(int x, int y) {
		boxes.add(new Rectangle(x, y, BOX_LENGTH, BOX_LENGTH));
		wcTop.setBoxNumber(boxes.size()); // report new number of boxes
	}

	// does p intersect with any of the obstacles?
	synchronized public boolean hits(Point p, int size) {
		Rectangle r = new Rectangle(p.x, p.y, size, size);
		Rectangle box;
		for (int i = 0; i < boxes.size(); ++i) {
			box = (Rectangle) boxes.get(i);
			if (box.intersects(r))
				return true;
		}
		return false;
	} // end of intersect()

	// draw a series of blue boxes
	synchronized public void draw(Graphics g) {
		Rectangle box;
		g.setColor(Color.blue);
		for (int i = 0; i < boxes.size(); ++i) {
			box = (Rectangle) boxes.get(i);
			g.fillRect(box.x, box.y, box.width, box.height);
		}
	} // end of draw();

	synchronized public int getNumObstacles() {
		return boxes.size();
	}
}
