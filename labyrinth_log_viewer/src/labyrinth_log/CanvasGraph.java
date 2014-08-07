package labyrinth_log;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Polygon;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;


public class CanvasGraph extends JPanel {
    private static final long serialVersionUID = 1L;
    int subjectx=0;
    int subjecty=0;
    int subjectz =0;
    boolean showArrow = true;
    
    double dirx;
    double diry;
    int canvasType = 2; //0: T-Maze ; 1:Hexag. ; 2:no-type
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
        //TMAZE type
        
        g.setColor(Color.black);
        //g.drawOval(0, 0, width, height);
        g.fillRect(width / 4 , height - ( height / 4 - height / 100 )  , width, height);
        g.fillRect(width / 4 ,  0 , width, height / 4 - height / 15);
        g.setColor(Color.BLUE);
        g.fillOval(xx * width / 71 - 5, height - (yy * height / 16) - 5, 10, 10);
        
        
        int xxpos = xx * width / 71 - 5;
        int yypos = height - (yy * height / 16) - 5;
        
        
        if (showArrow){
            g.setColor(Color.DARK_GRAY);
            //arrow
            g.drawLine(xxpos + 5, yypos + 5, xxpos + 5 + (int)(dirx*20) , yypos + 5 -(int)(diry*20) );
            drawArrow(g, xxpos + 5, yypos + 5, xxpos + 5 + (int)(dirx*20) , yypos + 5 -(int)(diry*20) );
        }

    }
    else if (canvasType == 1){
        //hexag. type.
        
        g.setColor(Color.GREEN);
        int xxpos = xx * width / 44 - 45;
        int yypos = height - (yy * height / 44) - 5;
        
        g.fillOval(winningPoint.x * width / 44 - 45 - 1, height - ( (winningPoint.y-3) * height / 44) - 5 - 1, 12, 12);
        g.setColor(Color.BLUE);
        g.fillOval(xxpos, yypos, 10, 10);
        int xPoly[] = {15 * width / 44 - 15   , 31 * width / 44 - 15  , 41 * width / 44 - 15    , 31 * width / 44 - 15  , 15 * width / 44 - 15,  5 * width / 44 - 15   };
        int yPoly[] = {4 * height / 44 - 5    , 4 * height / 44 - 5   , 22 * height / 44 - 5   , 40 * height / 44 - 5, 40 * height / 44 - 5   , 22 * height / 44 - 5  };
        
        if (showArrow){
            g.setColor(Color.DARK_GRAY);
            //arrow
            g.drawLine(xxpos + 5, yypos + 5, xxpos + 5 + (int)(dirx*20) , yypos + 5 -(int)(diry*20) );
            drawArrow(g, xxpos + 5, yypos + 5, xxpos + 5 + (int)(dirx*20) , yypos + 5 -(int)(diry*20) );
        }

        
        g.setColor(Color.BLACK);
        Polygon poly = new Polygon(xPoly, yPoly, xPoly.length);
        g.drawPolygon(poly);
        
        //square key.
        g.setColor(Color.CYAN);
        g.fillRect(37 * width / 44, 32 * height / 44, width/30,  width/30);
        
        //triangle key.
        g.setColor(Color.CYAN);
        int triangPolygonX [] = {5 * width / 44, 7 * width / 44 , 6 * width / 44  };
        int triangPolygonY [] = {34 * height / 44, 34 * height / 44 , 31 * height / 44  };
        Polygon polyTriang = new Polygon(triangPolygonX, triangPolygonY, triangPolygonX.length);
        g.fillPolygon(polyTriang);
        
        //circle key.
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
  
  void savePanel(String filen) {
      if (filen == null)
          return;
      int w = this.getWidth();
      int h = this.getHeight();
      BufferedImage bi = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
      Graphics2D g2 = bi.createGraphics();
      this.paint(g2);
      g2.dispose();
      String tipo = "png";
      try {
          ImageIO.write(bi, tipo, new File(filen + "." + tipo));
          System.out.println("Image: " + filen + "." + tipo + " saved");
      } catch (IOException ioe) {
          System.out.println("Saving file error: " + ioe.getMessage());
      }
      this.updateUI();
  }
  
  void drawArrow(Graphics g1, int x1, int y1, int x2, int y2) {
      Graphics2D g = (Graphics2D) g1.create();
      int ARR_SIZE = 8;
      
      double dx = x2 - x1, dy = y2 - y1;
      double angle = Math.atan2(dy, dx);
      int len = (int) Math.sqrt(dx*dx + dy*dy);
      AffineTransform at = AffineTransform.getTranslateInstance(x1, y1);
      at.concatenate(AffineTransform.getRotateInstance(angle));
      g.transform(at);

      // Draw horizontal arrow starting in (0, 0)
      g.drawLine(0, 0, len, 0);
      g.fillPolygon(new int[] {len, len-ARR_SIZE, len-ARR_SIZE, len},
                    new int[] {0, -ARR_SIZE, ARR_SIZE, 0}, 4);
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
  
  public void updateData(){
      this.repaint();
  }
  
  public void updateData(int x, int y, int z, double drx, double dry){
      subjectx = x;
      subjecty = y;
      subjectz = z;
      dirx = drx;
      diry = dry;
      this.repaint();
  }
  
}