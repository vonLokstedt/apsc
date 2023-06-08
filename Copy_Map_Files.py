import PySimpleGUI as sg
import time

import json
from functools import reduce
from operator import getitem
import shutil
import os
import time



def ProgressTrigger(window2):
    for i in range(100):
        window2['-PBAR-'].update(current_count=i + 1)
        window2['-OUT-'].update(str(i + 1))
        time.sleep(.1)
        window2['Write'].update(disabled=False)


def copyMapjpgRAW(JPGname,_imgMapPath,window2):
    pureName = JPGname
    _pureName = pureName[:-4]
    __pureName = _pureName+(".NEF")

    shutil.copy2(os.path.join(_imgMapPath, __pureName), ('./selection'))
