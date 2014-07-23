package labyrinth_log;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.Polygon;

import javax.swing.JFrame;
import javax.swing.JPanel;


public class CanvasGraph extends JPanel {
    private static final long serialVersionUID = 1L;
    int subjectx=0;
    int subjecty=0;
    int subjectz =0;
    int canvasType = 1; //0: T-Maze ; 1:Hexag.
    Point winningPoint = new Point (-50,-50);
    
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
    if (canvasType == 0){
        //TMAZE
        g.setColor(Color.black);
        //g.drawOval(0, 0, width, height);
        g.fillRect(width / 4 , height - ( height / 4 - height / 100 )  , width, height);
        g.fillRect(width / 4 ,  0 , width, height / 4 - height / 15);
        g.setColor(Color.BLUE);
        g.fillOval(xx * width / 71 - 5, height - (yy * height / 16) - 5, 10, 10);
    }
    else if (canvasType == 1){
        //hexag.
        g.setColor(Color.GREEN);
        g.fillOval(winningPoint.x * width / 44 - 45 - 1, height - ( (winningPoint.y-3) * height / 44) - 5 - 1, 12, 12);
        g.setColor(Color.BLUE);
        g.fillOval(xx * width / 44 - 45, height - (yy * height / 44) - 5, 10, 10);
        int xPoly[] = {15 * width / 44 - 15   , 31 * width / 44 - 15  , 41 * width / 44 - 15    , 31 * width / 44 - 15  , 15 * width / 44 - 15,  5 * width / 44 - 15   };
        int yPoly[] = {4 * height / 44 - 5    , 4 * height / 44 - 5   , 22 * height / 44 - 5   , 40 * height / 44 - 5, 40 * height / 44 - 5   , 22 * height / 44 - 5  };

        Polygon poly = new Polygon(xPoly, yPoly, xPoly.length);
        g.drawPolygon(poly);
        
        //square.
        g.setColor(Color.CYAN);
        g.fillRect(37 * width / 44, 32 * height / 44, width/30,  width/30);
        
        //triangle.
        g.setColor(Color.CYAN);
        int triangPolygonX [] = {5 * width / 44, 7 * width / 44 , 6 * width / 44  };
        int triangPolygonY [] = {34 * height / 44, 34 * height / 44 , 31 * height / 44  };
        Polygon polyTriang = new Polygon(triangPolygonX, triangPolygonY, triangPolygonX.length);
        g.fillPolygon(polyTriang);
        
        //circle.
        g.setColor(Color.CYAN);
        g.fillOval(24 * width / 50, 1 * height / 50, width/30, width/30);
    }

  }
  public static void main(String args[]) {
    JFrame frame = new JFrame("Oval Sample");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.add(new CanvasGraph());
    frame.setSize(300, 200);
    frame.setVisible(true);
  }
  
  public void setCanvasType(int nwtype){
      canvasType = nwtype;
      if (canvasType == 0){
          System.out.println("Canvas type changed to T-MAZE");
      }
      else if (canvasType == 1){
          System.out.println("Canvas type changed to Hexag");
      }
  }
  
  public void updateData(int x, int y, int z){
      subjectx = x;
      subjecty = y;
      subjectz = z;
      this.repaint();
  }
  
}