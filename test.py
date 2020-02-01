import glob
import re
from decimal import Decimal
import os, sys, subprocess
from time import sleep

def root_main():
    print("Ayy, pretty cool, you're root!")
    return 0

def user_main():
    print("That's also cool, you're a user, I don't discriminate.")

if os.getuid() == 0:
    root_main()
else:
    user_main()
