import PySimpleGUI as sg
import subprocess
import re


_VARS = {'Networks': [],
         'NetworkStrength': []}

LEDGE_OFFSET = 100  # Offset for the Ledge
TEXT_OFFSET = 300  # Offset for Network Name
GRAPH_SIZE = DATA_SIZE = (600, 600)
GLOBAL_FONT = ('Helvetica', 14)


# SCANNER DATA :

def getNetworks():
    process = subprocess.run(["airport", "en0", "--scan"],
                             check=True,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    processRows = process.stdout.split("\n")
    # clear global network Lists
    _VARS['Networks'].clear()
    _VARS['NetworkStrength'].clear()

    # Parse by 2 or more spaces and build dicts:
    for item in processRows:
        splitData = re.split(r'\s{2,}', item)
        if len(splitData) > 1:
            _VARS['Networks'].append(splitData[1])
            _VARS['NetworkStrength'].append(splitData[2])
    # Remove first item, which is the header
    _VARS['Networks'].pop(0)
    _VARS['NetworkStrength'].pop(0)


# GUI
sg.theme('DarkAmber')

layout = [[sg.Text('Strength', font=GLOBAL_FONT),
           sg.Text('RSSI', font=GLOBAL_FONT, pad=((60, 0), (0, 0))),
           sg.Text('Network', font=GLOBAL_FONT, pad=((100, 0), (0, 0)))],
          [sg.Graph(GRAPH_SIZE, (0, 0), DATA_SIZE, k='-GRAPH-')],
          [sg.Button('SCAN FOR WIFI NETWORKS', font=GLOBAL_FONT),
           sg.Exit(font=GLOBAL_FONT)]]

window = sg.Window('WIFI SCANNER', layout, finalize=True)
graph = window['-GRAPH-']       # type: sg.Graph

# GUI

while True:
    graph.erase()
    getNetworks()
    print('Getting Networks')

    numNetworks = len(_VARS['Networks'])
    bar_height = (GRAPH_SIZE[0]/numNetworks)
    bar_spacing = (GRAPH_SIZE[0]/numNetworks)
    for i in range(numNetworks):
        # Negative value for graph
        graph_value = -int(_VARS['NetworkStrength'][i])
        rssi_value = _VARS['NetworkStrength'][i]
        networkName = _VARS['Networks'][i]

        graph.draw_rectangle(top_left=(0 - LEDGE_OFFSET,
                                       GRAPH_SIZE[1] - i * bar_height),
                             bottom_right=(graph_value,
                                           GRAPH_SIZE[1] -
                                           (i * bar_height) - bar_height),
                             fill_color='lightgreen')
        # draw network name
        graph.draw_text(text=networkName, location=(
            TEXT_OFFSET, i * bar_height + bar_height/2),
            font=GLOBAL_FONT, color='white')

        # draw rssi value
        graph.draw_text(text=rssi_value, location=(
            140, i * bar_height + bar_height/2),
            font=GLOBAL_FONT, color='lightgreen')

    # Normally at the top of the loop,
    # but because we're drawing the graph first, making it at the bottom
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break


window.close()