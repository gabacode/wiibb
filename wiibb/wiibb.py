import evdev
from evdev import ecodes


class WiiBalanceBoard:
    def __init__(self):
        self.device = self.get_device()

    @staticmethod
    def get_device():
        """Return the Wii Balance Board device."""
        devices = [
            path
            for path in evdev.list_devices()
            if evdev.InputDevice(path).name == "Nintendo Wii Remote Balance Board"
        ]
        if not devices:
            return None

        board = evdev.InputDevice(
            devices[0],
        )
        return board

    def get_raw_measurement(self):
        """Read one measurement from the board."""
        data = [None] * 4
        while True:
            event = self.device.read_one()
            if event is None:
                continue
            if event.code == ecodes.ABS_HAT1X:
                data[0] = event.value / 100  # Top left
            elif event.code == ecodes.ABS_HAT0X:
                data[1] = event.value / 100  # Top right
            elif event.code == ecodes.ABS_HAT0Y:
                data[2] = event.value / 100  # Bottom left
            elif event.code == ecodes.ABS_HAT1Y:
                data[3] = event.value / 100  # Bottom right
            elif event.code == ecodes.SYN_REPORT and event.value == 0:
                if None not in data:
                    return data
                data = [None] * 4

    @staticmethod
    def calculate_cop(data):
        """Calculate the center of pressure (CoP) based on the four corner weights."""
        TL, TR, BL, BR = data

        # Normalize x and y coordinates to the range -1 to 1
        x_cop = ((TR + BR) - (TL + BL)) / (TL + TR + BL + BR)  # x-axis correction
        y_cop = ((TL + TR) - (BL + BR)) / (TL + TR + BL + BR)  # y-axis correction

        return x_cop, y_cop
