package labyrinth_log;


import java.awt.*;
import javax.swing.*;
import static java.awt.GraphicsDevice.WindowTranslucency.*;

public class fadePopUp extends JDialog {
    private static final long serialVersionUID = 1L;
    static fadeOutThread fadeout;
    static String message ;
    
    public fadePopUp( String textMessage) {
        //super("TranslucentWindow");
        System.out.println("popup created.");
        setLayout(new GridBagLayout());

        setSize(300,200);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);

        //Add a sample button.
        message = textMessage;
        add (new JLabel(message));
        pack();
        setAlwaysOnTop(true);
        //add(new JButton("Test button"));
    }
    
    public void disposeAll(){
        this.dispose();
        fadeout = null;
        System.gc();
    }

    public static void main(String[] args) {
        // Determine if the GraphicsDevice supports translucency.
        GraphicsEnvironment ge = 
            GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice gd = ge.getDefaultScreenDevice();

        //If translucent windows aren't supported, exit.
        if (!gd.isWindowTranslucencySupported(TRANSLUCENT)) {
            System.err.println(
                "Translucency is not supported");
                System.exit(0);
        }
        
        JDialog.setDefaultLookAndFeelDecorated(true);

        // Create the GUI on the event-dispatching thread
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                fadePopUp tw = new fadePopUp(message);
                //tw.setMessage(message);
                // Set the window to 55% opaque (45% translucent).
                tw.setOpacity(1.0f);
                tw.setResizable(false);
                fadeout = new fadeOutThread();
                fadeout.setRunningJDialog(tw);
                fadeout.start();

                // Display the window.
                tw.setVisible(true);
            }
        });
    }
}


class fadeOutThread extends Thread {
    fadePopUp runningJDialog;
    int counter = 0;
    boolean running = true;
    
    public void setRunningJDialog(fadePopUp pop){
        runningJDialog = pop;
    }
    
    public void run(){
        while(running){
            System.out.println("MyThread running");
            counter++;
            if (counter >= 45){
                running = false;
                System.out.println("MyThread FALSE");
                //this.interrupt();
                runningJDialog.disposeAll();
            }
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                //e.printStackTrace();
            }
            
            if (counter >= 35){
                float fl =(float) (runningJDialog.getOpacity() - 0.1);
                if (fl < 0.01) fl = 0;
                runningJDialog.setOpacity(fl);
            }
            }

        }
       
}