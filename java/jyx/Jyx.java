package jyx;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Jyx extends JPanel implements ActionListener {
    
    JTextPane jtp;
    
    public Jyx() {
        setLayout(new BorderLayout());
        
        jtp = new JTextPane();
        jtp.setPreferredSize(new Dimension(400, 600));
        //jtp.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
        add(jtp, BorderLayout.CENTER);
        
        JScrollPane scrollPane = new JScrollPane(jtp);
        add(scrollPane, BorderLayout.LINE_END);
    }
    
    public void actionPerformed(ActionEvent e) {
    }
    
    public static void main(String[] args) {
        System.out.println("Hello Java World");
        
        JFrame frame = new JFrame("Jyx");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        JMenuBar menuBar;
        JMenu menu, submenu;
        JMenuItem menuItem;
        
        menuBar = new JMenuBar();
            menu = new JMenu("Menu 1");
            menu.setMnemonic(KeyEvent.VK_A);
            menu.getAccessibleContext().setAccessibleDescription("The only menu in this program that has menu items");
                menuItem = new JMenuItem("A text-only menu item", KeyEvent.VK_T);
                menuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_T, ActionEvent.ALT_MASK));
                menuItem.getAccessibleContext().setAccessibleDescription("This doesn't really do anything");
            menu.add(menuItem);
            menu.addSeparator();
        menuBar.add(menu);
        
        frame.add(new Jyx());
        frame.setJMenuBar(menuBar);
        
        frame.pack();
        frame.setVisible(true);
        
    }
    
}
