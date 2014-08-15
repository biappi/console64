# adapted from http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/

try:
    import msvcrt

    def getch():
        return msvcrt.getch()

except:
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

