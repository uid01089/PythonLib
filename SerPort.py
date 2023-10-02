# This class provides an interface for serial port communication, with options for both hardware and dummy (testing) implementations.
import logging
import serial

logger = logging.getLogger('PythonLib.SerPort')

# See https://pyserial.readthedocs.io/en/latest/shortintro.html


class SerPort:
    def read(self) -> bytes:
        """
        Read data from the serial port.

        Returns:
            bytes: The data read from the port.
        """
        raise NotImplementedError

    def write(self, data: bytes) -> None:
        """
        Write data to the serial port.

        Args:
            data (bytes): The data to be written to the port.
        """
        raise NotImplementedError

    def delete(self, bytesToDelete: bytes) -> None:
        """
        Delete specific bytes from the buffer.

        Args:
            bytesToDelete (bytes): The bytes to be deleted from the buffer.
        """
        raise NotImplementedError

    def setup(self) -> None:
        """
        Set up the serial port connection (specific to hardware implementation).
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        Start the serial port connection (specific to hardware implementation).
        """
        raise NotImplementedError

    def clear(self) -> None:
        """
        Clear the serial port buffer.
        """
        raise NotImplementedError


class SerPortDummy(SerPort):
    def __init__(self, data: bytes) -> None:
        self.buffer = data

    def read(self) -> bytes:
        return self.buffer

    def write(self, data: bytes) -> None:
        self.buffer = data

    def delete(self, bytesToDelete: bytes) -> None:
        logger.debug("SerPort delete %s", bytesToDelete)
        self.buffer = self.buffer.replace(bytesToDelete, b'')

    def setup(self) -> None:
        pass

    def start(self) -> None:
        pass

    def clear(self) -> None:
        self.buffer = b''


class SerPortHw(SerPortDummy):

    def __init__(self, serPort: serial.Serial) -> None:
        super().__init__(b'')
        self.serial = serPort

    def setup(self) -> None:

        self.serial.baudrate = 9600
        self.serial.parity = 'N'
        self.serial.stopbits = 1
        self.serial.bytesize = 8
        self.serial.timeout = None
        self.serial.xonxoff = 0
        self.serial.rtscts = 0

    def start(self) -> None:
        logger.debug('SerPort start')
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def write(self, data: bytes) -> None:
        logger.debug("SerPort write %s", data)
        self.serial.write(data)

    def read(self) -> bytes:
        inputData = self.serial.read_all()
        if inputData:
            self.buffer = self.buffer + inputData
            logger.debug("SerPort read %s", self.buffer)

        return self.buffer

    def clear(self) -> None:
        self.buffer = b''
        self.serial.read_all()
