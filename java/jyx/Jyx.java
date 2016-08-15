package jyx;

import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;

import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.BadLocationException;
import javax.swing.text.AttributeSet;
import javax.swing.text.AbstractDocument.DefaultDocumentEvent;
import javax.swing.text.StyleContext;
import javax.swing.text.Style;
import javax.swing.text.StyleConstants;
import javax.swing.text.Document;
import javax.swing.text.Element;

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
        
        // enable anti-aliased text:
        System.setProperty("awt.useSystemAAFontSettings","on");
        System.setProperty("swing.aatext", "true");
  
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
        } else if (command.equals(JyxConfig.ABOUT)) {
            getController().update(Controller.ABOUT);
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
    
    static class JyxDocument extends DefaultStyledDocument {
        
        Jyx panel;
        
        Style base;
        Style bold;
        Style italic;
        
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
            
        }
        
    	@Override
    	public void insertString(int offs, String str, AttributeSet a) {
            try {
                str = str.replaceAll("\t", "    ");
                if (str.charAt(0) == '*' && str.charAt(str.length()-1) == '*') {
                    super.insertString(offs, str, this.getStyle("bold"));
                } else {
                    super.insertString(offs, str, this.getStyle("regular"));
                }
                panel.getController().update(Controller.WRITING);
                System.out.println("Inserted : offset = " + offs + " str = " + str);
                this.parse(offs);
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
        
        public void parse(int offset) {
            Element e = this.getParagraphElement(offset);
            int e_length = this.elementLength(e);
            if (e_length > 1) {
                String s = this.elementText(e);
                if (s.charAt(0) == '-' && s.charAt(1) == '-') {
                    this.setCharacterAttributes(e.getStartOffset(), e_length, this.getStyle("italic"), true);
                    return;
                }
            }
            this.setCharacterAttributes(e.getStartOffset(), e_length, this.getStyle("regular"), true);
        }
        
        public String safeGetText() { // don't translate \n by \r\n on windows :-)
            String text = "";
            try {
                int length = this.getLength();
                text = this.getText(0, length);
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception");
            } finally {
                return text;
            }
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
            try {
                //s = this.getText(offset, len);
                super.remove(offset, len);
                if (offset > 1) {
                    this.parse(offset-1);
                } else {
                    this.parse(0);
                }
            } catch (BadLocationException ble) {
                System.out.println("Bad location exception");
            }
            panel.getController().update(Controller.REMOVING);
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
            menu = new JMenu("?");
                menuItem = new JMenuItem("À propos...");
                menuItem.addActionListener(jyx);
            menu.add(menuItem);
        menuBar.add(Box.createHorizontalGlue());
        menuBar.add(menu);  
        frame.add(jyx);
        frame.setJMenuBar(menuBar);
        
        frame.pack();
        frame.setVisible(true);
        
    }
    
}
