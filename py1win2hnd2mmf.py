import py1win0 as win0
from ctypes import *
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCWSTR, LPCVOID, LPVOID

''' C타입  함수 포인터들의 선언 '''
FILE_MAP_ALL_ACCESS = 0x000F001F  # 플래그의 상수값
INVALID_HANDLE_VALUE = -1  # 시스템 페이지를 사용하기위한 파일디스크립터(INVALID_FILE_HANDLER)
SHMEMSIZE = 0x100  # 공유메모리 크기
PAGE_READWRITE = 0x04  # 플래그의 상수값

FILE_MAP_READ = 0x0004  # 플래그의 상수값

kernel32_dll = windll.kernel32
msvcrt_dll = cdll.msvcrt

create_file_mapping_func = kernel32_dll.CreateFileMappingW
create_file_mapping_func.argtypes = (HANDLE, LPVOID, DWORD, DWORD, DWORD, LPCWSTR)
create_file_mapping_func.restype = HANDLE

open_file_mapping_func = kernel32_dll.OpenFileMappingW
open_file_mapping_func.argtypes = (DWORD, BOOL, LPCWSTR)
open_file_mapping_func.restype = HANDLE

map_view_of_file_func = kernel32_dll.MapViewOfFile
map_view_of_file_func.argtypes = (HANDLE, DWORD, DWORD, DWORD, c_ulonglong)
map_view_of_file_func.restype = LPVOID

memcpy_func = msvcrt_dll.memcpy
memcpy_func.argtypes = (c_void_p, c_void_p, c_size_t)
memcpy_func.restype = LPVOID

unmap_view_of_file_func = kernel32_dll.UnmapViewOfFile
unmap_view_of_file_func.argtypes = (LPCVOID,)
unmap_view_of_file_func.restype = BOOL

memcpy_func = msvcrt_dll.memcpy
memcpy_func.argtypes = (c_void_p, c_void_p, c_size_t)
memcpy_func.restype = LPVOID

close_handle_func = kernel32_dll.CloseHandle
close_handle_func.argtypes = (HANDLE,)
close_handle_func.restype = BOOL

get_last_error_func = kernel32_dll.GetLastError
getch_func = msvcrt_dll._getch
''' C타입  함수 포인터들의 선언 '''



def createMmf(_nMmf = "mmftest_pchr", _size = SHMEMSIZE ,_debugMode = 0):
    file_mapping_name_ptr = c_wchar_p(_nMmf)
    mapping_handle_ = create_file_mapping_func(INVALID_HANDLE_VALUE, 0, PAGE_READWRITE, 0,
                                              _size, file_mapping_name_ptr)

    if(_debugMode == 1):
        print("Mapping object handle: 0x{:016X}".format(mapping_handle_))

    if not mapping_handle_:
        print("Could not open file mapping object: {:d}".format(get_last_error_func()))
        return 1

        raise WinError()

    return mapping_handle_


def mmf_yHdr(_hMmf, _yHdr , _debugMode = 0):

    data = _yHdr
    msg_ptr = c_char_p(data)

    if (_debugMode == 1):
        print(f"len : {len(data)}")

    mapped_view_ptr = map_view_of_file_func(_hMmf, FILE_MAP_ALL_ACCESS, 0, 0, SHMEMSIZE)

    if (_debugMode == 1):
        print("Mapped view addr: 0x{:016X}".format(mapped_view_ptr))

    if not mapped_view_ptr:
        print("Could not map view of file: {:d}".format(get_last_error_func()))
        close_handle_func(_hMmf)
        return 1
        raise WinError()

    if (_debugMode == 1):
        print("Message length: {:d} chars ({:d} bytes)".format(len(data), len(data)))

    memcpy_func(mapped_view_ptr, msg_ptr, len(data))

def mmf_s(_hMmf, _s , _debugMode = 0):
    if(_debugMode == 1):
        print("mmf_s")
    mmf_yHdr(_hMmf,win0.yHdr_s(_s))



def openMmf(_nMmf, _debugMode = 0 ):

    if(_debugMode == 1):
        print("openMmf")

    file_mapping_name_ptr = c_wchar_p(_nMmf)
    read_handle = open_file_mapping_func(FILE_MAP_READ, 0, file_mapping_name_ptr)

    if not read_handle:
        print("Could not open file mapping object: {:d}".format(get_last_error_func()))
        return 1
        raise WinError()

    return read_handle

def yHdr_mmf(_hMmf , _debugMode = 0 ):
    if(_debugMode == 1):
        print("yHdr_mmf")

    readMapped_view_ptr = map_view_of_file_func(_hMmf, FILE_MAP_READ, 0, 0,
                                                          SHMEMSIZE)

    if not readMapped_view_ptr:
        print("Could not map view of file: {:d}".format(get_last_error_func()))
        close_handle_func(_hMmf)
        return 1
        raise WinError()

    DATA = c_char_p(readMapped_view_ptr)
    DATA = string_at(DATA, size=255)  # 포인터에서 널문자를 무시하고 일정 크기를 바이트배열로 반환

    yHdr_ = DATA

    return yHdr_


def closeMmf(_hMmf, _debugMode = 0):
    if (_debugMode == 1):
        print("closeMmf")
    close_handle_func(_hMmf)



def yHdr_mmf(_hMmf, _debugMode = 0):
    if (_debugMode == 1):
        print("yHdr_mmf")


    readMapped_view_ptr = map_view_of_file_func(_hMmf, FILE_MAP_READ, 0, 0,
                                                          SHMEMSIZE)

    if not readMapped_view_ptr:
        print("Could not map view of file: {:d}".format(get_last_error_func()))
        close_handle_func(_hMmf)
        return 1
        raise WinError()

    DATA = c_char_p(readMapped_view_ptr)
    DATA = string_at(DATA, size=255)  # 포인터에서 널문자를 무시하고 일정 크기를 바이트배열로 반환

    yHdr = DATA
    return yHdr

def s_mmf(_hMmf, _debugMode = 0):
    if (_debugMode == 1):
        print("yHdr_mmf")

    return win0.s_yHdr(yHdr_mmf(_hMmf))






class MmfWriter:

    def __init__(self, _nMmf="mmftest_pchr", _size=SHMEMSIZE, _debugMode = 0):
        self.nMmf = _nMmf
        self.debugMod = _debugMode
        self.size = _size
        self.handle = createMmf(self.nMmf,self.size, self.debugMod)

    def mmf_s(self, _string):
        mmf_s(self.handle, _string, self.debugMod)

    def mmf_yHdr(self, _yHdr):
        mmf_yHdr(self.handle,_yHdr, self.debugMod)

    def __del__(self):
        closeMmf(self.handle, self.debugMod)



class MmfReader:

    def __init__(self, _nMmf = "mmftest_pchr", _size = SHMEMSIZE, _debugMode = 0):
        self.nMmf = _nMmf
        self.debugMod = _debugMode
        self.size = _size
        self.handle = openMmf(self.nMmf,self.debugMod)

    def s_mmf(self):
        return s_mmf(openMmf(self.nMmf, self.debugMod))

    def yHdr_mmf(self):
        return yHdr_mmf(openMmf(self.nMmf, self.debugMod))

    def __del__(self):
        closeMmf(self.handle, self.debugMod)