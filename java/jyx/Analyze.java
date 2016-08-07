package jyx;

import java.util.ArrayList;
import javax.swing.text.Document;
import javax.swing.text.BadLocationException;

public class Analyze {
    
    int nb_lines;
    int nb_chars;
    ArrayList<Integer> starts_of_line;
    int pos_line;
    
    Analyze(Document dsd, int offset) {
        this();
        try {
            nb_chars = dsd.getLength();
            String s = dsd.getText(0, nb_chars);
            analyze(s, offset);
        } catch (BadLocationException ble) {
            System.out.println("Bad location exception");
            analyze("", offset);
        }
    }
    
    Analyze(String s, int offset) {
        this();
        this.nb_lines = 1;
        this.nb_chars = 0;s.length();
        this.pos_line = -1;
        this.starts_of_line = new ArrayList<Integer>();
        this.addStartOfLine(0);
        analyze(s, offset);
    }
    
    Analyze() {
        this.nb_lines = 1;
        this.nb_chars = 0;
        this.pos_line = -1;
        this.starts_of_line = new ArrayList<Integer>();
        this.addStartOfLine(0);
    }
    
    void analyze(String s, int offset) {
        this.nb_chars = s.length();
        // System.out.println("getLength() of Document : " + nb_chars + " vs length() of String : " + s.length());
        for (int i=0; i < this.nb_chars; i++) {
            if (i == offset) {
                this.setPosLine(this.nb_lines);
            }
            if (s.charAt(i) == '\n') {
                this.nb_lines += 1;
                this.addStartOfLine(i);
                // System.out.println(">>> New line at " + i);
            }
            //System.out.println(">>> " + i + ". [" + s.charAt(i) + "]");
        }
        if (offset == this.nb_chars) {
            this.setPosLine(this.nb_lines);
        }
    }
    
    void setNbLines(int i) {
        this.nb_lines = i;
    }
    
    int getNbLines() {
        return this.nb_lines;
    }
    
    void setNbChars(int i) {
        this.nb_chars = i;
    }
    
    int getNbChars() {
        return this.nb_chars;
    }
    
    void addStartOfLine(int pos) {
        this.starts_of_line.add(pos);
    }
    
    void setPosLine(int i) {
        this.pos_line = i;
    }
    
    int getCarretLine() {
        return this.pos_line;
    }
    
    int getStartOfLine(int lineNum) {
        if (lineNum < 1) {
            System.out.println("No!"); // TODO:
            return 0;
        }
        return (int) this.starts_of_line.get(lineNum-1);
    }
}