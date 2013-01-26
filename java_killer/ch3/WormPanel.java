import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.text.DecimalFormat;

import com.sun.j3d.utils.timer.J3DTimer;

public class WormPanel extends JPanel implements Runnable {
	private static final int PWIDTH = 320;
	private static final int PHEIGHT = 240;

	private static long MAX_STATS_INTERVAL = 1000000000L;

	private static final int NO_DELAYS_PER_YIELD = 16;

	private static int MAX_FRAME_SKIPS = 5;

	private static int NUM_FPS = 10;

	// used for gathering statistics
	private long statsInterval = 0L;
	private long prevStatsTime;
	private long totalElapsedTime = 0L;
	private long gameStartTime;
	private int timeSpentInGame = 0;

	private long frameCount = 0;
	private double fpsStore[];
	private long statsCount = 0;
	private double averageFPS = 0.0;

	private long framesSkipped = 0L;
	private long totalFramesSkipped = 0L;
	private double upsStore[];
	private double averageUPS = 0.0;

	private Thread animator;	// the thread that performs the animation
	private boolean running = false; // use to stop 
	private boolean isPaused = false;

	private long period;

	private WormChase wcTop;
	private Worm fred;
	private Obstacles obs;

	// used at game termination
	private boolean gameOver = false;
	private int score = 0;
	private Font font;
	private FontMetrics metrics;

	// off screen rendering
	private Graphics dbg;
	private Image dbImage = null;

	public WormPanel(WormChase wc, long period) {
		wcTop = wc;
		this.period = period;

		setBackground(Color.white);
		setPreferredSize(new Dimension(PWIDTH, PHEIGHT));
		
		setFocusable(true);
		requestFocus();
		readyForTermination();

		// create game components
		obs = new Obstacles(wcTop);
		fred = new Worm(PWIDTH, PHEIGHT, obs);

		addMouseListener(new MouseAdapter() {
			public void mousePressed(MouseEvent e) {
				testPress(e.getX(), e.getY());
			}
		});

		// set up message font
		font = new Font("SansSerif", Font.BOLD, 24);
		metrics = this.getFontMetrics(font);

		gameRender();
	} // end of WormPanel()

	private void readyForTermination() {
		// listen for esc, q, end, ctrl-c on the canvas to 
		// allow a convenient exit from the full screen configuration
		addKeyListener(new KeyAdapter() {
			public void keyPressed(KeyEvent e) {
				int keyCode = e.getKeyCode();
				if (keyCode == KeyEvent.VK_ESCAPE
					|| keyCode == KeyEvent.VK_Q
					|| keyCode == KeyEvent.VK_END
					|| (keyCode == KeyEvent.VK_C && e.isControlDown())) {
					running = false;
				}
			}
		}); 

	}

	public void resumeGame() {
		
	}

	public void pauseGame() {

	}

	public void stopGame() {

	}

	private void testPress(int x, int y) {
		if (!isPaused && !gameOver) {
			if (fred.nearHead(x, y)) {
				gameOver = true;
				// hack together a score
				score = (40 - timeSpentInGame) + (40 - obs.getNumObstacles());
			} else { // add an obstacle if possible
				if (!fred.touchedAt(x, y)) {
					obs.add(x, y);
				}
			}
		}
	} // end of testPress();

	// The frames of the animation are drawn inside the while loop.
	public void run() {
		long beforeTime, afterTime, timeDiff, sleepTime;
		long overSleepTime = 0L;
		int noDelays = 0;
		long excess = 0L;

		gameStartTime = J3DTimer.getValue();
		prevStatsTime = gameStartTime;
		beforeTime = gameStartTime;

		running = true;

		while (running) {
			gameUpdate();
			gameRender();
			paintScreen();

			afterTime = J3DTimer.getValue();
			timeDiff = afterTime - beforeTime;
			sleepTime = (period - timeDiff) - overSleepTime;

			if (sleepTime > 0L) { // some time left in this cycle
				try {
					Thread.sleep(sleepTime / 1000000L);
				} catch (InterruptedException ex) {
				}
				overSleepTime = (J3DTimer.getValue() - afterTime) - sleepTime;
			} else { // sleepTime <= 0; the frame took longer than the period
				excess -= sleepTime;
				overSleepTime = 0L;
				if (++noDelays >= NO_DELAYS_PER_YIELD) {
					Thread.yield();
					noDelays = 0;
				}
			}

			beforeTime = J3DTimer.getValue();

			/**
			 * If frame animation is taking too long, update the game state
			 * without rendering it, to get the updates/sec nearer to
			 * the required FPS.
			 */
			int skips = 0;
			while ((excess > period) && (skips < MAX_FRAME_SKIPS)) {
				excess -= period;
				gameUpdate();
				skips++;
			}
			framesSkipped += skips;
		}
		System.exit(0);
	}

	private void gameUpdate() {
		if (!isPaused && !gameOver) {
			fred.move();
		}
	}

	private void gameRender() {
		if (dbImage == null) {
			dbImage = createImage(PWIDTH, PHEIGHT);
			if (dbImage == null) {
				System.out.println("dbImage is null");
				return;
			} else {
				dbg = dbImage.getGraphics();
			}
		}
		
		// clear the background
		dbg.setColor(Color.white);
		dbg.fillRect(0, 0, PWIDTH, PHEIGHT);

		dbg.setColor(Color.blue);
		dbg.setFont(font);

		obs.draw(dbg);
		fred.draw(dbg);
	}

	private void gameOverMessage(Graphics g) {

	}

	// use active rendering to put the buffered image on-screen
	private void paintScreen() {
		Graphics g;
		try {
			g = this.getGraphics();
			if ((g != null) && (dbImage != null)) {
				g.drawImage(dbImage, 0, 0, null);
			}
			g.dispose();
		} catch (Exception e) {
			System.out.println("Graphics context error: " + e);
		}
	}

	// wait for the JPanel to be added to the JFrame before starting
	public void addNotify() {
		super.addNotify(); // creates the peer
		startGame();	// start the thread
	}

	// initialise and start the thread
	private void startGame() {
		if (animator == null || !running) {
			animator = new Thread(this);
			animator.start();
		}
	} // end of startGame();

	private void storeStats() {

	}

	private void printStats() {

	}
}
