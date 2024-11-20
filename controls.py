from NKTP_DLL import *

COMport = 'COM3' # depends on the port the device is connected to. COM3 for Rayleigh desktop
COMPACT_devID = 1 # fixed for the SuperK COMPACT
SELECT_devID = 16 # fixed for the SuperK SELECT
RFdriver_devID = 17 # fixed for the SuperK RF driver

# TODO: make classes for the COMPACT and SELECT devices
# TODO: don't print regresult status each time
# TODO: make a document to list all of these functions
# TODO: find a way to turn on/off power to the RF channels separately

# Scan all ports and print out the devices connected to each port
def scan_ports():
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

def get_interlock():
    """Get the interlock status"""
    result = registerReadU32(COMport, COMPACT_devID, 0x32, -1)
    LSB = result[1]

    if LSB == 2:
        print('Interlock is OK.')
    elif LSB == 1:
        print('Waiting for interlock to reset.')
    elif LSB == 0:
        print('Interlock off (interlock circuit open).')


def disable_interlock():
    """Disable the interlock"""
    result = registerWriteReadU32(COMport, COMPACT_devID, 0x32, 0, -1)
    LSB = result[1]

    if LSB == 2:
        print('Interlock is OK.')
    elif LSB == 1:
        print('Waiting for interlock to reset.')
    elif LSB == 0:
        print('Interlock off (interlock circuit open).')


def reset_interlock():
    """Reset the interlock. Make sure the physical key is switched ON before calling this function."""
    result = registerWriteReadU32(COMport, COMPACT_devID, 0x32, 1, -1)
    LSB = result[1]

    if LSB == 2:
        print('Interlock is OK.')
    elif LSB == 1:
        print('Waiting for interlock to reset.')
    elif LSB == 0:
        print('Interlock off (interlock circuit open).')


def trig_mode(mode=None):
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
        result = registerReadU32(COMport, COMPACT_devID, 0x31, -1)
        status = mode_mapping[result[1]]
        print('Laser mode:', status)
    else:
        result = registerWriteReadU32(COMport, COMPACT_devID, 0x31, mode, -1)
        status = mode_mapping[result[1]]
        print('Laser mode:', status)


def emission_on():
    """Turn on the laser emission."""
    result = registerWriteU8(COMport, COMPACT_devID, 0x30, 1, -1) # devID=1 for Compact
    print('Setting emission ON.', RegisterResultTypes(result))


def emission_off():
    """Turn off the laser emission."""
    result = registerWriteU8(COMport, COMPACT_devID, 0x30, 0, -1)
    print('Setting emission OFF.', RegisterResultTypes(result))


def overall_power(power=None):
    """Get the current overall power for laser emission as a percent. Optional input to set the power level."""
    if power is None:
        result = registerReadU8(COMport, COMPACT_devID, 0x3E, -1)
        current_power = result[1]
        print(f'Overall power level: {current_power}%')
    else:
        result = registerWriteReadU8(COMport, COMPACT_devID, 0x3E, power, -1)
        current_power = result[1]
        print(f'Setting overall power level to {current_power}%.')


def get_max_pulse():
    """Get the maximum possible internal pulse frequency in Hz."""
    result = registerReadU32(COMport, COMPACT_devID, 0x36, -1)
    max_frequency = result[1]
    print(f'Maximum possible internal frequency: {max_frequency} Hz.')


def pulse_frequency(frequency=None):
    """Get the current internal pulse frequency in Hz. Optional input to set the pulse frequency."""
    if frequency is None:
        result = registerReadU32(COMport, COMPACT_devID, 0x33, -1)
        current_frequency = result[1]
        print(f'Current internal pulse frequency: {current_frequency} Hz.')
    else:
        result = registerWriteReadU32(COMport, COMPACT_devID, 0x33, frequency, -1)
        current_frequency = result[1]
        print(f'Current internal pulse frequency: {current_frequency} Hz.')


def display_backlight(brightness=None):
    """Get the current display backlight level as a percent. Optional input to set the brightness level."""
    if brightness is None:
        result = registerReadU32(COMport, COMPACT_devID, 0x26, -1)
        backlight_level = result[1]
        print('Display backlight level: ', backlight_level, '%')
    else:
        result = registerWriteReadU32(COMport, COMPACT_devID, 0x26, brightness, -1)
        backlight_level = result[1]
        print(f'Display backlight level set to {backlight_level}%.')


def display_readout():
    """Readout of the text currently shown in the display."""
    result = registerRead(COMport, COMPACT_devID, 0x78, -1)
    print(result[1])


def heat_sink_temp():
    """Heat sink temperature readout in C."""
    result = registerReadS16(COMport, COMPACT_devID, 0x1B, -1)
    temp = result[1] / 10
    print(f"Heat sink temperature: {temp} C.")


def supply_voltage():
    """Readout the internal supply voltage in mV."""
    result = registerReadU16(COMport, COMPACT_devID, 0x1A, -1)
    voltage = result[1] # voltage given in mV
    print('Internal supply voltage:', voltage, 'mV.')


# Now functions for the SuperK SELECT

def crystal1_range():
    """Crystal 1 (VIS/NIR) wavelength range in nm."""
    result1 = registerReadU32(COMport, SELECT_devID, 0x90, -1)
    min = result1[1]/1000 # convert pm to nm

    result2 = registerReadU32(COMport, SELECT_devID, 0x91, -1)
    max = result2[1]/1000

    print(f'Crystal 1 (VIS/NIR) wavelength range: {int(min)} nm to {int(max)} nm.')


def crystal2_range():
    """Crystal 2 (NIR/IR) wavelength range in nm."""
    result1 = registerReadU32(COMport, SELECT_devID, 0xA0, -1)
    min = result1[1]/1000 # convert pm to nm

    result2 = registerReadU32(COMport, SELECT_devID, 0xA1, -1)
    max = result2[1]/1000

    print(f'Crystal 2 (NIR/IR) wavelength range: {int(min)} nm to {int(max)} nm.')


# now functions for the RF driver in charge of controlling the SELECT wavelengths

def crystal_temp():
    """Read the connected crystal temperature in degrees Celsius."""
    result = registerReadS16(COMport, RFdriver_devID, 0x38, -1)
    temperature = result[1]/10 # convert temp from tenths of degrees to degrees
    print('Crystal temperature: ', temperature, 'degrees C.')


def RF_power_on():
    """Turn on power output to the RF driver to SuperK SELECT."""
    result = registerWriteReadU8(COMport, RFdriver_devID, 0x30, 1, -1)
    result = registerReadU8(COMport, RFdriver_devID, 0x30, -1)
    power = result[1]
    if power==0:
        print('RF power is off.')
    elif power==1:
        print('RF power is on.')


def RF_power_off():
    """Turn off power output to the RF driver to SuperK SELECT."""
    result = registerWriteReadU8(COMport, RFdriver_devID, 0x30, 0, -1)
    result = registerReadU8(COMport, RFdriver_devID, 0x30, -1)
    power = result[1]
    if power==0:
        print('RF power is off.')
    elif power==1:
        print('RF power is on.')


def read_connected_crystal():
    """Read the current connected crystal."""
    result = registerReadS8(COMport, RFdriver_devID, 0x75, -1)
    crystal_type = result[1]

    if crystal_type==0:
        print('No crystal is connected to the RF driver.')
    elif crystal_type==1:
        print('Connected to crystal: 1 (VIS/NIR).')
    elif crystal_type==2:
        print('Connected to crystal: 2 (NIR/IR).')
    else:
        print('Connected to crystal:', crystal_type)


def set_channel(channel, wavelength, amplitude):          # WORKS
    """Specify the channel (1-8), then set the wavelength in nm and amplitude as a percent for that channel."""
    wavelength_channel_ID = int(channel-1)
    wavelength_address = f"0x9{wavelength_channel_ID}"
    wavelength_address = int(wavelength_address, 16)
    wavelength_pm = int(wavelength*1000) # convert nm to pm as the input format

    amplitude_channel_ID = int(channel-1)
    amplitude_address = f"0xB{amplitude_channel_ID}"
    amplitude_address = int(amplitude_address, 16)
    amplitude_percent = int(amplitude*10) # convert to tenths of a percent as the imput format

    result1 = registerWriteReadU32(COMport, RFdriver_devID, wavelength_address, wavelength_pm, 0) # send index 0 if not in FSK mode
    result2 = registerWriteReadU16(COMport, RFdriver_devID, amplitude_address, amplitude_percent, -1)

    print(f'Channel {channel} wavelength set to:', result1[1]/1000, 'nm, amplitude set to:', result2[1]/10, '%.')

