import time
import PySimpleGUI as psg
layout = [
   [psg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='-PBAR-'), psg.Button('Test')],
   [psg.Text('', key='-OUT-', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
]
window = psg.Window('Progress Bar', layout, size=(715, 150))
while True:
   event, values = window.read()
   print(event, values)
   if event == 'Test':
      window['Test'].update(disabled=True)
      for i in range(100):
         window['-PBAR-'].update(current_count=i + 1)
         window['-OUT-'].update(str(i + 1))
         time.sleep(1)
         window['Test'].update(disabled=False)
   if event == 'Cancel':
      window['-PBAR-'].update(max=100)
   if event == psg.WIN_CLOSED or event == 'Exit':
      break