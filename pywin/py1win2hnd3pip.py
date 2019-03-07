import time
import win32pipe
import win32file
import pywintypes
import py1win0 as win0






def createPip(_nPip = r'\\.\pipe\Foo', _debugMode = 0):
    if(_debugMode == 1):
        print("createPip")
    pipe = win32pipe.CreateNamedPipe(_nPip,  # name of pipe
            win32pipe.PIPE_ACCESS_DUPLEX,  # openmode
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,  # pipe mode
            1, 65536, 65536,  # nMaxinstances , nOutBufferSize , nInbufferSize
            0,  # nDrfaultTimeOut
            None)  # pysecurity attributes

    return pipe

def closePip(_pip, _debugMode = 0):
    if (_debugMode == 1):
        print("closePip")
    win32file.CloseHandle(_pip)

def connectPip(_hPip, _debugMode = 0):
    if (_debugMode == 1):
        print("connectPip")
    win32pipe.ConnectNamedPipe(_hPip,  # handle
                               None)  # overlapped

def pip_yHdr(_hPip, _yHdr, _debugMode = 0):
    try:

        if(_debugMode == 1):
            print("waiting for client")

        connectPip(_hPip, _debugMode)

        win32file.WriteFile(_hPip, _yHdr)

        time.sleep(1)

        if (_debugMode == 1):
            print("finished now")
    finally:
        closePip(_hPip, _debugMode)

def openPip(_nPip = r'\\.\pipe\Foo', _debugMode = 0):
    if (_debugMode == 1):
            print("openPip")

    handle = win32file.CreateFile(
        _nPip,  # filename
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,  # win32con.GENERIC_READ | win32con.GENERIC_WRITE,
        0,  # win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,  # win32security.SECURITY_ATTRIBUTES(),
        win32file.OPEN_EXISTING,  # win32con.OPEN_EXISTING,
        0,  # win32con.FILE_FLAG_OVERLAPPED,
        None  # 0
    )

    res = win32pipe.SetNamedPipeHandleState(
        handle,  # HANDLE
        win32pipe.PIPE_READMODE_MESSAGE,  # PIPE_READMODE_BYTE OR PIPE_READMODE_MESSAGE
        None,  # PIPE_WAIT OR PIPE_NOWAIT
        None)  # NULL

    if res == 0:
        print(f"SetNamedPipeHandleState return code: {res}")

    return handle

def yHdr_pip(_nPip = r'\\.\pipe\Foo' , _debugMode = 0):
    if (_debugMode == 1):
            print("yHdr_pip")

    handle = openPip(_nPip, _debugMode)
    resp = win32file.ReadFile(handle, 64 * 1024)

    yHdr = resp[1]

    return yHdr

def s_pip(_nPip = r'\\.\pipe\Foo' , _debugMode = 0):
    if (_debugMode == 1):
            print("s_pip")

    return win0.s_yHdr(yHdr_pip(_nPip, _debugMode))

def ws_pip(_nPip = r'\\.\pipe\Foo' , _debugMode = 0):
    if (_debugMode == 1):
        print("ws_pip")

    return win0.ws_yHdr(yHdr_pip(_nPip, _debugMode))

def pip_s(_pip, _string, _debugMode = 0):
    if (_debugMode == 1):
        print("pip_s")

    pip_yHdr(_pip, win0.yHdr_s(_string), _debugMode)

def pip_ws(_pip, _string, _debugMode = 0):
    if (_debugMode == 1):
        print("pip_ws")

    pip_yHdr(_pip, win0.yHdr_ws(_string), _debugMode)


class PipWriter:

    def __init__(self, name_pip = r'\\.\pipe\Foo', _debugMode = 0):
        self.name_pip = name_pip
        self.debugMode = _debugMode

    def pip_s(self,string):
        pip = createPip(self.name_pip,self.debugMode)
        pip_s(pip,string, self.debugMode)

    def pip_ws(self,string):
        pip = createPip(self.name_pip, self.debugMode)
        pip_ws(pip,string, self.debugMode)

class PipReader:

    def __init__(self, _nPip = r'\\.\pipe\Foo', _debugMode = 0):
        self.name_pip = _nPip
        self.debugMode = _debugMode

    def s_pip(self):
        quit = False

        while not quit:
            try:
                return s_pip(self.name_pip,self.debugMode)

            except pywintypes.error as e:

                if e.args[0] == 2 :
                    if self.debugMode == 1:
                        print("no pipe, trying again in a sec")
                    time.sleep(1)

                elif e.args[0] == 109 :
                    if self.debugMode == 1 :
                        print("broken pipe, bye bye")
                    quit = True


    def ws_pip(self):
        if (self.debugMode == 1):
            print("pipe client")
        quit = False

        while not quit:
            try:
                return ws_pip(self.name_pip,self.debugMode)

            except pywintypes.error as e:

                if e.args[0] == 2 :
                    if self.debugMode == 1:
                        print("no pipe, trying again in a sec")
                    time.sleep(1)

                elif e.args[0] == 109 :
                    if self.debugMode == 1 :
                        print("broken pipe, bye bye")
                    quit = True
    def __del__(self):
        closePip(self.handle ,self.debugMode)

