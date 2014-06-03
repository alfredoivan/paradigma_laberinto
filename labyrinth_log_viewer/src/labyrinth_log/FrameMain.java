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
	private Closer Handler;
	CanvasGraph canvas = new CanvasGraph();
	JSlider timeSlider;
	JList txtNum;

	DefaultListModel listModel = new DefaultListModel();
	JLabel lblInfo;
	JLabel lblInfo_Start;
	JLabel lblInfo_End;
	JLabel lblInfo_Duration;
	JLabel lblInfo_Status;
	JLabel lblInstantInfo;

	ArrayList<Trial> trialArray = new ArrayList<Trial>();
	int currentTrialIndex = 0;
	
	int currentTrialStart = 0;
	int currentTrialEnd = 0;
	int currentTrialStatus = 0; //0 unknown, 1 lose, 2 win
	
	boolean fileOpened = false; //true = at least one file has been opened
	
	final int SLIDER_DIVISION = 1000;
	
	FrameMain() {

		Handler = new Closer();
		setTitle("Labyrinth log viewer");
		setSize(640, 480);
		addWindowListener(Handler);
		addComponents();
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
		
		JButton btnUpdate = new JButton("Update");
		btnUpdate.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				System.out.println("Updating...");
				updateFrame();
			}} );

		JPanel pnlAll = new JPanel();
		pnlAll.setLayout(new BorderLayout());

		JPanel pnlCanvas = new JPanel();
		pnlCanvas.setLayout(new BorderLayout());

		JPanel pnlButton = new JPanel();
		pnlButton.setLayout(new GridLayout(0, 1));

		JLabel lblTitle = new JLabel("Labyrinth Log");
		lblInstantInfo = new JLabel("aaaaa123456---___123");

		pnlAll.add(lblTitle, BorderLayout.NORTH);
		
		JPanel pnlII = new JPanel();
		pnlII.add(lblInstantInfo, BorderLayout.LINE_END);
		pnlAll.add(pnlII, BorderLayout.SOUTH);

		JPanel pnlInterButton = new JPanel();
		pnlInterButton.setLayout(new BorderLayout());

		pnlInterButton.add(btnLoad, BorderLayout.NORTH);
		pnlCanvas.add(canvas, BorderLayout.CENTER);

		timeSlider = new JSlider(JSlider.HORIZONTAL, 0, SLIDER_DIVISION, 0);
		timeSlider.addChangeListener(this);

		// listModel.addElement("Trial 0");
		// listModel.addElement("Trial 1");
		// listModel.addElement("Trial 2");
		listModel.addElement("-----------------");
		txtNum = new JList(listModel);
		txtNum.setVisibleRowCount(5);

		// txtNum.setPreferredSize(new Dimension(10,20) );
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setViewportView(txtNum);
		pnlInterButton.add(scrollPane, BorderLayout.CENTER);
		pnlInterButton.add(btnUpdate, BorderLayout.SOUTH);

		JPanel pnlSuperInfo = new JPanel();
		pnlSuperInfo.setLayout(new BorderLayout());

		JPanel pnlInfo = new JPanel();
		pnlInfo.setLayout(new GridLayout(0, 1, 5, 2));

		lblInfo = new JLabel("Trial info:");
		lblInfo_Start = new JLabel("Start:");
		lblInfo_End = new JLabel("End:");
		lblInfo_Status = new JLabel("Status:");
		lblInfo_Duration = new JLabel("Duration:");

		pnlButton.add(pnlInterButton);

		pnlInfo.add(lblInfo);
		pnlInfo.add(lblInfo_Start);
		pnlInfo.add(lblInfo_End);
		pnlInfo.add(lblInfo_Duration);
		pnlInfo.add(lblInfo_Status);
		
		

		pnlSuperInfo.add(pnlInfo, BorderLayout.SOUTH);
		pnlButton.add(pnlSuperInfo);

		pnlCanvas.add(timeSlider, BorderLayout.SOUTH);

		pnlAll.add(pnlCanvas, BorderLayout.CENTER);
		pnlAll.add(pnlButton, BorderLayout.LINE_START);
		this.add(pnlAll);
	}

	public void openFile(String path) throws FileNotFoundException, IOException {
		System.out.println("openFile");
		fileOpened = true;
		trialArray.removeAll(trialArray);
		try (BufferedReader br = new BufferedReader(new FileReader("" + path))) {
			StringBuilder sb = new StringBuilder();
			String line = br.readLine();
			int counter = 0; // reaches 4 => finished this trial.
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
					}
					//currentTrialStart = temp.getStart();
					//currentTrialEnd = temp.getEnd();
					//currentTrialStatus = temp.getStatus();
					
					trialArray.add(temp);
					temp = new Trial();
					counter = 0;
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

			// txtNum = new JList(listModel);
		}
	}

	public static void main(String args[]) {
		@SuppressWarnings("unused")
		JFrame f;
		f = new FrameMain();
	}
	
	public void updateFrame(){
		if (!fileOpened) return;
		//update function: First checks if variables are correct, then calls other f.
		currentTrialIndex = txtNum.getSelectedIndex();
		if (currentTrialIndex < 0)
			return;
		
		timeSlider.setValue(0);
		_updateFr();
		
		canvas.repaint();
	}
	
	private void _updateFr(){
		//private function that only updates labels with updated info.
		currentTrialStart = trialArray.get(currentTrialIndex).getStart();
		currentTrialEnd = trialArray.get(currentTrialIndex).getEnd();
		currentTrialStatus = trialArray.get(currentTrialIndex).getStatus();
		
		
		lblInfo.setText("Trial info: " + currentTrialIndex );
		lblInfo_Start.setText("Start: " + currentTrialStart );
		lblInfo_End.setText("End: " + currentTrialEnd );
		lblInfo_Status.setText("Status: " + currentTrialStatus );
		lblInfo_Duration.setText("Duration: " + (currentTrialEnd - currentTrialStart) );
	}
	
	public void print(String text){
		lblInstantInfo.setText(text);
		
	}
	
	@Override
	public void stateChanged(ChangeEvent arg0) {
		if (!fileOpened) return;
		System.out.println(txtNum.getSelectedIndex());
		currentTrialIndex = txtNum.getSelectedIndex();
		if (currentTrialIndex < 0)
			return;
		// currentTrialIndex = txtNum.getSelectedIndex();
		_updateFr();
		
		int a = timeSlider.getValue();
		System.out.println("Slider status changed: " + a);
		trialArray.get(trialArray.size() / SLIDER_DIVISION * a);

		int tmpin = (int) ((int) trialArray.get(currentTrialIndex).points
				.size() / (SLIDER_DIVISION * 1.0) * a) - 1;
		if (tmpin < 0)
			tmpin = 0;
		System.out.println(trialArray.get(currentTrialIndex).getPoint(tmpin)
				.toString());
		print (trialArray.get(currentTrialIndex).getPoint(tmpin)
				.toString());
		canvas.updateData(
				(int) trialArray.get(currentTrialIndex).getPoint(tmpin).getX(),
				(int) trialArray.get(currentTrialIndex).getPoint(tmpin).getY(),
				(int) trialArray.get(currentTrialIndex).getPoint(tmpin)
						.getTime());
	}
}

class Closer extends WindowAdapter {
	public void windowClosing(WindowEvent event) {
		System.exit(0);
	}
}