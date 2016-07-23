package jyx;

import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;

import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.AttributeSet;
import javax.swing.text.AbstractDocument.DefaultDocumentEvent;

import java.io.File;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.FileWriter;

import java.nio.charset.Charset;

//import com.sun.java.swing.plaf.gtk.GTKLookAndFeel;
//import com.sun.java.swing.plaf.motif.MotifLookAndFeel;
//import com.sun.java.swing.plaf.windows.WindowsLookAndFeel;

public class Jyx extends JPanel implements ActionListener {
    
    JTextPane jtp;
    JFrame frame;
    File currentFile;
    boolean launch;
    boolean hasChanged;
    Controller master;
    
    public Jyx(JFrame frame) {
        this.frame = frame;
        this.master = new Controller(this);
        this.hasChanged = false;
        this.launch = true;
        
        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        Border border = BorderFactory.createEtchedBorder();
        setBorder(BorderFactory.createTitledBorder(border, "Texte"));
        
        jtp = new JTextPane();
        jtp.setDocument(new JyxDocument(this));
        //jtp.setPreferredSize(new Dimension(400, 600));
        //jtp.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        gbc.gridx = gbc.gridy = 0;
        gbc.gridwidth = gbc.gridheight = 1;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.anchor = GridBagConstraints.NORTHWEST;
        gbc.weightx = 95;
        gbc.weighty = 100;
        add(jtp, gbc);
        
        JScrollPane scrollPane = new JScrollPane(jtp);
        gbc.gridx =1;
        gbc.gridy = 0;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        gbc.weightx = 5;
        add(scrollPane, gbc);
        
        try {
            File file = new File(JyxConfig.SAVE_BUFFER);
            if (file.exists() && !file.isDirectory()) {
                jtp.setText(readFile(file));
                frame.setTitle(JyxConfig.BUFFER_SAVED);
            }
        } catch (Exception e) {
            System.err.format("IOException: %s%n", e);
        }
        
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
    
    boolean askAndLockLaunch() {
        if (this.launch) {
            this.launch = false;
            return true;
        } else {
            return false;
        }
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
            FileWriter fw = new FileWriter(file);
            fw.write(content);
            fw.close();
        } catch (IOException ioe) {
            System.err.format("IOException: %s%n", ioe);
        }
    }
    
    static class Controller {
        
        static int NEW = 1;
        static int OPEN = 2;
        static int SAVE = 3;
        static int SAVE_AS = 4;
        static int QUIT = 5;
        
        Jyx jyx;
        
        Controller (Jyx jyx) {
            this.jyx = jyx;
        }
        
        void update(int event, File file) {
            if (event == Controller.OPEN) {
                jyx.getTextPane().setText(jyx.readFile(file));
                jyx.getFrame().setTitle(file.getName() + " - Jyx 1.0"); 
                jyx.setCurrentFile(file);
                jyx.resetChanged();
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
                    new_title = JyxConfig.BUFFER_SAVED;
                } else {
                    file = jyx.getCurrentFile();
                    new_title = file.getName() + " - Jyx 1.0"; 
                }
                jyx.saveFile(file, jyx.getTextPane().getText());
                jyx.resetChanged();
                jyx.getFrame().setTitle(new_title);
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
                if (!panel.getHasChanged()) {
                    String old_title = panel.getFrame().getTitle();
                    String new_title = "(Changed) " + old_title;
                    panel.getFrame().setTitle(new_title);
                    if (panel.askAndLockLaunch()) {
                        // Do nothing. it's the first insert in this case, when we open the document
                    } else {
                        panel.setChanged();
                    }
                }
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception");
            }
    	}
        
        @Override
        public void removeUpdate(DefaultDocumentEvent chng) {
            super.removeUpdate(chng);
            if (!panel.getHasChanged()) {
                String old_title = panel.getFrame().getTitle();
                String new_title = "(Changed) " + old_title;
                panel.getFrame().setTitle(new_title);
                panel.setChanged();
            }
        }
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
