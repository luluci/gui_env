import sys
import ctypes
import PySimpleGUI as sg

import pythoncom

from ctypes import cast
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM

print("hi!!")


# https://teratail.com/questions/49758
# https://sites.google.com/site/pythoncasestudy/home/tkinterdedrag-drop-ctypes-shi-yong


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


DragAcceptFiles = ctypes.windll.shell32.DragAcceptFiles
DragQueryFile = ctypes.windll.shell32.DragQueryFile
DragQueryFile.argtypes = [ ctypes.c_void_p, UINT, ctypes.c_void_p, UINT ]
DragFinish = ctypes.windll.shell32.DragFinish
DragFinish.argtypes = [ ctypes.c_void_p ]
CallWindowProc = ctypes.windll.user32.CallWindowProcW
CallWindowProc.restype = ctypes.c_void_p
CallWindowProc.argtypes = [ ctypes.c_void_p, HWND , UINT, WPARAM, LPARAM ]
try: GetWindowLong = ctypes.windll.user32.GetWindowLongPtrW
except AttributeError: GetWindowLong = ctypes.windll.user32.GetWindowLongW
GetWindowLong.restype = ctypes.c_void_p
try: SetWindowLong = ctypes.windll.user32.SetWindowLongPtrW
except AttributeError: SetWindowLong = ctypes.windll.user32.SetWindowLongW
SetWindowLong.restype = ctypes.c_void_p

prototype = ctypes.WINFUNCTYPE(ctypes.c_void_p, HWND, UINT, WPARAM, LPARAM)
WM_DROPFILES = 0x0233
GWL_WNDPROC = -4
WINPROC = None
dropname = ""

def getaddr(x): return cast(x, ctypes.c_void_p).value

def py_drop_func(hwnd, msg, wp, lp):
    """
    WinProcのプロトタイプ
    ファイルのドラッグアンドドロップイベント(WM_DROPFILES)を検出して、
    ドロップされたファイルを保存する。
    ここでウィンドウ(tk)を使用するとハングアップするのでデータ保存だけ行う。
    """
    if msg == WM_DROPFILES:
        DragQueryFile(wp, -1, None, 0)
        buf = ctypes.c_buffer(260)
        DragQueryFile(wp, 0, buf, ctypes.sizeof(buf))
        dropname = buf.value.decode(sys.getfilesystemencoding())
        #fns = [ buf.value.decode(FS_ENCODING) for nn in range(nf) \
        #    if DragQueryFile(wp, nn , buf, ctypes.sizeof(buf)) ]
        DragFinish(wp)
        print(dropname)

    return CallWindowProc(WINPROC, hwnd, msg, wp, lp)



if __name__ == "__main__":
    dropname = None
    
    #=== ドラッグアンドドロップイベントを取得させるようにする。===
    #ハンドラの取得
    #hwnd = window.TKroot.wm_frame()
    #hwnd = window.TKroot.winfo_id()
    item = window["list_box"]
    hwnd = item.Widget.winfo_id()

    #ウィンドウがドラッグアンドドロップを認識できるようにする。
    DragAcceptFiles(hwnd, True)
    #ウィンドウプロシージャを取得
    WINPROC = GetWindowLong(hwnd, GWL_WNDPROC)
    #ドラッグアンドドロップを処理できるウィンドウプロシージャを作成
    drop_func = prototype(py_drop_func)
    #ウィンドウプロシージャを追加
    SetWindowLong(hwnd, GWL_WNDPROC, drop_func)




while True:
    event, values = window.read()

    if event is None:
        print("exit")
        break


window.close()
