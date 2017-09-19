package jyx;

import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.Style;
import javax.swing.text.StyleContext;
import javax.swing.text.StyleConstants;
import javax.swing.text.AttributeSet;
import javax.swing.text.Element;
import javax.swing.text.BadLocationException;

import java.util.ArrayList;

public class JyxDocument extends DefaultStyledDocument {
    
    Jyx panel;
    
    Style base;
    Style bold;
    Style italic;
    
    ArrayList<Action> actions;
    
    public JyxDocument(Jyx panel) {
        super();
        this.panel = panel;
        
        Style def = StyleContext.getDefaultStyleContext().getStyle(StyleContext.DEFAULT_STYLE);
        this.base = this.addStyle("regular", def);
        StyleConstants.setFontFamily(def, "Verdana"); // Consolas
        this.italic = this.addStyle("italic", base);
        StyleConstants.setItalic(this.italic, true);
        this.bold = this.addStyle("bold", base);
        StyleConstants.setBold(this.bold, true);
        
        this.actions = new ArrayList<Action>();
    }
    
    public ArrayList<Action> getActions() {
        return this.actions;
    }
    
    public void addAction(Action a) {
        this.actions.add(a);
    }
    
    @Override
    public void insertString(int offset, String str, AttributeSet a) {
        try {
            str = str.replaceAll("\t", "    ");
            if (str.charAt(0) == '*' && str.charAt(str.length()-1) == '*') {
                super.insertString(offset, str, this.getStyle("bold"));
            } else {
                super.insertString(offset, str, this.getStyle("regular"));
            }
            panel.getController().update(Controller.WRITING, offset, str);
            System.out.println("Inserted : offset = " + offset + " str = " + str);
            if (str.length() > 1) {
                this.parse_multiple_elem(offset);
            } else {
                this.parse(offset);
            }
        } catch (BadLocationException ble) {
            System.out.println("Bad location exception");
        }
    }
    
    public int elementLength(Element e) {
        return e.getEndOffset() - e.getStartOffset() - 1;
    }
    
    public String elementText(Element e) {
        String s = "";
        try {
            s = this.getText(e.getStartOffset(), this.elementLength(e));
        } catch (BadLocationException ble) {
            System.out.println("Bad location exception in parse for offset = " + e.getStartOffset());
        } finally {
            return s;
        }
    }
    
    // Iterate over all the elements of the newly insert string
    public void parse_multiple_elem(int offset) {
        Element root = this.getDefaultRootElement();
        int elem_index = root.getElementIndex(offset);
        for (int i = elem_index; i < root.getElementCount(); i++) {
            Element e = root.getElement(i);
            this.parse(e.getStartOffset());
        }
    }
    
    public void parse(int offset) {
        Element e = this.getParagraphElement(offset);
        int e_length = this.elementLength(e);
        if (e_length > 1) {
            String s = this.elementText(e);
            if (s.startsWith("--")) {
                this.setCharacterAttributes(e.getStartOffset(), e_length, this.getStyle("italic"), true);
                return;
            } else if (s.startsWith("= Lundi") || s.startsWith("= Mardi") || s.startsWith("= Mercredi") || s.startsWith("= Jeudi") || s.startsWith("= Vendredi") || s.startsWith("= Samedi") || s.startsWith("= Dimanche")) {
                this.setCharacterAttributes(e.getStartOffset(), e_length, this.getStyle("bold"), true);
                return;
            }
        }
        this.setCharacterAttributes(e.getStartOffset(), e_length, this.getStyle("regular"), true);
    }
    
    public String safeGetText(int offset, int length) { // don't translate \n by \r\n on windows :-)
        String text = "";
        try {
            text = this.getText(offset, length);
        } catch (BadLocationException ble) {
            System.out.println("Bad location exception");
        } finally {
            return text;
        }
    }
    
    public String safeGetText() {
        return this.safeGetText(0, this.getLength());
    }
    
    @Override
    public void remove(int offset, int len) {
        /*
        int backup_offset = offset;
        int backup_len = len;
        String s = this.safeGetText();
        if (len == 1) {
            Analyze ana = new Analyze(s, offset);
            int start_of_line = ana.getStartOfLine(ana.getCarretLine());
            int char_count = 0;
            for (int i = start_of_line + 1; i < s.length() && s.charAt(i) != '\n' && i < offset; i++) {
                char_count += 1;
            }
            
            System.out.println("START of line " + ana.getCarretLine() + " @" + start_of_line);
            int nearest_tab = 0;
            if (offset == start_of_line || (offset - start_of_line + 1) % 4 == 0) {
                nearest_tab = offset;
            }
            System.out.println("Position of offset is @" + offset + ". Nearest TAB is @" + nearest_tab);
            char_count = 0;
            int tab_count = 0;
            int last_tab_offset = start_of_line;
            int white_count = 0;
            boolean only_white = true;
            for (int i = start_of_line; i < s.length() && s.charAt(i) != '\n' && i <= offset; i++) {
                System.out.println("@" + i + ". " + s.charAt(i));
                char_count += 1;
                if (char_count != 0 && (char_count % 4) == 0) {
                    tab_count += 1;
                    if (i != offset) {
                        last_tab_offset = i;
                        white_count = 0;
                    }
                    System.out.println("TAB");
                } else if (Character.isWhitespace(s.charAt(i))) {
                    white_count += 1;
                } else {
                    only_white = false;
                }
            }
            System.out.println("Last tab at " + last_tab_offset + " white_count = " + white_count);
            if (only_white) {
                offset = last_tab_offset;
                len = white_count;
            }
            if (len == 0) {
                offset = backup_offset;
                len = backup_len;
                System.out.println("0 length removal detected!");
            }
        }*/
        String save = "";
        try {
            //s = this.getText(offset, len);
            save = this.safeGetText(offset, len);
            System.out.println("Preparing to remove : " + save);
            super.remove(offset, len);
            if (offset > 1) {
                this.parse(offset-1);
            } else {
                this.parse(0);
            }
            
        } catch (BadLocationException ble) {
            System.out.println("JyxDocument::remove -> Bad location exception");
        }
        panel.getController().update(Controller.REMOVING, offset, save);
        //System.out.println("Removed : offset = " + offset + " len = " + len + " s = [" + s + "]");
    }
    
    /*
    @Override
    public void removeUpdate(DefaultDocumentEvent chng) {
        super.removeUpdate(chng);
        panel.getController().update(Controller.REMOVING);
        System.out.println("Removing");
    }
    */
}