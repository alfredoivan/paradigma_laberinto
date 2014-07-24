package labyrinth_log;

import java.awt.Point;

public class PointTime extends Point{
    /**
     * 
     */
    private static final long serialVersionUID = 1L;
    int time;
    double dirx;
    double diry;
    
    PointTime(int x, int y, int z, double directionx, double directiony){
        this.x = x;
        this.y = y;
        this.time = z;
        this.dirx = directionx;
        this.diry = directiony;
    }
    
    int getTime(){
        return time;
    }
    
    double getDirX(){
        return dirx;
    }
    double getDirY(){
        return diry;
    }
    
    int iGetX(){
        return x;
    }
    int iGetY(){
        return y;
    }
    
    public String toString(){
        return "labyrinth_log.PointTime[x="+x+",y="+y+",time="+time+"ms "+",dirx="+dirx +",diry="+diry +"]";
    }
}
