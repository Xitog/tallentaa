package jyx;

public class Action {
        
    String str;
    int offset;
    int type;
    
    static int REMOVE = 0;
    static int WRITE = 1;
    
    Action(int offset, String str, int type) {
        this.str = str;
        this.offset = offset;
        this.type = type;
    }
    
    @Override
    public String toString() {
        if (this.type == Action.REMOVE) {
            return "Remove at " + this.offset;
        } else {
            if (this.str.length() > 10) {
                return "Write at " + this.offset + " : " + this.str.substring(0, 10) + "...";
            } else {
                return "Write at " + this.offset + " : " + this.str;
            }
        }
    }
}