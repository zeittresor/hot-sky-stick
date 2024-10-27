import pygame
import psutil
import time
import ctypes
import sys
import win32gui
import win32process
import win32con
#hotSwap Joystick support for skyrim as a mod by triplex2011 (zeittresor)
# Define necessary structures and functions for SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ('wVk', ctypes.c_ushort),
        ('wScan', ctypes.c_ushort),
        ('dwFlags', ctypes.c_ulong),
        ('time', ctypes.c_ulong),
        ('dwExtraInfo', PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ('uMsg', ctypes.c_ulong),
        ('wParamL', ctypes.c_short),
        ('wParamH', ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.c_long),
        ('dy', ctypes.c_long),
        ('mouseData', ctypes.c_ulong),
        ('dwFlags', ctypes.c_ulong),
        ('time',ctypes.c_ulong),
        ('dwExtraInfo', PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ('ki', KeyBdInput),
        ('mi', MouseInput),
        ('hi', HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_ulong),
        ('ii', Input_I)
    ]

# Define SendInput function
SendInput = ctypes.windll.user32.SendInput

# Map key names to scancodes
SCANCODE = {
    'W': 0x11,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'SPACE': 0x39,
    'I': 0x17
}

# Function to simulate key press
def press_key(scancode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(
        wVk=0,
        wScan=scancode,
        dwFlags=0x0008,  # KEYEVENTF_SCANCODE
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to simulate key release
def release_key(scancode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(
        wVk=0,
        wScan=scancode,
        dwFlags=0x0008 | 0x0002,  # KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to simulate mouse click
def click_mouse(button, down):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    flags = {
        ('left', True): 0x0002,    # MOUSEEVENTF_LEFTDOWN
        ('left', False): 0x0004,   # MOUSEEVENTF_LEFTUP
        ('right', True): 0x0008,   # MOUSEEVENTF_RIGHTDOWN
        ('right', False): 0x0010   # MOUSEEVENTF_RIGHTUP
    }
    ii_.mi = MouseInput(
        dx=0,
        dy=0,
        mouseData=0,
        dwFlags=flags[(button, down)],
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to check if a process is running
def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

# Function to list all running processes
def list_processes():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_list.append((proc.info['pid'], proc.info['name']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list

# Function to get window handles (HWNDs) for a process
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

# Initialize pygame and the joystick
pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick connected.")
    sys.exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick '{joystick.get_name()}' initialized.")

# Check if SkyrimSE.exe is running
process_name = "SkyrimSE.exe"

pid = is_process_running(process_name)
if pid is None:
    print(f"{process_name} is not running.")
    processes = list_processes()
    print("Running processes:")
    for pid_iter, name in processes:
        print(f"{pid_iter}: {name}")
    process_name = input("Enter the name of the process to send input to: ")
    pid = is_process_running(process_name)
    if pid is None:
        print(f"Process {process_name} not found.")
        sys.exit()

hwnds = get_hwnds_for_pid(pid)
if not hwnds:
    print(f"No window handles found for process {process_name}.")
    sys.exit()
else:
    hwnd = hwnds[0]
    print(f"Input will be sent to window handle {hwnd}.")

    # Bring the window to the foreground
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        print(f"Switched focus to {process_name}.")
    except Exception as e:
        print(f"Could not bring window to foreground: {e}")

# Variables to track pressed keys and buttons
keys_pressed = {'W': False, 'A': False, 'S': False, 'D': False, 'SPACE': False, 'I': False}
buttons_pressed = {'LEFT': False, 'RIGHT': False}

try:
    while True:
        # Check if the process is still running
        if not psutil.pid_exists(pid):
            print(f"Process {process_name} has ended. Exiting script.")
            break

        pygame.event.pump()
        x_axis = joystick.get_axis(0)  # Left/Right
        y_axis = joystick.get_axis(1)  # Up/Down

        threshold = 0.5  # Threshold to avoid noise

        # Forward (W)
        if y_axis < -threshold:
            if not keys_pressed['W']:
                press_key(SCANCODE['W'])
                keys_pressed['W'] = True
        else:
            if keys_pressed['W']:
                release_key(SCANCODE['W'])
                keys_pressed['W'] = False

        # Backward (S)
        if y_axis > threshold:
            if not keys_pressed['S']:
                press_key(SCANCODE['S'])
                keys_pressed['S'] = True
        else:
            if keys_pressed['S']:
                release_key(SCANCODE['S'])
                keys_pressed['S'] = False

        # Left (A)
        if x_axis < -threshold:
            if not keys_pressed['A']:
                press_key(SCANCODE['A'])
                keys_pressed['A'] = True
        else:
            if keys_pressed['A']:
                release_key(SCANCODE['A'])
                keys_pressed['A'] = False

        # Right (D)
        if x_axis > threshold:
            if not keys_pressed['D']:
                press_key(SCANCODE['D'])
                keys_pressed['D'] = True
        else:
            if keys_pressed['D']:
                release_key(SCANCODE['D'])
                keys_pressed['D'] = False

        # Joystick buttons
        # Button 0: Left mouse button
        if joystick.get_button(0):
            if not buttons_pressed['LEFT']:
                click_mouse('left', True)
                buttons_pressed['LEFT'] = True
        else:
            if buttons_pressed['LEFT']:
                click_mouse('left', False)
                buttons_pressed['LEFT'] = False

        # Button 1: Right mouse button
        if joystick.get_button(1):
            if not buttons_pressed['RIGHT']:
                click_mouse('right', True)
                buttons_pressed['RIGHT'] = True
        else:
            if buttons_pressed['RIGHT']:
                click_mouse('right', False)
                buttons_pressed['RIGHT'] = False

        # Button 2: Spacebar
        if joystick.get_button(2):
            if not keys_pressed['SPACE']:
                press_key(SCANCODE['SPACE'])
                keys_pressed['SPACE'] = True
        else:
            if keys_pressed['SPACE']:
                release_key(SCANCODE['SPACE'])
                keys_pressed['SPACE'] = False

        # Button 3: Key 'I'
        if joystick.get_button(3):
            if not keys_pressed['I']:
                press_key(SCANCODE['I'])
                keys_pressed['I'] = True
        else:
            if keys_pressed['I']:
                release_key(SCANCODE['I'])
                keys_pressed['I'] = False

        time.sleep(0.01)
except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    pygame.quit()
