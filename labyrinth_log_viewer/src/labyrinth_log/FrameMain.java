package labyrinth_log;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import java.awt.*;
import java.awt.event.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class FrameMain extends JFrame implements ChangeListener {
    /**
     * 
     */
    private static final long serialVersionUID = 1L;
    final int SLIDER_DIVISION = 1000;
    
    static int mouseCounter = 0; //counter for double-click
    private Closer Handler;
    CanvasGraph canvas = new CanvasGraph();
    JSlider timeSlider;
    JList<String> jListTrials;
    JPanel pnlAll = new JPanel(); //panel that contains the rest of the GUI items.

    DefaultListModel<String> listModel = new DefaultListModel<String>();
    JLabel lblInfo;
    JLabel lblSouthInfo;
    JLabel lblInfoBlank;
    JLabel lblInfo_Start;
    JLabel lblInfo_End;
    JLabel lblInfo_Duration;
    JLabel lblInfo_Status;
    JLabel lblInstantInfo;

    JMenu menuRecentFiles;
    ArrayList<String> paths = new ArrayList<String>();

    ArrayList<Trial> trialArray = new ArrayList<Trial>();
    int currentTrialIndex = 0;
    int currentTrialStart = 0;
    int currentTrialEnd = 0;
    int currentTrialStatus = 0; // 0 unknown, 1 lose, 2 win

    boolean fileOpened = false; // true = at least one file has been opened
    boolean winingLocationFound = false; //appropriate with octagon.

    String currentFilePath; //current working path.

    FrameMain() {
        Handler = new Closer();
        setTitle("Labyrinth log viewer");
        setSize(640, 480);
        addWindowListener(Handler);
        addComponents();
        counterThread cnt = new counterThread();
        cnt.start();
        setVisible(true);
        prepareDragAndDrop();
    }

    public void prepareDragAndDrop() {
        new FileDrop(pnlAll, new FileDrop.Listener() {
            public void filesDropped(java.io.File[] files) {
                // handle file drop
                for (int i = 0; i < files.length; i++) {
                    try {
                        System.out.println(files[i].getCanonicalPath() + "\n");
                        openFile(files[i].getCanonicalPath());
                        // model.addElement(files[i].getCanonicalPath());
                    } // end try
                    catch (java.io.IOException e) {
                    }
                } // end for: through each dropped file
            } // end filesDropped
        }); // end FileDrop.Listener
    }

    public void addComponents() {
        JButton btnLoad = new JButton("Load Log File");
        final JFileChooser fc = new JFileChooser();
        btnLoad.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                //
                int returnVal = fc.showOpenDialog(null);

                if (returnVal == JFileChooser.APPROVE_OPTION) {
                    File file = fc.getSelectedFile();
                    // This is where a real application would open the file.
                    System.out.println("Opening: " + file.getAbsolutePath());
                    print("Opening: " + file.getAbsolutePath());
                    try {
                        openFile(file.getAbsolutePath());
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else {
                    System.out.println("Open command cancelled by user.");
                    print("Open command cancelled by user.");
                }
            }
        });

        // JButton btnUpdate = new JButton("Update");
        // btnUpdate.addActionListener(new ActionListener() {
        //
        // @Override
        // public void actionPerformed(ActionEvent arg0) {
        // System.out.println("Updating...");
        // updateFrame();
        // }} );

        pnlAll.setLayout(new BorderLayout());

        JPanel pnlCanvas = new JPanel();
        pnlCanvas.setLayout(new BorderLayout());

        JPanel pnlButton = new JPanel();
        pnlButton.setLayout(new GridLayout(0, 1));

        JMenuBar menuBar;
        JMenu menu;
        menuRecentFiles = new JMenu("Recent Files");
        JMenuItem menuItem;

        menuBar = new JMenuBar();
        menu = new JMenu("Labyrinth Log");
        menu.setMnemonic(KeyEvent.VK_A);
        menu.getAccessibleContext().setAccessibleDescription(
                "Main Labyrinth log menu.");
        menuBar.add(menu);

        menu.add(menuRecentFiles);

        menuItem = new JMenuItem("Binary (stats)", KeyEvent.VK_B);
        menuItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                launchWindow(0);
            }

        });
        menu.add(menuItem);
        
        menuItem = new JMenuItem("Duration (stats)", KeyEvent.VK_D);
        menuItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                launchWindow(1);
            }

        });
        menu.add(menuItem);

        final JCheckBoxMenuItem checkmenu = new JCheckBoxMenuItem(
                "Show subject's direction (arrow)?");
        checkmenu.setState(true);
        checkmenu.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                if (checkmenu.getState() == true) {
                    canvas.showArrow = true;
                } else {
                    canvas.showArrow = false;
                }
                canvas.updateData();
            }

        });
        menu.add(checkmenu);
        
        final JCheckBoxMenuItem checkmenu2 = new JCheckBoxMenuItem(
                "Show subject's vision field ?");
        checkmenu2.setState(false);
        checkmenu2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                if (checkmenu2.getState() == true) {
                    canvas.showVField = true;
                } else {
                    canvas.showVField = false;
                }
                canvas.updateData();
            }

        });
        menu.add(checkmenu2);

        menuItem = new JMenuItem("Exit", KeyEvent.VK_T);
        menuItem.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                // TODO Auto-generated method stub
                System.out.println("Exit from menu.");
                exitAll();

            }

        });
        menu.add(menuItem);

        this.setJMenuBar(menuBar);

        // JLabel lblTitle = new JLabel("Labyrinth Log");
        lblInstantInfo = new JLabel("----------");
        lblInstantInfo.setHorizontalAlignment(SwingConstants.CENTER);
        JPanel southLabels = new JPanel(new BorderLayout());
        JLabel lblBlankSpace = new JLabel("     ");
        // southLabels.add(lblInstantInfo, BorderLayout.CENTER);
        southLabels.add(lblBlankSpace, BorderLayout.PAGE_END);

        lblSouthInfo = new JLabel("No file loaded.");
        lblSouthInfo.setFont(lblSouthInfo.getFont().deriveFont(10.0f));

        // southLabels.add(lblSouthInfo, BorderLayout.LINE_START);

        // pnlAll.add(lblTitle, BorderLayout.NORTH);

        JPanel pnlII = new JPanel(new BorderLayout());
        pnlII.add(southLabels, BorderLayout.CENTER);
        pnlII.add(lblSouthInfo, BorderLayout.PAGE_END);
        pnlAll.add(pnlII, BorderLayout.SOUTH);

        JPanel pnlInterButton = new JPanel();
        pnlInterButton.setLayout(new BorderLayout());

        pnlInterButton.add(btnLoad, BorderLayout.NORTH);
        pnlCanvas.add(canvas, BorderLayout.CENTER);

        timeSlider = new JSlider(JSlider.HORIZONTAL, 0, SLIDER_DIVISION, 0);
        timeSlider.addChangeListener(this);

        JPanel timeSliderPluslblInfo = new JPanel(new BorderLayout());
        timeSliderPluslblInfo.add(lblInstantInfo, BorderLayout.PAGE_END);
        timeSliderPluslblInfo.add(timeSlider, BorderLayout.PAGE_START);

        // listModel.addElement("Trial 0");
        // listModel.addElement("Trial 1");
        // listModel.addElement("Trial 2");
        listModel.addElement("-----------------");
        jListTrials = new JList<String>(listModel);
        jListTrials.setVisibleRowCount(5);
        jListTrials.addMouseListener(new MouseListener() {

            @Override
            public void mouseClicked(MouseEvent arg0) {
                mouseCounter += 5;
                if (mouseCounter > 5) {
                    // System.out.println("Mouse doubleclicked..");
                    mouseCounter = 0;
                    updateFrame();
                }

            }

            @Override
            public void mouseEntered(MouseEvent arg0) {
            }

            @Override
            public void mouseExited(MouseEvent arg0) {
            }

            @Override
            public void mousePressed(MouseEvent arg0) {
            }

            @Override
            public void mouseReleased(MouseEvent arg0) {
            }

        });

        // jListTrials.setPreferredSize(new Dimension(10,20) );
        JScrollPane scrollPane = new JScrollPane();
        scrollPane.setViewportView(jListTrials);
        pnlInterButton.add(scrollPane, BorderLayout.CENTER);
        // pnlInterButton.add(btnUpdate, BorderLayout.SOUTH);

        JPanel pnlSuperInfo = new JPanel();
        pnlSuperInfo.setLayout(new BorderLayout());

        JPanel pnlInfo = new JPanel();
        pnlInfo.setLayout(new GridLayout(0, 1, 5, 2));

        lblInfoBlank = new JLabel("                                       ");
        lblInfo = new JLabel("Trial info:");
        lblInfo_Start = new JLabel("Start:");
        lblInfo_End = new JLabel("End:");
        lblInfo_Status = new JLabel("Status:");
        lblInfo_Duration = new JLabel("Duration:");

        pnlButton.add(pnlInterButton);

        pnlInfo.add(lblInfoBlank);
        pnlInfo.add(lblInfo);
        pnlInfo.add(lblInfo_Start);
        pnlInfo.add(lblInfo_End);
        pnlInfo.add(lblInfo_Duration);
        pnlInfo.add(lblInfo_Status);

        // not working properly.
        pnlInfo.setMinimumSize(new Dimension(lblInfo_Duration.getText()
                .length() * 10, lblInfo_Duration.getText().length() * 10));

        pnlSuperInfo.add(pnlInfo, BorderLayout.SOUTH);
        pnlButton.add(pnlSuperInfo);

        pnlCanvas.add(timeSliderPluslblInfo, BorderLayout.SOUTH);

        pnlAll.add(pnlCanvas, BorderLayout.CENTER);
        pnlAll.add(pnlButton, BorderLayout.LINE_START);
        this.add(pnlAll);
    }

    public void openFile(String path) throws FileNotFoundException, IOException {
        System.out.println("openFile: " + path);
        fileOpened = true;
        winingLocationFound = false;
        trialArray.removeAll(trialArray);
        //System.out.println("trialArray cleaned.");
        try {
            BufferedReader br = new BufferedReader(new FileReader("" + path));
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            Trial temp = new Trial();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
                if (line == null)
                    continue;
                line = line.replaceAll(";", ","); // just in case it is with ;
                if (line.contains(",1,1") || line.contains(",1,2")) {
                    if (line.contains(",1,1")) {
                        temp.setStatus(1);
                    } else {
                        temp.setStatus(2);
                        // we inform position of win. Useful if hexag to
                        // determine winning status in each trial and to put
                        // winning loc.

                        canvas.winningPoint.setLocation(temp.getPoint(-1)
                                .iGetX(), temp.getPoint(-1).iGetY());
                        // System.out.println(".........----");
                        // System.out.println(temp.getPoint(-1).iGetX());
                        // System.out.println(temp.getPoint(-1).iGetY());
                        // System.out.println(".........----");
                        winingLocationFound = true;

                    }
                    // currentTrialStart = temp.getStart();
                    // currentTrialEnd = temp.getEnd();
                    // currentTrialStatus = temp.getStatus();

                    trialArray.add(temp);
                    temp = new Trial();
                    continue;
                }
                temp.addPoint(line);

            }
            trialArray.add(temp);
            // String everything = sb.toString();
            // System.out.println("Trial 0 contains:");
            // trialArray.get(0).printAllPoints();
            // System.out.println("-------");
            // System.out.println("Trial 1 contains:");
            // trialArray.get(1).printAllPoints();
            // listModel.removeAllElements();
            listModel.clear();
            for (int i = 0; i < trialArray.size(); i++) {
                listModel.addElement("Trial " + i);
            }
            if ((int) trialArray.get(0).getPoint(0).getX() == 25
                    && (int) trialArray.get(0).getPoint(0).getY() == 25) {
                // this is a hexag training type.
                //System.out.println("this is hexag type.");
                canvas.setCanvasType(1);
                if (winingLocationFound == true)
                    infoBox("Winning location drawn into a green circle on each trial.");
                else {
                    infoBox("Warning: no winning location found. Probably subject never won.");
                }
            } else if ((int) trialArray.get(0).getPoint(0).getX() == 70
                    && (int) trialArray.get(0).getPoint(0).getY() == 11) {
                //System.out.println("this is tmaze type.");
                canvas.setCanvasType(0);
            } else {
                //System.out.println("Unknown type.");
            }

            canvas.repaint();

            lblSouthInfo.setText("File opened: " + path);
            addRecentFile(path);
            jListTrials.setSelectedIndex(0);
            updateFrame();
            currentFilePath = path;
            br.close();
            // jListTrials = new JList(listModel);
        }
        catch(Exception e){
            System.out.println("Exception while opening file.");
            return;
        }
    }

    public static void main(String args[]) {
        @SuppressWarnings("unused")
        JFrame f = new FrameMain();
    }

    public void updateFrame() {
        if (!fileOpened)
            return;
        // update function: First checks if variables are correct, then calls
        // other fs.
        currentTrialIndex = jListTrials.getSelectedIndex();
        if (currentTrialIndex < 0)
            return;

        timeSlider.setValue(0);
        _updateFr();
        setSliderPointTime(0);
    }

    private void _updateFr() {
        // private function that only updates labels with updated info.
        currentTrialStart = trialArray.get(currentTrialIndex).getStart();
        currentTrialEnd = trialArray.get(currentTrialIndex).getEnd();
        currentTrialStatus = trialArray.get(currentTrialIndex).getStatus();

        lblInfo.setText("Trial info: " + currentTrialIndex);
        lblInfo_Start.setText("Start: " + currentTrialStart + " ms");
        lblInfo_End.setText("End: " + currentTrialEnd + " ms");
        if (currentTrialStatus == 1) {
            lblInfo_Status.setText("Status: " + currentTrialStatus
                    + " - Fail           ");
        } else if (currentTrialStatus == 2) {
            lblInfo_Status.setText("Status: " + currentTrialStatus
                    + " - Success ");
        } else {
            lblInfo_Status.setText("Status: " + currentTrialStatus);
        }
        // lblInfo_Status.setText("Status: " + currentTrialStatus );
        lblInfo_Duration.setText("Duration: "
                + (currentTrialEnd - currentTrialStart) + " ms");
    }

    public void print(String text) {
        lblInstantInfo.setText(text);
    }

    @Override
    public void stateChanged(ChangeEvent arg0) {
        if (!fileOpened)
            return;
        //System.out.println(jListTrials.getSelectedIndex());
        currentTrialIndex = jListTrials.getSelectedIndex();
        if (currentTrialIndex < 0)
            return;
        // currentTrialIndex = jListTrials.getSelectedIndex();
        _updateFr();

        int a = timeSlider.getValue();
        //System.out.println("Slider status changed: " + a);
        trialArray.get(trialArray.size() / SLIDER_DIVISION * a);

        int tmpin = (int) ((int) trialArray.get(currentTrialIndex).points
                .size() / (SLIDER_DIVISION * 1.0) * a) - 1;
        if (tmpin < 0)
            tmpin = 0;
        setSliderPointTime(tmpin);
    }

    public void setSliderPointTime(int tmpin) {
        //System.out.println(trialArray.get(currentTrialIndex).getPoint(tmpin)
        //        .toString());
        print(trialArray.get(currentTrialIndex).getPoint(tmpin).toString());
        canvas.updateData(
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin).getX(),
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin).getY(),
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin)
                        .getTime(),
                trialArray.get(currentTrialIndex).getPoint(tmpin).getDirX(),
                trialArray.get(currentTrialIndex).getPoint(tmpin).getDirY());
    }

    @SuppressWarnings("static-access")
    public void infoBox(String infoMessage) {
        fadePopUp pop = new fadePopUp(infoMessage);
        pop.main(null);
    }

    public void addRecentFile(String path) {
        // adds file to menu list of recent files. If file already exists in the
        // list, put it on top..

        for (int i = 0; i < paths.size(); i++) {
            if (paths.get(i).equals(path)) {
                paths.remove(i);
            }
        }

        paths.add(path);
        menuRecentFiles.removeAll();

        for (int i = 0; i < paths.size(); i++) {
            final JMenuItem menuItem = new JMenuItem(paths.get(i),
                    KeyEvent.VK_T);
            menuItem.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent arg0) {
                    // TODO Auto-generated method stub
                    try {
                        openFile(menuItem.getText());
                    } catch (Exception e) {
                    }

                }

            });
            menuRecentFiles.add(menuItem);
        }
    }

    public void launchWindow( int type) {
        if (!fileOpened)
            return;
        
        String fileSuffix = "";
        final JFrame frBinary = new JFrame();
        final CanvasStats canvasStats = new CanvasStats();
        canvasStats.setPrefSize();
        if (type == 0 ){
            //binary.
            fileSuffix = "_binary";
            frBinary.setTitle("Binary (stats.)");
            canvasStats.setData(processBinaryData());
            
        }
        if (type == 1){
            //trial duration vs trial.
            fileSuffix = "_duration";
            frBinary.setTitle("Trial Duration in seconds (stats.)");
            canvasStats.setData(processDurationData());
        }
        
        JMenu binary_menu = new JMenu("Options");

        JMenuItem menuItem_save = new JMenuItem("Save Image", KeyEvent.VK_S);

        JMenuItem menuItem_exit = new JMenuItem("Exit", KeyEvent.VK_E);

        final String fileSuff_ = fileSuffix; 
        menuItem_save.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {
                canvasStats.savePanel(currentFilePath + fileSuff_);
                infoBox("Image Saved: " + currentFilePath + fileSuff_ + "." +canvasStats.imageExtension );
            }

        });

        menuItem_exit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent arg0) {

                frBinary.dispatchEvent(new WindowEvent(frBinary,
                        WindowEvent.WINDOW_CLOSING));
            }

        });

        binary_menu.add(menuItem_save);
        binary_menu.add(menuItem_exit);

        JMenuBar menuBar_binary = new JMenuBar();
        menuBar_binary.add(binary_menu);

        frBinary.setJMenuBar(menuBar_binary);

        frBinary.setVisible(true);

        

        System.out.println("trialarray size : " + trialArray.size());

        final JScrollPane scrollCanvas = new JScrollPane(canvasStats,
                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
                JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);

        frBinary.add(scrollCanvas);
        
        
        frBinary.pack();
    }
    
    private int[] processDurationData(){
        //returns array of int as the dataset to be draw in a canvas.
        //rounds data to seconds, 2 decimals
        
        int[] dataset = new int[trialArray.size()];
        
        for (int i = 0; i < trialArray.size(); i++) {
            dataset[i] = (int) ( ( trialArray.get(i).getDuration() )/ 1000.0 );
        }
        
        return dataset;
    }
    
    private int[] processBinaryData() {
        int[] dataset = new int[trialArray.size()];

        for (int i = 0; i < trialArray.size(); i++) {
            if (trialArray.get(i).getStatus() == 2) {
                dataset[i] = 1;
            } else {
                dataset[i] = 0;
            }

        }

        return dataset;
    }

    public void exitAll() {
        System.exit(0);
    }
}

class counterThread extends Thread {
    boolean runningc = true;

    public void run() {
        while (runningc) {
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                // e.printStackTrace();
            }
            // System.out.println(FrameMain.mouseCounter);
            if (FrameMain.mouseCounter > 0) {
                FrameMain.mouseCounter--;
            }
        }

    }

}

class Closer extends WindowAdapter {
    public void windowClosing(WindowEvent event) {
        System.exit(0);
    }
}