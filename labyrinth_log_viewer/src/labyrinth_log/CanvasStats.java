package labyrinth_log;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.JPanel;

class CanvasStats extends JPanel {
    int arrayData[] = new int[0];
    int maxValue = 0;
    boolean isMaxTrialsToTen = false;

    private static final long serialVersionUID = 1L;

    public CanvasStats() {
        setBorder(BorderFactory.createLineBorder(Color.black));
        // System.out.println("Canvas graph created.");
    }

    public Dimension getPreferredSize() {
        return new Dimension(10 + arrayData.length * 62 + 50, 350);
    }

    public void setPrefSize() {
        this.setPreferredSize(new Dimension(10 + arrayData.length * 62 + 50,
                350));
        // System.out.println(arrayData.length);
        this.updateUI();
    }
    
    
    
    public int getMaxValue() {
        return maxValue;
    }

    public void setMaxValue(int maxValue) {
        this.maxValue = maxValue;
    }

    
    public void setGoodSize(){
        this.setSize(new Dimension(this.getSize().width,
                382));
    }
    
    public void paintComponent(Graphics g) {
        // Draws to the canvas
        super.paintComponent(g);
        // Draw Text
        // g.drawString("Custom Panel: Here goes the graph needed to visualize",10,20);
        if (arrayData != null) {
            for (int i = 0; i < arrayData.length; i++) {
                int unitHeightValue = 0;
                if (maxValue != 0)
                    unitHeightValue = g.getClipBounds().height / maxValue;
                
                g.fillRect(10 + i * 62, g.getClipBounds().height - (arrayData[i] + 1)
                        * unitHeightValue - 5, 40, (arrayData[i] + 1)
                        * unitHeightValue - 35);
                g.drawString("[" + i + "] _ " + arrayData[i], 10 + i * 62,
                        super.getHeight() - 20);
            }

        }

    }

    public void setData(int[] data) {
        arrayData = data;
        
        if (!isMaxTrialsToTen){
            for (int i = 0; i < arrayData.length; i++) {
                if (arrayData[i] > maxValue)
                    maxValue = arrayData[i];
            }
        }else{
            maxValue = 11;
        }

        // System.out.println(maxValue);
        this.setPrefSize();
    }

    void savePanel(String filen) {
        if (filen == null)
            return;
        setGoodSize();
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
    }

    
    void recalculateMaxData(){
        for (int i = 0; i < arrayData.length; i++) {
            if (arrayData[i] > maxValue)
                maxValue = arrayData[i];
        }
    }
    
}
