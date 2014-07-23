package labyrinth_log;

import java.awt.Point;

public class PointTime extends Point{
    /**
     * 
     */
    private static final long serialVersionUID = 1L;
    int time;
    
    PointTime(int x, int y, int z){
        this.x = x;
        this.y = y;
        time = z;
    }
    
    int getTime(){
        return time;
    }
    
    int iGetX(){
        return x;
    }
    int iGetY(){
        return y;
    }
    
    public String toString(){
        return "labyrinth_log.PointTime[x="+x+",y="+y+",z="+time+"]";
    }
}
