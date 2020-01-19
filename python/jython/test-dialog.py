#------------------------------------------------------------------------------
# Test Jython with Swing
# Date : lundi 25 novembre 2019
# Always execture the jar of jython with java.exe, not javaw.exe
#------------------------------------------------------------------------------

print "Start of Script"

from javax.swing import JOptionPane

JOptionPane.showMessageDialog(None, "Message", "Titre", JOptionPane.INFORMATION_MESSAGE)
print "bonjour"

ret = JOptionPane.showConfirmDialog(None, "Message", "Titre", JOptionPane.OK_CANCEL_OPTION)
if ret == JOptionPane.OK_OPTION:
    print "ok"
elif ret == JOptionPane.CANCEL_OPTION:
    print "cancel"
elif ret == JOptionPane.CLOSED_OPTION:
    print "closed"

d = JOptionPane()
opt = ['Alpha', 'Beta', 'Delta', 'Gamma']
ret = d.showOptionDialog(None, "Message", "Titre", JOptionPane.DEFAULT_OPTION, JOptionPane.QUESTION_MESSAGE, None, opt, opt[0])
# Waiting for answer

if ret == JOptionPane.CLOSED_OPTION:
    print "closed custom"
else:
    print opt[ret]

# https://imss-www.upmf-grenoble.fr/prevert/Prog/Java/swing/JOptionPane.html
# https://docs.oracle.com/javase/7/docs/api/javax/swing/JOptionPane.html
