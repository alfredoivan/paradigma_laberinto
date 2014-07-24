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
        //System.out.println("New Trial created.");
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
        //parse a x y time point from a string, adds it to list of points.
        if (pnt == null)return;
        if (pnt.equals("")) return;
        stringLines.add(pnt);
        
        String[] parts = pnt.split(",", 10);
        String parts1 = correctMultiplePoints( parts[1] );
        String parts2 = correctMultiplePoints( parts[2] );
        String parts3 = correctMultiplePoints( parts[3] );
        String parts4 = correctMultiplePoints( parts[4] );
        
        
        int posx = (int)Double.parseDouble( parts1 );
        
        int posy = (int)Double.parseDouble( parts2 );
        
        double dirx = Double.parseDouble( parts3 ) ;
        double diry = Double.parseDouble( parts4 ) ;
        
        
        
        int z = Integer.parseInt(parts[0]); //this being the time.
        
        points.add(new PointTime(posx,posy, z, dirx, diry));
    }
    
    public String correctMultiplePoints(String input){
        //input has multiple points. should return a string from 0 to the 2nd point
        String output = input;
        int count = output.length() - output.replace(".", "").length();
        //System.out.println("Occurrences of dots: "+count);
        if (count == 1){
            //only one dot, so it is ok like this
            return output;
        }
        if (count >1){
            //more than one dot, remove everything from the second one.
            int tempcount = 0;
            for (int i=0; i< input.length(); i++){
                if (input.charAt(i) == '.'){
                    tempcount++;
                }
                
                if (tempcount == 2){
                    //second occurrence, remove everything from 0 to here.
                    output = input.substring(0, i);
                    return output;
                }
            }
            
        }
        
        return output;
        
    }
    
    public void printAllPoints(){
        //for (String temp : stringLines) {
            //System.out.println(temp);
        //}
        for (Point temp : points) {
            System.out.println(temp.toString());
        }
    }
    
    
    public PointTime getPoint(int pos){
        if (pos == -1){
            pos = points.size() -1;
        }
        return points.get(pos);
    }
}
