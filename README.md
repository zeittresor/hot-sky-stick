Using this mod you can use your regular USB Joystick (hot swappend) while you play - just plug it into your system and start the mod.. :-)

- Start Skyrim SE (but no worry if it is the Skyrim (old) or a different game supporting WSAD controls - it should also work*).
- After you have started your game switch back to desktop using alt+tab
- plug-in / swap your usb joystick into your pc, start the application of the mod (with administrator rights)
  -> right mouseclick onto the executable of the mod "run as administrator"

.. it should switch back to Skyrim SE .. *if not a list of all running processes will be showen, do not enter
the process id but the name of the process you want to send the joystick input to.

The Inputs are:
Up -> Keyboard Key W
Down -> Keyboard Key S
Left -> Keyboard Key A
Right -> Keyboard Key D
Trigger #0 -> Emulate Left Mouse Button
Trigger #1 -> Emulate Right Mouse Button
Trigger #2 -> Keyboard Key Space
Trigger #3 -> Keyboard Key I

![joystick1_small](https://github.com/user-attachments/assets/f1677da5-20cb-4aa2-a759-8801cbe0db4b)

How it works
The Mod Utility is just seaching for a joystick connected to your System, if a joystick is detected the utility will send the input as keyboard keys
to the running Skyrim process (like a keyboard it is also doing). If the regular Skyrim SE process is detected it will automaticly switch back to the game,
if not you can specify the running process name like tesv.exe or skyrim.exe or how ever the game name is (the reason to make it dynamic like this is
that you can use the tool with almost every game wich is supporting WSAD input to control) :-)

![joystick](https://github.com/user-attachments/assets/76606d44-fec9-4f94-bc15-ee5abd0d3475)

History
v1.0 (26-October-2024)
- Basic Controls by emulating Keypress WSAD with 4 Trigger
- First compiled Version of the mod
- Include the python sourcecode of the mod for other modders (make sure to link back here if u do, please)

This is a mod for Skyrim (SSE) created by triplex2011 (zeittresor) but it should work also with the old vanilla version as long with Fallout or some other games..

Mod Page: https://www.nexusmods.com/skyrimspecialedition/mods/132391
