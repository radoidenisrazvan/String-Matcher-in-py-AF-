import PySimpleGUI as sg
from finite_automaton import computeTF, search, build_transition_table

def build_layout():
    layout = [
        [sg.Text("Enter Pattern:")],
        [sg.InputText(key="pattern")],
        [sg.Text("Enter Text T:")],
        [sg.InputText(key="text_to_search")],
        [sg.Button("Search Pattern"), sg.Button("Generate Transition Table"), sg.Button("Exit")],
        [sg.Multiline("", size=(50, 10), key="-OUTPUT-", disabled=True)]
    ]
    return layout

def highlight_pattern(pattern, text):
    highlighted_text = []
    i = 0

    while i < len(text):
        if text[i:i + len(pattern)] == pattern:
            end = i + len(pattern)
            highlighted_text.append(sg.Text(text[i:end], background_color='green', text_color='white'))
            i = end
        else:
            highlighted_text.append(sg.Text(text[i], text_color='black'))
            i += 1

    return highlighted_text



def main():
    window = sg.Window("Automat finit management", build_layout(), resizable=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        if event == "Search Pattern":
            pattern = values["pattern"]
            text_to_search = values["text_to_search"]

            if not pattern or not text_to_search:
                sg.popup_error("Please enter both the pattern and the text to search.")
            else:
                M = len(pattern)
                N = len(text_to_search)
                TF = computeTF(pattern, M)
                state = 0
                result_indices = []

                for i in range(N):
                    state = TF[state][ord(text_to_search[i])]
                    if state == M:
                        result_indices.append(i - M + 1)

                if result_indices:
                    indices_str = f"[{', '.join(map(str, result_indices))}]" ## lista de indici gasiti
                    output_text = f"Pattern found at indices: {indices_str}" ## locurile unde s-a gasit sablonul in text
                    highlighted_output = highlight_pattern(pattern, text_to_search)
                    layout = [
                        [sg.Text(output_text)],
                        highlighted_output
                    ]

                    result_window = sg.Window("Search Result", layout=layout, modal=True)
                    result_window.read(close=True)
                else:
                    output_text = "Pattern not found in the given text."

                window["-OUTPUT-"].update(output_text)

        if event == "Generate Transition Table":
            pattern = values["pattern"]

            if not pattern:
                sg.popup_error("Please enter the pattern.")
            else:
                transitions = build_transition_table(pattern)
                if transitions:
                    output_text = ""
                    for row in transitions:
                        output_text += '|'.join(map(str, row)) + '\n'

                    window["-OUTPUT-"].update(output_text)

    window.close()

if __name__ == "__main__":
    main()


