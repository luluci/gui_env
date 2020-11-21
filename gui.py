import sys
import PySimpleGUI as sg

from PySimpleGUIHelper import PySimpleGUIHelper as sg_helper

print("hi!!")


# https://teratail.com/questions/49758
# https://sites.google.com/site/pythoncasestudy/home/tkinterdedrag-drop-ctypes-shi-yong


sg.theme("Dark Blue 3")


layout = [
	[sg.Text("Test GUI.")],
	[sg.Text("ListBox:")],
	[sg.Listbox(key="list_box",values=["test1", "test2"], size=(50,10), enable_events=True)],
	[sg.Text("TextBox:")],
	[sg.InputText(key="input_text", default_text="hoge")]
]


window = sg.Window("test window.", layout, finalize=True)
#window.Finalize()


def dad_list_box(dn: str):
	print("[list_box] D&D accepted! Get: " + dn)

def dad_text_box(dn: str):
	print("[input_text] D&D accepted! Get: " + dn)



#=== ドラッグアンドドロップイベントを取得させるようにする。===
#ハンドラの取得
#hwnd = window.TKroot.wm_frame()
#hwnd = window.TKroot.winfo_id()
item = window["list_box"]
hwnd = item.Widget.winfo_id()

adapt1 = sg_helper.adapt_dad(window["list_box"], dad_list_box)
adapt2 = sg_helper.adapt_dad(window["input_text"], dad_text_box)

while True:
	event, values = window.read()

	if event is None:
		print("exit")
		break

window.close()


