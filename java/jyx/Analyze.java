package jyx;

import java.util.ArrayList;
import javax.swing.text.BadLocationException;
import javax.swing.text.Element;

public class Analyze {
    
    Analyze(JyxDocument dsd, int offset) {
        analyze(dsd, offset);
    }
    
    JyxDocument doc;
    int offset;
    int offsetElementIndex;
    Element offsetElement;
    
    void analyze(JyxDocument doc, int offset) {
        this.doc = doc;
        this.offset = offset;
        Element root = this.doc.getDefaultRootElement();
        //for (int i = 0; i < root.getElementCount(); i++) {
        //    Element e = root.getElement(i);
        //    System.out.println("" + i + ". s=" + e.getStartOffset() + " e=" + e.getEndOffset());
        //}
        this.offsetElementIndex = root.getElementIndex(this.offset);
        this.offsetElement = root.getElement(offsetElementIndex);
    }
    
    int getNbChars() {
        return this.doc.getLength();
    }
    
    int getNbLines() {
        return this.doc.getDefaultRootElement().getElementCount();
    }

    int getOffsetLine() {
        return this.offsetElementIndex + 1;
    }
    
    int getOffsetLineLength() {
        return offsetElement.getEndOffset() - offsetElement.getStartOffset() - 1; // \n not counted
    }
    
    int getOffsetPosInLine() {
        return this.offset - offsetElement.getStartOffset();
    }
    
    Element getOffsetElement() {
        return offsetElement;
    }
    
    /*
    int getStartOfLine(int lineNum) {
        if (lineNum < 1) {
            System.out.println("No!"); // TODO:
            return 0;
        }
        return (int) this.starts_of_line.get(lineNum-1);
    }
    */
}