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
    static int REMOVING = 6; // Same !
    static int CARRET_MOVE = 7;
    static int ABOUT = 8;
    
    // State
    static int OPENING = 1;
    static int WORKING = 2;
    
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
        Analyze ana = new Analyze(this.jyx.getTextPane().getDocument(), caretPos);
        jyx.setInfo(" " + ana.getNbChars() + " characters on " + ana.getNbLines() + " lines. Caret at " + caretPos + ", line " + ana.getCarretLine() + ".");
    }
    
    void update(int event, int int1, int int2) {
        if (event == Controller.CARRET_MOVE) {
            this.updateInfo();
        }
    }
    
    void update(int event, File file) {
        if (event == Controller.OPEN) {
            setState(OPENING);
            jyx.getTextPane().setText(jyx.readFile(file));
            jyx.getFrame().setTitle(file.getName() + " - Jyx 1.0");
            jyx.setCurrentFile(file);
            jyx.resetChanged();
            setState(WORKING);
        }
    }
    
    void update(int event) {
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
        } else if (event == Controller.WRITING) {
            if (current_state != Controller.OPENING && !jyx.getHasChanged()) {
                String old_title = jyx.getFrame().getTitle();
                String new_title = "(Changed) " + old_title;
                jyx.getFrame().setTitle(new_title);
                jyx.setChanged();
            }
            this.updateInfo();
        } else if (event == Controller.ABOUT) {
            JOptionPane.showMessageDialog(jyx.getFrame(), "Jyx - Damien Gouteux, 2016. Made with ❤", "À propos", JOptionPane.INFORMATION_MESSAGE);
        } else {
            jyx.setInfo(" Unknown event : " + event);
        }
    }
    
}