# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import PySimpleGUI as sg
import time
import PySimpleGUI as psg

import os
from PIL import Image, ImageTk
import io
import Select_writeJson
import json
import Write_MkDir
import Copy_Map_Files


def iteration(numbr):
    global cnet
    cnet = numbr
    print(cnet)


isSet = False


def setGlobalsInit(B):
    global isSet
    if (B == 'F'):
        isSet = False
    elif (B == 'T'):
        isSet = True


setGlobalsInit('F')


def checkStatusBeforeSetIt(filename, status, noS):
    print("checkStatusBeforeSetIt Entry Start", filename)
    with open('data.json', "r") as json_file:
        # json_file = open("data.json", "r")
        data = json.load(json_file)
        json_file.close()
        tmp = data['photoSelection']
        # print(tmp)
        for ij in tmp:
            print(ij)
            if (ij['namez_'] == filename):
                print("found")
                setGlobalsInit('F')
                ij['statusSelected'] = status
                json_file = open("data.json", "w+")
                json_file.write(json.dumps(data))
                json_file.close()
                return True




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Alive, {name}')  # Press Strg+F8 to toggle the breakpoint.
    sg.theme('DarkTanBlue')
    """
    APSC Advanced Photo Selector C.
    --------------------------------------------
    M1 Mode Prepare:
    1 Umwandeln der NEF Raw in JPG in 1000px max. Kantenlaenge
    2 Einfache Bildbearbeitung AutoBright/Kontrast 
    
    M2 Mode Select:
    3 Die aus M1 hergestellten JPG laden und Anzeigen
    4 Auswaehlen "P" ( Mausrad Anwaehlen +/- ) oder wieder abwaehlen "U" und so zu einer JSON data.json adden
    5 Die Angewaehlten Bilder bekommen einen gelben Rahmen und der Rahmen erscheint wenn man das Bild ansieht bzw wenn man es Ausgewaehlt hat. Beim Abwaehlen wird der Rahmen schwarz.
    
    M3 Mode Copy:
    6 Die ausgewaelten JPG haben den gleichen dateinamen wie die NEF ( MUST HAVE )
    7 Die Dateinamen der ausgewaehlten JPGs welche in der JSON Datei den Status: YAY haben werden auf den Ordner der NEF gemappt.
    8 Die gemappten NEF Datein werden so in einen neuen Unter-Ordner des NEF Ordners kopiert.
    

    Dependecies
    ------------
    Python3
    PIL
    """

    # Get the folder containin:g the images from the user
    folder = sg.popup_get_folder('Image folder to open', default_path='')
    if not folder:
        sg.popup_cancel('Cancelling')
        raise SystemExit()

    # PIL supported image types
    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

    # get list of files in folder
    flist0 = os.listdir(folder)

    # create sub list of image files (no sub folders, no wrong file types)
    fnames = [f for f in flist0 if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith(img_types)]

    num_files = len(fnames)  # number of img found
    if num_files == 0:
        sg.popup('No files in folder')
        raise SystemExit()

    del flist0  # no longer needed

    # ------------------------------------------------------------------------------
    # use PIL to read data of one image
    # ------------------------------------------------------------------------------

    def get_img_data(f, maxsize=(1200, 850), first=False):
        """Generate image data using PIL
        """
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:  # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

    # ------------------------------------------------------------------------------

    # make these 2 elements outside the layout as we want to "update" them later
    # initialize to the first file in the list
    filename = os.path.join(folder, fnames[0])  # name of first file in list
    image_elem = sg.Image(data=get_img_data(filename, first=True))
    filename_display_elem = sg.Text(filename, size=(80, 3))
    file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

    # define layout, show and read the form
    col = [[filename_display_elem],
           [image_elem]]
    layout_PB = [
        [psg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20), key='-PBAR-'), psg.Button('Test')],
        [psg.Text('', key='-OUT-', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
    ]

    # window = psg.Window('Progress Bar', layout_PB, size=(715, 150))
    col_files = [[sg.Button('[X]', size=(8, 1)),],[sg.Listbox(values=fnames,
                             # select_mode="extended",
                             size=(60, 30),
                             default_values=['APSC'],
                             enable_events=True,
                             key='listbox')],
                 [  # programm beenden
                  sg.Button('Deselect', size=(8, 1)),  # Auswahl aus json wieder entfernen bzw auf Null setzen
                  sg.Button('Prev', size=(8, 1)),  # Ein Bild --
                  sg.Button('Next', size=(8, 1)),  # Ein Bild ++
                  sg.Button('Select', size=(8, 1), change_submits=True),

                  file_num_display_elem],
                 [sg.Button('Set RAW-Folder', size=(9, 3)), ## next step
                  sg.Button('Copy NEF', size=(10, 3))], ## next Step - hier wird der aktiv wenn man den RAW Folder ausgewaehlt hat.],
                 [sg.Text('', key='-OUT-', enable_events=True, font=('Arial Bold', 16), justification='center',
                          expand_x=True),
                  sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20), key='-PBAR-')]]

    layout = [[sg.Column(col_files), sg.Column(col)]]

    window = sg.Window('Image Browser', layout, return_keyboard_events=True,
                       location=(0, 0), use_default_focus=True)
    lb = window['listbox']
    ##  sg.Button("xCopy", disabled=True)  "NEXT STEP"
    # loop reading the user input and displaying image, filename
    i = 0
    imgMapPath = ""

    def initJSON():
        initDictionary = [
            "initpath",
            "status",
             "initfilename"
        ]
        Select_writeJson.write_json(initDictionary)
    initJSON()

    while True:
        # read the form
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event in ('Next', 'MouseWheel:Down'):
            i += 1
            filename = os.path.join(folder, fnames[i])
            f = fnames[i]  # selected filename
            k = fnames.index(f)  # update running index
            lb.update(scroll_to_index=k, set_to_index=k)
            if i >= num_files:
                i -= num_files
        elif event in ('Prev', 'MouseWheel:Up'):
            i -= 1
            f = fnames[i]  # selected filename
            k = fnames.index(f)  # update running index
            lb.update(scroll_to_index=k, set_to_index=k)
            if i < 0:
                i = num_files + i
        elif event in ('p:80'):
            window['Select'].click()
            filename = os.path.join(folder, fnames[i])
        elif event in ('u:80'):
            window['Deselect'].click()
            filename = os.path.join(folder, fnames[i])
        elif event in ('Deselect'):
            i = i
            filename = os.path.join(folder, fnames[i])
            filename_ = fnames[i]
            # print(filename)
            status = "nay"
            namez_ = filename_
            noS = [filename, status, namez_]

            if (checkStatusBeforeSetIt(filename_, status, noS)):
                print("UPDATED NAY")
            else:
                Select_writeJson.write_json(noS)


            Write_MkDir.makeDir()
        elif event in ('Select'):
            i = i
            filename = os.path.join(folder, fnames[i])
            filename_ = fnames[i]
            # print(filename)
            status = "yay"
            namez_ = filename_
            noS = [filename, status, namez_]
             #checkStatusBeforeSetIt(filename_, status, noS)
            print(" YAY ")
            if (checkStatusBeforeSetIt(filename_, status, noS)):
                print("UPDATED")
            else:
                Select_writeJson.write_json(noS)
                print(" --NEW ENTRY Y A Y -- ")

            Write_MkDir.makeDir()
        elif event in ('xCopy'):
            ###  window2['Write'].update(disabled=True)
            window2 = window
            event, values = window2.read()
            # print(event, values)
            if imgMapPath != "":
                with open('data.json') as json_file:
                    data = json.load(json_file)
                    for ij in data['photoSelection']:
                        if (ij['statusSelected'] == "yay"):
                            Copy_Map_Files.copyMapjpgRAW(ij['namez_'], imgMapPath, window2)
                            iteration(ij)
        elif event in ("Set RAW-Folder"):
            # Get the folder containin:g the images from the user
            imgMapPath = sg.popup_get_folder('Image folder to open', default_path='')
            #imgMapPath = imgMapPath.replace('/', '\\')
            imgMapPath = imgMapPath.replace('\\','/')
        #    if(imgMapPath != ""):
        #      sg.Button("xCopy",disabled=False)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'listbox':  # something from the listbox
            f = values["listbox"][0]  # selected filename
            filename = os.path.join(folder, f)  # read this file
            i = fnames.index(f)  # update running index
        else:
            filename = os.path.join(folder, fnames[i])

        # update window with new image
        image_elem.update(data=get_img_data(filename, first=True))
        # update window with filename
        filename_display_elem.update(filename)
        # update page display
        file_num_display_elem.update('File {} of {}'.format(i + 1, num_files))

    window.close()


if __name__ == '__main__':
    print_hi('APSC')
