import PySimpleGUI as sg

sg.theme("Dark Blue 3")
layout = [
    [sg.Text("Test GUI.")],
    [sg.Text("ListBox:")],
    [sg.Listbox(key="list_box",values=["test1", "test2"], size=(50,10), enable_events=True)],
    [sg.Text("TextBox:")],
    [sg.InputText("hoge")]
]
window = sg.Window("test window.", layout, finalize=True)
#window.Finalize()


tk = window.TKroot
hwnd = tk.winfo_id()
tk.winfo_class
tk.winfo_name
tk.winfo_visual
item = window["list_box"]
item_id = item.Widget.winfo_id()
print(item_id)

print(hwnd)
print( tk.winfo_class(), ":", tk.winfo_name(), ":", tk.winfo_visual(), ":", tk.winfo_visualid() )

child = tk.winfo_children()
tk.selection_handle

for item in child:
    id = item.winfo_id()
    print( id, ":", item.winfo_class(), ":", item.winfo_name(), ":", item.winfo_visual(), ":", item.winfo_visualid() )

