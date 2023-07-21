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

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.
    # !/usr/bin/env python

    """
    Simple Image Browser based on PySimpleGUI
    --------------------------------------------
    There are some improvements compared to the PNG browser of the repository:
    1. Paging is cyclic, i.e. automatically wraps around if file index is outside
    2. Supports all file types that are valid PIL images
    3. Limits the maximum form size to the physical screen
    4. When selecting an image from the listbox, subsequent paging uses its index
    5. Paging performance improved significantly because of using PIL

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

    num_files = len(fnames)  # number of iamges found
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
    col_files = [[sg.Listbox(values=fnames,
                             #select_mode="extended",
                             size=(60, 30),
                             default_values=['APSC'],
                             enable_events=True,
                             key='listbox')],
                 [sg.Button('Exit', size=(8, 1)),  #programm beenden
                  sg.Button('Deselect', size=(8, 1)),  #Auswahl aus json wieder entfernen bzw auf Null setzen
                  sg.Button('Prev', size=(8, 1)), #Ein Bild --
                  sg.Button('Next', size=(8, 1)), #Ein Bild ++
                  sg.Button('Select', size=(8, 2), change_submits=True),
                  ## sg.Button('Set RAW-Folder', size=(9, 3)), ## next step
                  # sg.Button('xCopy', size=(8, 2)), ## next Step - hier wird der aktiv wenn man den RAW Folder ausgewaehlt hat.
                  file_num_display_elem],
                  [sg.Text('', key='-OUT-', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True),
                  sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20), key='-PBAR-')]]

    layout = [[sg.Column(col_files), sg.Column(col)]]

    window = sg.Window('Image Browser', layout, return_keyboard_events=True,
                       location=(0, 0), use_default_focus=True)
    lb = window['listbox']
   ##  sg.Button("xCopy", disabled=True)  "NEXT STEP"
    # loop reading the user input and displaying image, filename
    i = 0
    imgMapPath = ""
    while True:
        # read the form
        event, values = window.read()
        print(event, values)
        # perform button and keyboard operations
        if event == sg.WIN_CLOSED:
            break
       ## elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
        elif event in ('Next', 'MouseWheel:Down' ):
            i += 1
            filename = os.path.join(folder, fnames[i])

            f = fnames[i]  # selected filename
            k = fnames.index(f)  # update running index
            lb.update(scroll_to_index=k,set_to_index=k)
            #print("sf", i, fnames[i], k)

            if i >= num_files:
                print("------")
                i -= num_files


       ## elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
        elif event in ('Prev', 'MouseWheel:Up'):
            i -= 1
            #print("delegate")
            f = fnames[i]  # selected filename
            k = fnames.index(f)  # update running index
            lb.update(scroll_to_index=k,set_to_index=k)
            #print("sf", i, fnames[i], k)
            if i < 0:
                print("+++++")
                i = num_files + i

        elif event in ('p:80'):
         #   print("delegate")
        #    print(fnames[i])
            window['Select'].click()
            filename = os.path.join(folder, fnames[i])

        elif event in ('Select'):
            i = i
            filename = os.path.join(folder, fnames[i])
            filename_ = fnames[i]
            # print(filename)
            status = "yay"
            namez_ = filename_
            noS = [filename, status, namez_]
            # Add here the selected file to the JSON Data file
            Select_writeJson.write_json(noS)
            # Create a new Directory to copy the mapped and selected files from JSON
            Write_MkDir.makeDir()
        elif event in ('xCopy'):
          ###  window2['Write'].update(disabled=True)
            window2 = window
            event, values = window2.read()
            print(event, values)
            if imgMapPath != "":

                with open('data.json') as json_file:
                 data = json.load(json_file)
                 for ij in data['photoSelection']:
                       if (ij['statusSelected'] == "yay"):
                            print(ij['file'])
                            print(ij['namez_'])
                            print(imgMapPath)
                            print(window2)
                            Copy_Map_Files.copyMapjpgRAW( ij['namez_'],imgMapPath,window2)
                            iteration(ij)
        elif event in ( "Set RAW-Folder"):
            # Get the folder containin:g the images from the user
            imgMapPath = sg.popup_get_folder('Image folder to open', default_path='')
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
