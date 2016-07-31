package jyx;

import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;

import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.AttributeSet;
import javax.swing.text.AbstractDocument.DefaultDocumentEvent;
import javax.swing.event.CaretListener;
import javax.swing.event.CaretEvent;

import java.io.File;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.FileOutputStream;
import java.io.UnsupportedEncodingException;

import java.nio.charset.Charset;

//import com.sun.java.swing.plaf.gtk.GTKLookAndFeel;
//import com.sun.java.swing.plaf.motif.MotifLookAndFeel;
//import com.sun.java.swing.plaf.windows.WindowsLookAndFeel;

public class Jyx extends JPanel implements ActionListener, CaretListener {
    
    JTextPane jtp;
    JLabel jl;
    JFrame frame;
    File currentFile;
    boolean launch;
    boolean hasChanged;
    Controller master;
    
    public Jyx(JFrame frame) {
        this.frame = frame;
        this.master = new Controller(this);
        this.hasChanged = false;
        
        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        //Border border = BorderFactory.createEtchedBorder();
        //setBorder(BorderFactory.createTitledBorder(border, "Texte"));
        
        jtp = new JTextPane();
        jtp.setDocument(new JyxDocument(this));
        jtp.addCaretListener(this);
        //jtp.setPreferredSize(new Dimension(400, 600));
        //jtp.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        gbc.gridx = 0; // column
        gbc.gridy = 0; // row
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        gbc.weightx = 0.95;
        gbc.weighty = 0.99;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.anchor = GridBagConstraints.NORTHWEST;
        add(jtp, gbc);
        
        JScrollPane scrollPane = new JScrollPane(jtp);
        gbc.gridx =1;
        gbc.gridy = 0;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        gbc.weightx = 0.05;
        gbc.weighty = 0.99;
        add(scrollPane, gbc);
        //scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
   
        jl = new JLabel();
        gbc.gridx = 0; // column
        gbc.gridy = 1; // row
        gbc.gridwidth = 2;
        gbc.gridheight = 1;
        gbc.weightx = 1.00;
        gbc.weighty = 0.01;
        add(jl, gbc);
        jl.setVerticalAlignment(SwingConstants.BOTTOM);
        jl.setText(" A little hello from Jyx");
        //jl.setMaximumSize(new Dimension(jl.getMaximumSize().width, 20));
        
        try {
            File file = new File(JyxConfig.SAVE_BUFFER);
            if (file.exists() && !file.isDirectory()) {
                master.update(Controller.OPEN, file);
            }
        } catch (Exception e) {
            System.err.format("IOException: %s%n", e);
        }
        
    }
    
    public void setInfo(String s) {
        this.jl.setText(s);
    }
    
    public JFrame getFrame() {
        return this.frame;
    }
    
    public boolean getHasChanged() {
        return this.hasChanged;
    }
    
    public void setChanged() {
        this.hasChanged = true;
    }
    
    void resetChanged() {
        this.hasChanged = false;
    }
    
    JTextPane getTextPane() {
        return this.jtp;
    }
    
    void setCurrentFile(File file) {
        this.currentFile = file;
    }
    
    File getCurrentFile() {
        return this.currentFile;
    }
    
    public Controller getController() {
        return this.master;
    }
    
    public String readFile(File file) {
        Charset charset = Charset.forName("UTF-8"); //("US-ASCII");
        StringBuffer sb = new StringBuffer();
        try {
            FileInputStream fis = new FileInputStream(file);
            InputStreamReader isr = new InputStreamReader(fis, charset);
            BufferedReader reader = new BufferedReader(isr);
            String line = null;
            while ((line = reader.readLine()) != null) {
                sb.append(line + "\n");
            }
        } catch (IOException ioe) {
            System.err.format("IOException: %s%n", ioe);
        }
        return sb.toString();
    }
    
    public void saveFile(File file, String content) {
        try {
            FileOutputStream fos = new FileOutputStream(file);
            byte[] bytes = content.getBytes("UTF-8");
            fos.write(bytes);
            fos.close();
        } catch (UnsupportedEncodingException uee) {
            System.err.format("EncodingException: %s%n", uee);
        } catch (IOException ioe) {
            System.err.format("IOException: %s%n", ioe);
        }
    }
    
    static class Controller {
        
        // Event
        static int NEW = 1;
        static int OPEN = 2;
        static int SAVE = 3;
        static int SAVE_AS = 4;
        static int QUIT = 5;
        static int WRITING = 6; // ING because the action to write the text is not done by the Controller
        static int REMOVING = 6; // Same !
        static int CARRET_MOVE = 7;
        
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
        
        void update(int event, int int1, int int2) {
            if (event == Controller.CARRET_MOVE) {
                Analyze ana = analyze();
                jyx.setInfo(" " + ana.getNbChars() + " characters on " + ana.getNbLines() + " lines. Caret at " + jyx.getTextPane().getCaretPosition());
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
                Analyze ana = analyze();
                jyx.setInfo(" " + ana.getNbChars() + " characters on " + ana.getNbLines() + " lines. Caret at " + jyx.getTextPane().getCaretPosition());
            } else {
                jyx.setInfo(" Unknown event : " + event);
            }
        }
            
        Analyze analyze() {
            Analyze ana = new Analyze();
            int nb_lines = 1;
            int nb_chars = 0;
            try {
                nb_chars = jyx.getTextPane().getDocument().getLength();
                String s = jyx.getTextPane().getDocument().getText(0, nb_chars);
                // System.out.println("getLength() of Document : " + nb_chars + " vs length() of String : " + s.length());
                for (int i=0; i < nb_chars; i++) {
                    if (s.charAt(i) == '\n') {
                        nb_lines += 1;
                    }
                    //System.out.println(">>> " + i + ". [" + s.charAt(i) + "]");
                }
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception");
            } finally {
                ana.setNbLines(nb_lines);
                ana.setNbChars(nb_chars);
            }
            return ana;
        }
        
        int getNearestTab(int offset) {
            int nearest_tab = ((int)(offset / 4)) * 4;
            //System.out.println("I want to delete here : " + offset + " and the nearest tab is at " + nearest_tab);
            String s = jyx.getTextPane().getText();
            boolean exited = false;
            for(int i = nearest_tab; i < offset; i++) {
                if (!Character.isWhitespace(s.charAt(i))) {
                    exited = true;
                    break;
                }
            }
            if (exited) {
                return -1;
            } else {
                return nearest_tab;
            }
        }
        
        static class Analyze {
            int nb_lines;
            int nb_chars;
            
            Analyze() {
                this.nb_lines = 0;
                this.nb_chars = 0;
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
        }
        
    }
    
    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(JyxConfig.QUIT)) {
            System.exit(0);
        } else if (command.equals(JyxConfig.OPEN)) {
            JFileChooser fc = new JFileChooser();
            int retval = fc.showOpenDialog(frame);
            if (retval == JFileChooser.APPROVE_OPTION) {
                File file = fc.getSelectedFile();
                getController().update(Controller.OPEN, file);
            }
        } else if (command.equals(JyxConfig.NEW)) {
            getController().update(Controller.NEW);
        } else if (command.equals(JyxConfig.SAVE)) {
            getController().update(Controller.SAVE);
        } else if (command.equals(JyxConfig.SAVE_AS)) {
            JFileChooser fc = new JFileChooser();
            int retrival = fc.showSaveDialog(frame);
            if (retrival == JFileChooser.APPROVE_OPTION) {
                File file = fc.getSelectedFile();
                saveFile(file, jtp.getText());
                hasChanged = false;
                frame.setTitle(file.getName() + " - Jyx 1.0");
            }
        } else {
            JOptionPane.showMessageDialog(null, e.getActionCommand());
        }
    }
    
    public void caretUpdate(CaretEvent e) {
        transmit(e.getDot(), e.getMark());
    }

    protected void transmit(final int dot, final int mark) {
        SwingUtilities.invokeLater(new Runnable() { // Schedule the code for execution in the event dispatching thread where we can use set text
            public void run() {
                getController().update(Controller.CARRET_MOVE, dot, mark);
                // if (dot == mark) {
                // }
            }
        });
    }
    
    static class JyxConfig {
        // Default buffer file
        static String SAVE_BUFFER = "working_buffer.txt";
        static String BUFFER_SAVED = "[Buffer saved] - Jyx 1.0";
        // Menu
        static String NEW = "Nouveau";
        static int NEW_KEY = KeyEvent.VK_N;
        static String OPEN = "Ouvrir...";
        static int OPEN_KEY = KeyEvent.VK_O;
        static String SAVE = "Enregistrer";
        static int SAVE_KEY = KeyEvent.VK_S;
        static String SAVE_AS = "Enregistrer sous...";
        static String QUIT = "Quitter";
        static int QUIT_KEY = KeyEvent.VK_Q;
        static String COPY = "Copier";
        static int COPY_KEY = KeyEvent.VK_C;
    }
    
    static class JyxDocument extends DefaultStyledDocument {
        
        Jyx panel;
        
        public JyxDocument(Jyx panel) {
            super();
            this.panel = panel;
        }
        
    	@Override
    	public void insertString(int offs, String str, AttributeSet a) {
            try {
                str = str.replaceAll("\t", "    ");
                super.insertString(offs, str, a);
                panel.getController().update(Controller.WRITING);
                System.out.println("Inserted : offset = " + offs + " str = " + str);
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception");
            }
    	}
        
        @Override
        public void remove(int offs, int len) {
            try {
                if (len == 1) {
                    int i = panel.getController().getNearestTab(offs);
                    if (i == -1) {
                        //System.out.println("I will remove only one char, at offset = " + offs);
                    } else {
                        len = offs-i+1;
                        offs = i;
                        //System.out.println("I will remove " + len + " char(s), from offset = " + offs);
                    }
                }
                super.remove(offs, len);
                panel.getController().update(Controller.REMOVING);
                System.out.println("Removed : offset = " + offs + " len = " + len);
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception : " + offs + " and len = " + len);
            }
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
    
    public static void main(String[] args) {
        System.out.println("Hello Java World");
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            System.out.println("Unable to set system look and feel");
        }
        
        JFrame frame = new JFrame(); //"Jyx");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(600, 800));
        frame.setTitle("Jyx 1.0");
        frame.setResizable(true);
        
        Jyx jyx = new Jyx(frame);
        
        JMenuBar menuBar;
        JMenu menu, submenu;
        JMenuItem menuItem;
        
        // A mnemonic is a key that makes an already visible menu item be chosen.
        // An accelerator is a key combination that causes a menu item to be chosen, whether or not it's visible.
        
        menuBar = new JMenuBar();
            menu = new JMenu("Fichier");
            menu.setMnemonic(KeyEvent.VK_F);
            // menu.getAccessibleContext().setAccessibleDescription("The only menu in this program that has menu items");
                menuItem = new JMenuItem(JyxConfig.NEW, JyxConfig.NEW_KEY);
                //menuItem.setMnemonic(KeyEvent.VK_N);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, ActionEvent.CTRL_MASK));
                // menuItem.getAccessibleContext().setAccessibleDescription("This doesn't really do anything");
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
                menuItem = new JMenuItem(JyxConfig.OPEN, JyxConfig.OPEN_KEY);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(JyxConfig.OPEN_KEY, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
                menuItem = new JMenuItem(JyxConfig.SAVE, JyxConfig.SAVE_KEY);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(JyxConfig.SAVE_KEY, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
                menuItem = new JMenuItem(JyxConfig.SAVE_AS, JyxConfig.SAVE_KEY);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, ActionEvent.CTRL_MASK | Event.SHIFT_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
            menu.addSeparator();
                menuItem = new JMenuItem(JyxConfig.QUIT, JyxConfig.QUIT_KEY);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
        menuBar.add(menu);
            menu = new JMenu("Edition");
                menuItem = new JMenuItem("Couper", KeyEvent.VK_X);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_X, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
                menuItem = new JMenuItem(JyxConfig.COPY, JyxConfig.COPY_KEY);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_C, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
                menuItem = new JMenuItem("Coller", KeyEvent.VK_V);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_V, ActionEvent.CTRL_MASK));
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
        menuBar.add(menu);
        frame.add(jyx);
        frame.setJMenuBar(menuBar);
        
        frame.pack();
        frame.setVisible(true);
        
    }
    
}
