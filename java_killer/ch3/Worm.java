import java.awt.*;
import java.awt.geom.*;

public class Worm {
	private static final int DOTSIZE = 12;
	private static final int RADIUS = DOTSIZE / 2;
	private static final int MAXPOINTS = 40;

	// compass direction/bearing constants
	private static final int NUM_DIRS = 8;
	private static final int N = 0;
	private static final int NE = 1;
	private static final int E = 2;
	private static final int SE = 3;
	private static final int S = 4;
	private static final int SW = 5;
	private static final int W = 6;
	private static final int NW = 7;

	private int currCompass; // stores the current compass dir/bearing

	// Stores the increments in each of the compass dirs.
	// An Increment is added to the old head position to get the
	// new position.
	Point2D.Double incrs[];

	// probabiliy info for selecting a compass dir.
	private static final int NUM_PROBS = 9;
	private int probsForOffset[];

	// cells[] stores the dots making up the worm
	// it is treated like a circular buffer
	private Point cells[];
	private int nPoints;
	private int tailPosn, headPosn; // the tail and head of the buffer

	private int pWidth, pHeight; // panel dimensions;
	private long startTime; // in ms
	private Obstacles obs;

	public Worm(int pW, int pH, Obstacles os) {
		pWidth = pW;
		pHeight = pH;
		obs = os;
		cells = new Point[MAXPOINTS];
		nPoints = 0;
		headPosn = -1;
		tailPosn = -1;

		// increments for each compass dir
		incrs = new Point2D.Double[NUM_DIRS];
		incrs[N] = new Point2D.Double(0.0, -1.0);
		incrs[NE] = new Point2D.Double(0.7, -0.7);
		incrs[E] = new Point2D.Double(1.0, 0.0);
		incrs[SE] = new Point2D.Double(0.7, 0.7);
		incrs[S] = new Point2D.Double(0.0, 1.0);
		incrs[SW] = new Point2D.Double(-0.7, 0.7);
		incrs[W] = new Point2D.Double(-1.0, 0.0);
		incrs[NW] = new Point2D.Double(-0.7, -0.7);

		// probability info for selecting a compass dir.
		//		0 = no chage, -1 means 1 step anti-clockwise,
		//		1 means 1 step clockwise, etc.
		/* The array means that usually the worm continues in 
		 * the same direction but may bear slightly to the left
		 * or right
		 */
		probsForOffset = new int[NUM_PROBS];
		probsForOffset[0] = 0;
		probsForOffset[1] = 0;
		probsForOffset[2] = 0;
		probsForOffset[3] = 1;
		probsForOffset[4] = 1;
		probsForOffset[5] = 2;
		probsForOffset[6] = -1;
		probsForOffset[7] = -1;
		probsForOffset[8] = -2;
	} // end of Worm()

	// is (x, y) near the worm's head?
	public boolean nearHead(int x, int y) {
		if (nPoints > 0) {
			if (Math.abs(cells[headPosn].x + RADIUS - x) <= DOTSIZE
					&& Math.abs(cells[headPosn].y + RADIUS - y) <= DOTSIZE) {
				return true;
					}
		}
		return false;
	} // end of nearHead();

	// is (x, y) near any part of the worm's body?
	public boolean touchedAt(int x, int y) {
		int i = tailPosn;
		while (i != headPosn) {
			if (Math.abs(cells[i].x + RADIUS - x) <= RADIUS
					&& Math.abs(cells[i].y + RADIUS - y) <= RADIUS) {
				return true;
			}
			i = (i + 1) % MAXPOINTS;
		}
		return false;
	} // end of touchedAt();

	// draw a black wrom with a red head
	public void draw(Graphics g) {
		if (nPoints > 0) {
			g.setColor(Color.black);
			int i = tailPosn;
			while (i != headPosn) {
				g.fillOval(cells[i].x, cells[i].y, DOTSIZE, DOTSIZE);
				i = (i + 1) % MAXPOINTS;
			}
			g.setColor(Color.red);
			g.fillOval(cells[headPosn].x, cells[headPosn].y, DOTSIZE, DOTSIZE);
		}
	} // end of draw();

	public void move() {
		int prevPosn = headPosn;
		// save old head posn while creating new one
		headPosn = (headPosn + 1) % MAXPOINTS;

		if (nPoints == 0) {
			tailPosn = headPosn;
			currCompass = (int) (Math.random() * NUM_DIRS);
			cells[headPosn] = new Point(pWidth/2, pHeight/2);
			nPoints++;
		} else if (nPoints == MAXPOINTS) {
			tailPosn = (tailPosn + 1) % MAXPOINTS;
			newHead(prevPosn);
		} else {
			newHead(prevPosn);
			nPoints++;
		}
	} // end of move();

	private void newHead(int prevPosn) {
		int fixedOffs[] = {-2, -2, -4}; // offests to avoid obstacle
		int newBearing = varyBearing();
		Point newPt = nextPoint(prevPosn, newBearing);

		if (obs.hits(newPt, DOTSIZE)) {
			for (int i = 0; i < fixedOffs.length; ++i) {
				newBearing = calcBearing(fixedOffs[i]);
				newPt = nextPoint(prevPosn, newBearing);
				if (!obs.hits(newPt, DOTSIZE))
					break;
			}
		}
		cells[headPosn] = newPt; // new head position
		currCompass = newBearing; // new compass direction
	} // end of newHead();

	// Use the offset to calculate a new compass bearing
	// based on the current compass direction.
	private int calcBearing(int offset) {
		int turn = currCompass + offset;
		if (turn >= NUM_DIRS) {
			turn = turn - NUM_DIRS;
		} else if (turn < 0) {
			turn = NUM_DIRS + turn;
		}
		return turn;
	} // end of calcBearing();

	// vary the compass bearing semi-randomly
	private int varyBearing() {
		int newOffset = probsForOffset[ (int) (Math.random() * NUM_PROBS) ];
		return calcBearing(newOffset);
	} // end of varyBearing();

	// Return the next coordinate based on the previsou position
	// and compass bearing.
	//
	// Convert the compass bearing into predetermined increments
	// (sotred in incrs[]). Add the increments nultiplied by the
	// DOTSIZE to the old head position.
	// Deal with wraparound
	private Point nextPoint(int prevPosn, int bearing) {
		// get the increments for the compass bearing
		Point2D.Double incr = incrs[bearing];

		int newX = cells[prevPosn].x + (int)(DOTSIZE * incr.x);
		int newY = cells[prevPosn].y + (int)(DOTSIZE * incr.y);

		// modify newX/newY if < 0, or > pWidth/pHeight; use wraparound
		if (newX + DOTSIZE < 0) {
			newX = newX + pWidth;
		} else if (newX > pWidth) {
			newX = newX - DOTSIZE;
		}

		if (newY + DOTSIZE < 0) {
			newY = newY + pHeight;
		} else if (newY > pHeight) {
			newY = newY - pHeight;
		}

		return new Point(newX, newY);
	}

}
