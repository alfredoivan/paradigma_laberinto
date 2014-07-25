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
    
    static int mouseCounter = 0;
    private Closer Handler;
    CanvasGraph canvas = new CanvasGraph();
    JSlider timeSlider;
    JList<String> jListTrials;
    

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
    int currentTrialStatus = 0; //0 unknown, 1 lose, 2 win

    boolean fileOpened = false; //true = at least one file has been opened
    boolean winingLocationFound = false;

    final int SLIDER_DIVISION = 1000;

    FrameMain() {
        Handler = new Closer();
        setTitle("Labyrinth log viewer");
        setSize(640, 480);
        addWindowListener(Handler);
        addComponents();
        counterThread cnt = new counterThread();
        cnt.start();
        setVisible(true);
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
                    print ("Open command cancelled by user.");
                }
            }
        });

        //        JButton btnUpdate = new JButton("Update");
        //        btnUpdate.addActionListener(new ActionListener() {
        //
        //            @Override
        //            public void actionPerformed(ActionEvent arg0) {
        //                System.out.println("Updating...");
        //                updateFrame();
        //            }} );

        JPanel pnlAll = new JPanel();
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
        
        
        menuItem = new JMenuItem("Binary (stats)",
                KeyEvent.VK_B);
        menuItem.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent arg0) {
                launchBinaryWindow();
            }
            
        });
        menu.add(menuItem);
        
        final JCheckBoxMenuItem checkmenu = new JCheckBoxMenuItem("Show subject's direction (arrow)?");
        checkmenu.setState(true);
        checkmenu.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent arg0) {
                if (checkmenu.getState() == true){
                    canvas.showArrow = true;
                }else{
                    canvas.showArrow = false;
                }
                canvas.updateData();
            }
            
        });
        menu.add(checkmenu);
        
        menuItem = new JMenuItem("Exit",
                KeyEvent.VK_T);
        menuItem.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent arg0) {
                // TODO Auto-generated method stub
                System.out.println("Exit from menu.");
                exitAll();
                
            }
            
        });
        menu.add(menuItem);
        

        
        this.setJMenuBar(menuBar);
        
        
        //JLabel lblTitle = new JLabel("Labyrinth Log");
        lblInstantInfo = new JLabel("----------");
        lblInstantInfo.setHorizontalAlignment(SwingConstants.CENTER);
        JPanel southLabels = new JPanel(new BorderLayout());
        JLabel lblBlankSpace = new JLabel("     ");
        //southLabels.add(lblInstantInfo, BorderLayout.CENTER);
        southLabels.add(lblBlankSpace, BorderLayout.PAGE_END);
        
        lblSouthInfo = new JLabel("No file loaded.");
        lblSouthInfo.setFont(lblSouthInfo.getFont().deriveFont(10.0f));
        
        //southLabels.add(lblSouthInfo, BorderLayout.LINE_START);
        
        //pnlAll.add(lblTitle, BorderLayout.NORTH);

        JPanel pnlII = new JPanel(new BorderLayout() );
        pnlII.add(southLabels, BorderLayout.CENTER);
        pnlII.add(lblSouthInfo, BorderLayout.PAGE_END);
        pnlAll.add(pnlII, BorderLayout.SOUTH);

        JPanel pnlInterButton = new JPanel();
        pnlInterButton.setLayout(new BorderLayout());

        pnlInterButton.add(btnLoad, BorderLayout.NORTH);
        pnlCanvas.add(canvas, BorderLayout.CENTER);

        timeSlider = new JSlider(JSlider.HORIZONTAL, 0, SLIDER_DIVISION, 0);
        timeSlider.addChangeListener(this);
        
        JPanel timeSliderPluslblInfo = new JPanel( new BorderLayout() );
        timeSliderPluslblInfo.add(lblInstantInfo, BorderLayout.PAGE_END);
        timeSliderPluslblInfo.add(timeSlider, BorderLayout.PAGE_START);
        
        
        // listModel.addElement("Trial 0");
        // listModel.addElement("Trial 1");
        // listModel.addElement("Trial 2");
        listModel.addElement("-----------------");
        jListTrials = new JList<String>(listModel);
        jListTrials.setVisibleRowCount(5);
        jListTrials.addMouseListener(new MouseListener(){

            @Override
            public void mouseClicked(MouseEvent arg0) {
                mouseCounter += 5;
                if (mouseCounter > 5){
                    //System.out.println("Mouse doubleclicked..");
                    mouseCounter = 0;
                    updateFrame();
                }
                
            }

            @Override
            public void mouseEntered(MouseEvent arg0) { }

            @Override
            public void mouseExited(MouseEvent arg0) { }

            @Override
            public void mousePressed(MouseEvent arg0) { }

            @Override
            public void mouseReleased(MouseEvent arg0) { }
            
        });

        // jListTrials.setPreferredSize(new Dimension(10,20) );
        JScrollPane scrollPane = new JScrollPane();
        scrollPane.setViewportView(jListTrials);
        pnlInterButton.add(scrollPane, BorderLayout.CENTER);
        //pnlInterButton.add(btnUpdate, BorderLayout.SOUTH);

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

        //not working properly.
        pnlInfo.setMinimumSize( new Dimension (lblInfo_Duration.getText().length() *10 , lblInfo_Duration.getText().length() *10 ) );

        pnlSuperInfo.add(pnlInfo, BorderLayout.SOUTH);
        pnlButton.add(pnlSuperInfo);

        pnlCanvas.add(timeSliderPluslblInfo, BorderLayout.SOUTH);

        pnlAll.add(pnlCanvas, BorderLayout.CENTER);
        pnlAll.add(pnlButton, BorderLayout.LINE_START);
        this.add(pnlAll);
    }

    public void openFile(String path) throws FileNotFoundException, IOException {
        System.out.println("openFile");
        fileOpened = true;
        winingLocationFound = false;
        trialArray.removeAll(trialArray);
        try (BufferedReader br = new BufferedReader(new FileReader("" + path))) {
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            Trial temp = new Trial();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();



                if (line == null)
                    continue;

                line = line.replaceAll(";", ","); //just in case it is with ;

                if (line.contains(",1,1") || line.contains(",1,2")) {
                    if (line.contains(",1,1")){
                        temp.setStatus(1);
                    }else{
                        temp.setStatus(2);
                        //we inform position of win. Useful if hexag to determine winning status in each trial and to put winning loc.
                        
                        canvas.winningPoint.setLocation(temp.getPoint(-1).iGetX(), temp.getPoint(-1).iGetY());
                        //System.out.println(".........----");
                        //System.out.println(temp.getPoint(-1).iGetX());
                        //System.out.println(temp.getPoint(-1).iGetY());
                        //System.out.println(".........----");
                        winingLocationFound = true;
                        
                        
                    }
                    //currentTrialStart = temp.getStart();
                    //currentTrialEnd = temp.getEnd();
                    //currentTrialStatus = temp.getStatus();

                    trialArray.add(temp);
                    temp = new Trial();
                    continue;
                }
                temp.addPoint(line);

            }
            trialArray.add(temp);
            //String everything = sb.toString();
            //System.out.println("Trial 0 contains:");
            // trialArray.get(0).printAllPoints();
            //System.out.println("-------");
            //System.out.println("Trial 1 contains:");
            // trialArray.get(1).printAllPoints();
            // listModel.removeAllElements();
            listModel.clear();
            for (int i = 0; i < trialArray.size(); i++) {
                listModel.addElement("Trial " + i);
            }
            if ( (int)trialArray.get(0).getPoint(0).getX() == 25 && (int)trialArray.get(0).getPoint(0).getY() == 25){
                //this is a hexag training type.
                System.out.println("this is hexag type.");
                canvas.setCanvasType(1);
                if (winingLocationFound == true)
                    infoBox("Winning location drawn into a green circle on each trial.");
                else{
                    infoBox("Warning: no winning location found. Probably subject never won.");
                }
            }else if ( (int)trialArray.get(0).getPoint(0).getX() == 70 && (int)trialArray.get(0).getPoint(0).getY() == 11 ) {
                System.out.println("this is tmaze type.");
                canvas.setCanvasType(0);
            }
            else{
                System.out.println("Unknown type.");
            }
            
            canvas.repaint();
            
            lblSouthInfo.setText("File opened: " +path);
            addRecentFile(path);
            jListTrials.setSelectedIndex(0);
            updateFrame();
            
            // jListTrials = new JList(listModel);
        }
    }

    public static void main(String args[]) {
        @SuppressWarnings("unused")
        JFrame f = new FrameMain();
    }

    public void updateFrame(){
        if (!fileOpened) return;
        //update function: First checks if variables are correct, then calls other fs.
        currentTrialIndex = jListTrials.getSelectedIndex();
        if (currentTrialIndex < 0)
            return;

        timeSlider.setValue(0);
        _updateFr();
        setSliderPointTime(0);
    }

    private void _updateFr(){
        //private function that only updates labels with updated info.
        currentTrialStart = trialArray.get(currentTrialIndex).getStart();
        currentTrialEnd = trialArray.get(currentTrialIndex).getEnd();
        currentTrialStatus = trialArray.get(currentTrialIndex).getStatus();


        lblInfo.setText("Trial info: " + currentTrialIndex );
        lblInfo_Start.setText("Start: " + currentTrialStart +" ms");
        lblInfo_End.setText("End: " + currentTrialEnd +" ms");
        if (currentTrialStatus == 1){
            lblInfo_Status.setText("Status: " + currentTrialStatus + " - Fail           " );
        }
        else if (currentTrialStatus == 2){
            lblInfo_Status.setText("Status: " + currentTrialStatus + " - Success " );
        }
        else{
            lblInfo_Status.setText("Status: " + currentTrialStatus);
        }
        //lblInfo_Status.setText("Status: " + currentTrialStatus );
        lblInfo_Duration.setText("Duration: " + (currentTrialEnd - currentTrialStart)  +" ms");
    }

    public void print(String text){
        lblInstantInfo.setText(text);
    }

    @Override
    public void stateChanged(ChangeEvent arg0) {
        if (!fileOpened) return;
        System.out.println(jListTrials.getSelectedIndex());
        currentTrialIndex = jListTrials.getSelectedIndex();
        if (currentTrialIndex < 0)
            return;
        // currentTrialIndex = jListTrials.getSelectedIndex();
        _updateFr();

        int a = timeSlider.getValue();
        System.out.println("Slider status changed: " + a);
        trialArray.get(trialArray.size() / SLIDER_DIVISION * a);

        int tmpin = (int) ((int) trialArray.get(currentTrialIndex).points
                .size() / (SLIDER_DIVISION * 1.0) * a) - 1;
        if (tmpin < 0)
            tmpin = 0;
        setSliderPointTime(tmpin);
    }
    
    public void setSliderPointTime(int tmpin){
        System.out.println(trialArray.get(currentTrialIndex).getPoint(tmpin)
                .toString());
        print (trialArray.get(currentTrialIndex).getPoint(tmpin)
                .toString());
        canvas.updateData(
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin).getX(),
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin).getY(),
                (int) trialArray.get(currentTrialIndex).getPoint(tmpin).getTime(),
                trialArray.get(currentTrialIndex).getPoint(tmpin).getDirX(),
                trialArray.get(currentTrialIndex).getPoint(tmpin).getDirY()
                );
    }

    
    @SuppressWarnings("static-access")
    public void infoBox(String infoMessage)
    {
        fadePopUp pop = new fadePopUp(infoMessage);
        pop.main(null); 
    }
    
    public void addRecentFile(String path){
        //adds file to menu list of recent files. If file already exists in the list, put it on top..

        for (int i = 0; i < paths.size(); i++){
            if (paths.get(i).equals(path) ){
                paths.remove(i);
            }
        }
        
        paths.add(path);
        menuRecentFiles.removeAll();
        
        
        for (int i = 0; i < paths.size(); i++){
            final JMenuItem menuItem = new JMenuItem( paths.get(i) ,
                    KeyEvent.VK_T);
            menuItem.addActionListener(new ActionListener(){
                @Override
                public void actionPerformed(ActionEvent arg0) {
                    // TODO Auto-generated method stub
                    try{
                        openFile(menuItem.getText());
                    }
                    catch(Exception e){ }
                    
                }
                
            });
            menuRecentFiles.add(menuItem);
        }
    }
    
    public void launchBinaryWindow(){
        JFrame frBinary = new JFrame("Binary (stats.)");
        frBinary.setVisible(true);
        CanvasStats canvasStats = new CanvasStats();
        canvasStats.setPrefSize();
        int data[] = {5,0,0,0,0,5,5,5,5,5,0,5};
        frBinary.add(canvasStats);
        canvasStats.setData(data);
        frBinary.pack();
    }
    
    public void exitAll(){
        System.exit(0);
    }
}


class counterThread extends Thread {
    boolean runningc = true; 
    public void run(){
        while(runningc){
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                //e.printStackTrace();
            }
            //System.out.println(FrameMain.mouseCounter);
            if (FrameMain.mouseCounter > 0){
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