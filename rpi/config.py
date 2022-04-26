import platform

os_info = platform.platform()
COM_PORT = None
if 'windows' in os_info.lower():
    COM_PORT = 'COM5'
elif 'linux' in os_info.lower():
    COM_PORT = 'ACM0'
BOARD_ORIGIN = (151, 85)  # Gantry position for grid origin
ORIGIN = (BOARD_ORIGIN[0] - 4*25.4, BOARD_ORIGIN[1] - 4*25.4)
# ORIGIN = (103, 63)