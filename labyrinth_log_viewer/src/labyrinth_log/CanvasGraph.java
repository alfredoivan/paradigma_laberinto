package labyrinth_log;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JFrame;
import javax.swing.JPanel;


public class CanvasGraph extends JPanel {
	int subjectx=0;
	int subjecty=0;
	int subjectz =0;
	
  public CanvasGraph() {
	  this.setPreferredSize(new Dimension(200,200));
  }
  public void paintComponent(Graphics g) {
	//Note: we flip the trajectory vertically. Down = left. UP = right
    int width = getWidth();
    int height = getHeight();
    int xx = subjectx;
    int yy = subjecty - 3;
    g.setColor(Color.LIGHT_GRAY);
    g.fillRect(0, 0, width, height);
    g.setColor(Color.black);
    //g.drawOval(0, 0, width, height);
    g.fillRect(width / 4 , height - ( height / 4 - height / 100 )  , width, height);
    g.fillRect(width / 4 ,  0 , width, height / 4 - height / 15);
    g.setColor(Color.BLUE);
    g.fillOval(xx * width / 71 - 5, height - (yy * height / 16) - 5, 10, 10);

  }
  public static void main(String args[]) {
    JFrame frame = new JFrame("Oval Sample");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.add(new CanvasGraph());
    frame.setSize(300, 200);
    frame.setVisible(true);
  }
  
  
  public void updateData(int x, int y, int z){
	  subjectx = x;
	  subjecty = y;
	  subjectz = z;
	  this.repaint();
  }
  
}