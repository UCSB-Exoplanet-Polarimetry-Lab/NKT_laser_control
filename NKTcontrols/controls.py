from .NKTP_DLL import *

# TODO: add error handling if register result type is not good
# TODO: add return values for relevent functions
# TODO: update get_status function to show if the laser is off

def scan_ports():
    """Scan all ports and print out the devices connected to each port."""
    openPorts(getAllPorts(), 1, 1)
    print('Following ports has modules:', getOpenPorts())
    portlist = getOpenPorts().split(',')
    for portName in portlist:
        result, devList = deviceGetAllTypesV2(portName)
        for devId in range(0, len(devList)):
            if (devList[devId] != 0):
                print('Comport:',portName,'Device type:',"0x%0.4X" % devList[devId],'at address:',devId)

    # Close all ports
    closeResult = closePorts('')
    print('Close result: ', PortResultTypes(closeResult))


# Functions for the SuperK COMPACT
class compact:
    def __init__(self, COMport='COM3', COMPACT_devID=1):
        self.COMport = COMport
        self.COMPACT_devID = COMPACT_devID

    def get_interlock(self):
        """Get the interlock status"""
        result = registerReadU32(self.COMport, self.COMPACT_devID, 0x32, -1)
        LSB = result[1]

        if LSB == 2:
            print('Interlock is OK.')
        elif LSB == 1:
            print('Waiting for interlock to reset.')
        elif LSB == 0:
            print('Interlock off (interlock circuit open).')


    def disable_interlock(self):
        """Disable the interlock"""
        result = registerWriteReadU32(self.COMport, self.COMPACT_devID, 0x32, 0, -1)
        LSB = result[1]

        if LSB == 2:
            print('Interlock is OK.')
        elif LSB == 1:
            print('Waiting for interlock to reset.')
        elif LSB == 0:
            print('Interlock off (interlock circuit open).')


    def reset_interlock(self):
        """Reset the interlock. Make sure the physical key is switched ON before calling this function."""
        result = registerWriteReadU32(self.COMport, self.COMPACT_devID, 0x32, 1, -1)
        LSB = result[1]

        if LSB == 2:
            print('Interlock is OK.')
        elif LSB == 1:
            print('Waiting for interlock to reset.')
        elif LSB == 0:
            print('Interlock off (interlock circuit open).')


    def trig_mode(self, mode=None):
        """Get the current operating mode (pulse trigger source). Optional input to set the trigger mode."""
        mode_mapping = {
        0: 'Internal frequency generator',
        1: 'External trig',
        2: 'Software trigged burst',
        3: 'Hardware trigged burst',
        4: 'External gate on',
        5: 'External gate off',
        }

        if mode is None:
            result = registerReadU32(self.COMport, self.COMPACT_devID, 0x31, -1)
            status = mode_mapping[result[1]]
            print('Laser mode:', status)
        else:
            result = registerWriteReadU32(self.COMport, self.COMPACT_devID, 0x31, mode, -1)
            status = mode_mapping[result[1]]
            print('Laser mode:', status)


    def emission_on(self):
        """Turn on the laser emission."""
        result = registerWriteU8(self.COMport, self.COMPACT_devID, 0x30, 1, -1)
        print('Setting emission ON.')


    def emission_off(self):
        """Turn off the laser emission."""
        result = registerWriteU8(self.COMport, self.COMPACT_devID, 0x30, 0, -1)
        print('Setting emission OFF.')


    def get_emission(self):
        """Get the current emission status."""
        result = registerReadU8(self.COMport, self.COMPACT_devID, 0x30, -1)
        status = result[1]
        if status == 0:
            print('Emission is OFF.')
            return 0
        elif status == 1:
            print('Emission is ON.')
            return 1


    def overall_power(self, power=None):
        """Get the current overall power for laser emission as a percent. Optional input to set the power level."""
        if power is None:
            result = registerReadU8(self.COMport, self.COMPACT_devID, 0x3E, -1)
            current_power = result[1]
            print(f'Overall power level: {current_power}%')
        else:
            result = registerWriteReadU8(self.COMport, self.COMPACT_devID, 0x3E, power, -1)
            current_power = result[1]
            print(f'Setting overall power level to {current_power}%.')


    def get_max_pulse(self):
        """Get the maximum possible internal pulse frequency in Hz."""
        result = registerReadU32(self.COMport, self.COMPACT_devID, 0x36, -1)
        max_frequency = result[1]
        print(f'Maximum possible internal frequency: {max_frequency} Hz.')


    def pulse_frequency(self, frequency=None):
        """Get the current internal pulse frequency in Hz. Optional input to set the pulse frequency."""
        if frequency is None:
            result = registerReadU32(self.COMport, self.COMPACT_devID, 0x33, -1)
            current_frequency = result[1]
            print(f'Current internal pulse frequency: {current_frequency} Hz.')
        else:
            result = registerWriteReadU32(self.COMport, self.COMPACT_devID, 0x33, frequency, -1)
            current_frequency = result[1]
            print(f'Current internal pulse frequency: {current_frequency} Hz.')


    def display_backlight(self, brightness=None):
        """Get the current display backlight level as a percent. Optional input to set the brightness level."""
        if brightness is None:
            result = registerReadU32(self.COMport, self.COMPACT_devID, 0x26, -1)
            backlight_level = result[1]
            print('Display backlight level: ', backlight_level, '%')
        else:
            result = registerWriteReadU32(self.COMport, self.COMPACT_devID, 0x26, brightness, -1)
            backlight_level = result[1]
            print(f'Display backlight level set to {backlight_level}%.')


    def display_readout(self):
        """Readout of the text currently shown in the display."""
        result = registerRead(self.COMport, self.COMPACT_devID, 0x78, -1)
        print(result[1])


    def heat_sink_temp(self):
        """Heat sink temperature readout in C."""
        result = registerReadS16(self.COMport, self.COMPACT_devID, 0x1B, -1)
        temp = result[1] / 10
        print(f"Heat sink temperature: {temp} C.")


    def supply_voltage(self):
        """Readout the internal supply voltage in mV."""
        result = registerReadU16(self.COMport, self.COMPACT_devID, 0x1A, -1)
        voltage = result[1] # voltage given in mV
        print('Internal supply voltage:', voltage, 'mV.')


# Functions for the SuperK SELECT
class select:
    def __init__(self, COMport='COM3', SELECT_devID=16):
        self.COMport = COMport
        self.SELECT_devID = SELECT_devID


    def crystal1_range(self):
        """Crystal 1 (VIS/NIR) wavelength range in nm."""
        result1 = registerReadU32(self.COMport, self.SELECT_devID, 0x90, -1)
        min = result1[1]/1000 # convert pm to nm

        result2 = registerReadU32(self.COMport, self.SELECT_devID, 0x91, -1)
        max = result2[1]/1000

        print(f'Crystal 1 (VIS/NIR) wavelength range: {int(min)} nm to {int(max)} nm.')


    def crystal2_range(self):
        """Crystal 2 (NIR/IR) wavelength range in nm."""
        result1 = registerReadU32(self.COMport, self.SELECT_devID, 0xA0, -1)
        min = result1[1]/1000 # convert pm to nm

        result2 = registerReadU32(self.COMport, self.SELECT_devID, 0xA1, -1)
        max = result2[1]/1000

        print(f'Crystal 2 (NIR/IR) wavelength range: {int(min)} nm to {int(max)} nm.')


    # def power_monitor(self):    # CHECK
    #     """Readout from optional optical power monitors. Result as a percent."""
    #     result1 = registerReadU16(self.COMport, self.SELECT_devID, 0x10, -1)
    #     power1 = result1[1]/10

    #     result2 = registerReadU16(self.COMport, self.SELECT_devID, 0x11, -1)
    #     power2 = result2[1]/10

    #     print(f'Power monitor 1 readout: {power1} %, power monitor 2 readout: {power2} %.')


    # def monitor_switch(self, crystal=None):  # CHECK
        # """Select which power detector should be connected to the output connector. Optional input 1 or 2 to switch to the corresponding crystal."""
        # if crystal==None:
        #     result = registerReadU8(self.COMport, self.SELECT_devID, 0x35, -1)
        #     result = result[1]
        #     if result == 0:
        #         print('Optical power monitor connected to crystal 1.')
        #     elif result == 1:
        #         print('Optical power monitor connected to crystal 2.')

        # elif crystal == 1:
        #     result = registerWriteReadU8(self.COMport, self.SELECT_devID, 0x35, 0, -1)
        #     print('Optical power monitor connected to crystal 1.')
        # elif crystal == 2:
        #     result = registerWriteReadU8(self.COMport, self.SELECT_devID, 0x35, 1, -1)
        #     print('Optical power monitor connected to crystal 2.')

        # else:
        #     print('Invalid input. Choose 1 or 2.')


# Functions for the (external) RF driver in charge of controlling the SELECT wavelengths
class driver:
    def __init__(self, COMport='COM3', RFdriver_devID=17):
        self.COMport = COMport
        self.RFdriver_devID = RFdriver_devID


    def crystal_temp(self):
        """Read the connected crystal temperature in degrees Celsius."""
        result = registerReadS16(self.COMport, self.RFdriver_devID, 0x38, -1)
        temperature = result[1]/10 # convert temp from tenths of degrees to degrees
        print('Crystal temperature: ', temperature, 'degrees C.')


    def RF_power_on(self):
        """Turn on power output to the RF driver to SuperK SELECT."""
        result = registerWriteReadU8(self.COMport, self.RFdriver_devID, 0x30, 1, -1)
        result = registerReadU8(self.COMport, self.RFdriver_devID, 0x30, -1)
        power = result[1]
        if power==0:
            print('RF power is OFF.')
        elif power==1:
            print('RF power is ON.')


    def RF_power_off(self):
        """Turn off power output to the RF driver to SuperK SELECT."""
        result = registerWriteReadU8(self.COMport, self.RFdriver_devID, 0x30, 0, -1)
        result = registerReadU8(self.COMport, self.RFdriver_devID, 0x30, -1)
        power = result[1]
        if power==0:
            print('RF power is OFF.')
        elif power==1:
            print('RF power is ON.')

    def get_RF_power(self):
        """Get the current RF power status."""
        result = registerReadU8(self.COMport, self.RFdriver_devID, 0x30, -1)
        power = result[1]
        if power==0:
            print('RF power is OFF.')
            return 0
        elif power==1:
            print('RF power is ON.')
            return 1


    def read_connected_crystal(self):
        """Read the current connected crystal."""
        result = registerReadS8(self.COMport, self.RFdriver_devID, 0x75, -1)
        crystal_type = result[1]

        if crystal_type==0:
            print('No crystal is connected to the RF driver.')
        elif crystal_type==1:
            print('Connected to crystal: 1 (VIS/NIR).')
        elif crystal_type==2:
            print('Connected to crystal: 2 (NIR/IR).')
        else:
            print('Connected to crystal:', crystal_type)


    def set_channel(self, channel, wavelength, amplitude):          # WORKS
        """Specify the channel (1-8), then set the wavelength in nm and amplitude as a percent for that channel."""
        channel_ID = int(channel-1)
        wavelength_address = f"0x9{channel_ID}"
        wavelength_address = int(wavelength_address, 16)
        wavelength_pm = int(wavelength*1000) # convert nm to pm as the input format

        amplitude_address = f"0xB{channel_ID}"
        amplitude_address = int(amplitude_address, 16)
        amplitude_percent = int(amplitude*10) # convert to tenths of a percent as the imput format

        result1 = registerWriteReadU32(self.COMport, self.RFdriver_devID, wavelength_address, wavelength_pm, 0) # send index 0 if not in FSK mode
        result2 = registerWriteReadU16(self.COMport, self.RFdriver_devID, amplitude_address, amplitude_percent, -1)

        print(f'Channel {channel} wavelength set to:', result1[1]/1000, 'nm, amplitude set to:', result2[1]/10, '%.')

    
    def get_channels(self):
        """Read the current channels and print which ones are on and at what settings."""
        off_channels = []
        for channel in range(0, 8):
            wavelength_address = f"0x9{channel}"
            wavelength_address = int(wavelength_address, 16)

            amplitude_address = f"0xB{channel}"
            amplitude_address = int(amplitude_address, 16)

            result1 = registerReadU32(self.COMport, self.RFdriver_devID, wavelength_address, 0)
            result2 = registerReadU16(self.COMport, self.RFdriver_devID, amplitude_address, -1)

            if result2[1] != 0:
                print(f'Channel {channel+1} is ON, wavelength: {result1[1]/1000} nm, amplitude: {result2[1]/10} %.')
            else:
                # print(f'Channel {channel} is OFF.')
                off_channels.append(channel+1)
        print(f'Channels {off_channels} are OFF')


def get_status(compact, driver):
    """Get the overall status, all relevant information."""
    compact.get_interlock()
    compact.trig_mode()

    emission_status = compact.get_emission()
    if emission_status == 1:
        compact.overall_power()
        # compact.pulse_frequency()
    elif emission_status == 0:
        pass

    RF_status = driver.get_RF_power()
    if RF_status == 1:
        # driver.read_connected_crystal()
        driver.get_channels()
    elif RF_status == 0:
        pass
