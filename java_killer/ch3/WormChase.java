import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class WormChase extends JFrame implements WindowListener {
	private static final int DEFAULT_FPS = 10;
	
	private WormPanel wp;
	private JTextField jtfBox;
	private JTextField jtfTime;

	public WormChase(long peroid) {
		super("The Worm Chase");
		makeGUI(peroid);

		addWindowListener(this);
		pack(); // first one (the GUI doesn't include the JPanel yet)

		setResizable(false);
		setVisible(true);
	}

	private void makeGUI(long peroid) {
		Container c = getContentPane();

		wp = new WormPanel(this, peroid);
		c.add(wp, "Center");

		JPanel ctrls = new JPanel();
		ctrls.setLayout(new BoxLayout(ctrls, BoxLayout.X_AXIS));

		jtfBox = new JTextField("Boxes used: 0");
		jtfBox.setEditable(false);
		ctrls.add(jtfBox);

		jtfTime = new JTextField("TIme Spent: 0 secs");
		jtfTime.setEditable(false);
		ctrls.add(jtfTime);

		c.add(ctrls, "South");
	}

	public void setBoxNumber(int no) {
		jtfBox.setText("Boxes used: " + no);
	}

	public void setTimeSpent(long t) {
		jtfTime.setText("Time spent: " + t + " secs");
	}

	// --------------- window listener methods---------------------------
	public void windowActivated(WindowEvent e) {
		wp.resumeGame();
	}

	public void windowDeactivated(WindowEvent e) {
		wp.pauseGame();
	}

	public void windowDeiconified(WindowEvent e) {
		wp.resumeGame();
	}

	public void windowIconified(WindowEvent e) {
		wp.resumeGame();
	}

	public void windowClosing(WindowEvent e) {
		wp.pauseGame();
	}

	public void windowClosed(WindowEvent e) {
		wp.stopGame();
	}

	public void windowOpened(WindowEvent e) {
	}

	//end of ----------- window listener methods---------------------------

	public static void main(String args[]) {
		int fps = DEFAULT_FPS;
		if (args.length != 0)
			fps = Integer.parseInt(args[0]);

		long peroid = (long) 1000.0/fps;
		System.out.println("fps:" + fps + "; period:" + peroid + " ms");

		new WormChase(peroid * 1000000L);
	}

}
