import time
import win32pipe
import win32file
import pywintypes
import py1win0

class PipWriter:
    def __init__(self, name_pip = r'\\.\pipe\Foo'):
     self.name_pip = name_pip

    def pip_s(string):

        pipe = win32pipe.CreateNamedPipe(self.name_pip,  # name of pipe
            win32pipe.PIPE_ACCESS_DUPLEX,  # openmode
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,  # pipe mode
            1, 65536, 65536,  # nMaxinstances , nOutBufferSize , nInbufferSize
            0,  # nDrfaultTimeOut
            None)  # pysecurity attributes

        try:
            print("waiting for client")
            win32pipe.ConnectNamedPipe(pipe,  # handle
                                       None)  # overlapped
            print("got client")
            # convert to bytes
            data = header.yHdr_s(string)
            print(f"data to send : {data}")

            win32file.WriteFile(pipe, data)

            # win32file.WriteFile(pipe, b'hello pipe...!')

            time.sleep(1)

            print("finished now")

        finally:
            win32file.CloseHandle(pipe)

    def pip_ws(string):

        pipe = win32pipe.CreateNamedPipe(
            self.name_pip,  # name of pipe
            win32pipe.PIPE_ACCESS_DUPLEX,  # openmode
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,  # pipe mode
            1, 65536, 65536,  # nMaxinstances , nOutBufferSize , nInbufferSize
            0,  # nDrfaultTimeOut
            None)  # pysecurity attributes

        try:

            print("waiting for client")
            win32pipe.ConnectNamedPipe(pipe,  # handle
                                       None)  # overlapped
            print("got client")

            # print(f"writing message {count}")
            # convert to bytes

            data = header.yHdr_ws(string)

            # print(f"data to send : {data}")

            win32file.WriteFile(pipe, data)
            # win32file.WriteFile(pipe, b'hello pipe...!')
            time.sleep(1)

            print("finished now")

        finally:
            win32file.CloseHandle(pipe)

class PipReader:

    def __init__(self, name_pip = r'\\.\pipe\Foo'):
        self.name_pip = name_pip

    def s_pip(self):
        quit = False

        while not quit:
            try:
                handle = win32file.CreateFile(
                    self.name_pip, # filename
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE, # win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                    0, #win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                    None, # win32security.SECURITY_ATTRIBUTES(),
                    win32file.OPEN_EXISTING, #win32con.OPEN_EXISTING,
                    0, # win32con.FILE_FLAG_OVERLAPPED,
                    None # 0
                )

                res = win32pipe.SetNamedPipeHandleState(
                        handle, #HANDLE
                        win32pipe.PIPE_READMODE_MESSAGE, #PIPE_READMODE_BYTE OR PIPE_READMODE_MESSAGE
                        None,  # PIPE_WAIT OR PIPE_NOWAIT
                        None)  #NULL

                if res == 0:
                    print(f"SetNamedPipeHandleState return code: {res}")

                resp = win32file.ReadFile(handle, 64*1024)


                rawData = header.s_yHdr(resp[1])

                return rawData

            except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe, bye bye")
                    quit = True


    def ws_pip(self):
        print("pipe client")
        quit = False

        while not quit:
            try:
                handle = win32file.CreateFile(
                    self.name_pip,  # filename
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

                resp = win32file.ReadFile(handle, 64 * 1024)

                rawData = header.ws_yHdr(resp[1])

                return rawData

            except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe, bye bye")
                    quit = True


