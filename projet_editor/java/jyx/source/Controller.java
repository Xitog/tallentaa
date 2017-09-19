package jyx;

import java.io.File;
import javax.swing.*;

public class Controller {
    
    // Event
    static int NEW = 1;
    static int OPEN = 2;
    static int SAVE = 3;
    static int SAVE_AS = 4;
    static int QUIT = 5;
    static int WRITING = 6; // ING because the action to write the text is not done by the Controller
    static int REMOVING = 7; // Same !
    static int CARRET_MOVE = 8;
    static int ABOUT = 9;
    static int UNDO = 10;
    
    // State
    static int OPENING = 1;
    static int WORKING = 2;
    static int UNDOING = 3;
    
    Jyx jyx;
    int current_state;
    
    Controller (Jyx jyx) {
        this.jyx = jyx;
        current_state = Controller.WORKING;
    }
    
    void setState(int new_state) {
        this.current_state = new_state;
    }
    
    int getCurrentState() {
        return this.current_state;
    }
    
    void updateInfo() {
        int caretPos = jyx.getTextPane().getCaretPosition();
        JyxDocument jyxdoc = (JyxDocument) jyx.getTextPane().getDocument();
        Analyze ana = new Analyze(jyxdoc, caretPos);
        jyx.setInfo(" " + ana.getNbChars() + " characters on " + ana.getNbLines() + " lines. " +
                    "Caret at" + 
                    " char in text : " + caretPos + "/" + ana.getNbChars() + 
                    " line in lines : " + ana.getOffsetLine() + "/" + ana.getNbLines() + 
                    " char in line : " + ana.getOffsetPosInLine() + "/" + 
                        ana.getOffsetLineLength() + ". " +
                    " Modifications : " + jyxdoc.getActions().size() + ".");
    }
    
    void update(int event, int int1, int int2) {
        if (event == Controller.CARRET_MOVE) {
            this.updateInfo();
        }
    }
    
    void update(int event, File file) {
        if (event == Controller.OPEN) {
            JyxDocument jyxdoc = (JyxDocument) jyx.getTextPane().getDocument();
            setState(OPENING);
            jyx.getTextPane().setText(jyx.readFile(file));
            jyx.getFrame().setTitle(file.getName() + " - Jyx 1.0");
            jyx.setCurrentFile(file);
            jyx.resetChanged();
            setState(WORKING);
        }
    }
    
    void update(int event) {
        this.update(event, 0, null);
    }
    
    void update(int event, int offset, String content) {
        JyxDocument jyxdoc = (JyxDocument) jyx.getTextPane().getDocument();
        if (event == Controller.NEW) {
            jyx.getTextPane().setText("");
            jyx.getFrame().setTitle("Jyx 1.0");
            jyx.setCurrentFile(null);
            jyx.resetChanged();
        } else if (event == Controller.SAVE) {
            File file;
            String new_title;
            if (jyx.getCurrentFile() == null) {
                file = new File(JyxConfig.SAVE_BUFFER);
            } else {
                file = jyx.getCurrentFile();
            }
            new_title = file.getName() + " - Jyx 1.0"; 
            jyx.saveFile(file, jyx.getTextPane().getText());
            jyx.resetChanged();
            jyx.getFrame().setTitle(new_title);
        } else if (event == Controller.WRITING || event == Controller.REMOVING) {
            if (current_state != Controller.UNDOING && current_state != Controller.OPENING) {
                if (event == Controller.WRITING) {
                    jyxdoc.addAction(new Action(offset, content, Action.WRITE));
                } else if (event == Controller.REMOVING) {
                    jyxdoc.addAction(new Action(offset, content, Action.REMOVE));
                }
                jyx.switchUndo();
            }
            if (current_state != Controller.OPENING && !jyx.getHasChanged()) {
                String old_title = jyx.getFrame().getTitle();
                String new_title = "(Changed) " + old_title;
                jyx.getFrame().setTitle(new_title);
                jyx.setChanged();
            }
            this.updateInfo();
        } else if (event == Controller.UNDO) {
            this.setState(Controller.UNDOING);
            if (jyxdoc.getActions().size() > 0)
            {
                System.out.println("There is : " + jyxdoc.getActions().size());
                for (int i = 0; i < jyxdoc.getActions().size(); i++) {
                    System.out.println("" + i + ". " + jyxdoc.getActions().get(i));
                }
                Action a = jyxdoc.getActions().get(jyxdoc.getActions().size()-1);
                if (a.type == Action.REMOVE) {
                    jyxdoc.insertString(a.offset, a.str, null);
                } else {
                    jyxdoc.remove(a.offset, a.str.length());
                }
                jyxdoc.getActions().remove(jyxdoc.getActions().size()-1);
            }
            this.setState(Controller.WORKING);
            jyx.switchUndo();
            this.updateInfo();
        } else if (event == Controller.ABOUT) {
            JOptionPane.showMessageDialog(jyx.getFrame(), "Jyx - Damien Gouteux, 2016. Made with ❤", "À propos", JOptionPane.INFORMATION_MESSAGE);
        } else {
            jyx.setInfo(" Unknown event : " + event);
        }
    }
    
}