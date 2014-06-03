package labyrinth_log;

import java.awt.Point;
import java.util.ArrayList;

public class Trial {
	ArrayList<String> stringLines = new ArrayList<String>();
	
	ArrayList<PointTime> points = new ArrayList<PointTime>();
	
	int status = 0; //0 undefined , 1 lose, 2 win
	int start = 0;
	int duration = 0;
	int end = 0;
	
	public Trial(){
		System.out.println("New Trial created.");
		status = 0;
		start = 0;
		duration = 0;
		end = 0;
		points = new ArrayList<PointTime>();
		stringLines = new ArrayList<String>();
	}
	
	public int getStart() {
		return start;
	}

	public int getEnd() {
		return end;
	}
	
	public int getDuration() {
		return duration;
	}

	public int getStatus() {
		return status;
	}

	public void setStatus(int status) {
		this.status = status;
		start = points.get(0).getTime();
		end = points.get(points.size() - 1).getTime();
		duration = end - start;
		
	}

	public void addPoint(String pnt){
		if (pnt == null)return;
		stringLines.add(pnt);
		int a = pnt.indexOf(",");
		String tempstr = pnt.substring( a + 1 );
		String subtemp = tempstr.substring(0, tempstr.indexOf(","));
		//System.out.println("subtemp: "+subtemp);
		//System.out.println("X : "+pnt.substring(a, tempstr.indexOf(",") ) ) ;
		int posx = Integer.parseInt( subtemp.substring(0, subtemp.indexOf(".")) ) ;
		
		//System.out.println("posx: "+posx);
		
		String tempstr2 = tempstr.substring(tempstr.indexOf(",")+1);
		String subtemp2 = tempstr2.substring(0, tempstr2.indexOf(","));
		//System.out.println("tempstr2: "+tempstr2);
		//System.out.println("subtemp2: "+subtemp2);
		
		int posy = Integer.parseInt( subtemp2.substring(0, subtemp2.indexOf(".")) ) ;
		
		
		//System.out.println("posy: "+posy);
		
		String tempfl = pnt.substring( 0, a );
		//System.out.println("tempfl: "+ tempfl);
		
		int z = Integer.parseInt(tempfl); //this being the time.
		
		points.add(new PointTime(posx,posy, z));
	}
	
	public void printAllPoints(){
		for (String temp : stringLines) {
			//System.out.println(temp);
		}
		for (Point temp : points) {
			System.out.println(temp.toString());
		}
	}
	
	
	public PointTime getPoint(int pos){
		return points.get(pos);
	}
}
