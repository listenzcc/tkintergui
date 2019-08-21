# coding: utf-8

import numpy as np
from myClientNew import ScanClient

class Buffer():
    def __init__(self, offline=False):
        self.nchan = 68
        self.all_buffer = np.empty((self.nchan, 0))
        self.is_on = False
        self.record = False
        self.offline = offline

    def record_buffer(self, buffer):
        if self.record:
            self.all_buffer = np.concatenate((self.all_buffer, buffer), axis=1)
            print('  ', self.all_buffer.shape)
        else:
            pass

    def on(self, IP, port):
        if self.is_on:
            print('Connected: IP: %s port: %d' % (IP, port))
            return 0

        # No connection when offline testing
        if self.offline:
            return 0

        self.client = ScanClient(IP, port)
        self.client.register_receive_callback(self.record_buffer)
        self.record = False
        self.client.start_receive_thread(self.nchan)
        self.client.start_sending_data()
        self.is_on = True
        print('Connection established: IP: %s port: %d' % (IP, port))

    def off(self):
        if not self.is_on:
            print('Unconnected, do nothing.')
            return 0
        print('Disconnect, connection can not be recovered.')
        try:
            self.client.stop_receive_thread(stop_measurement=True)
            self.client._send_command(c.commandDict['Request_to_Stop_Sending_Data'])
            self.client._close_connect()
            self.client._sock.close()
        except:
            pass

    def start(self):
        if not self.is_on:
            return 0
        self.all_buffer = np.empty((self.nchan, 0))
        self.record = True

    def stop(self):
        if not self.is_on:
            return 0
        self.record = False

    def output(self, n=4000):
        assert(not self.record)
        if self.offline:
            return 'offline'
        return self.all_buffer[:, -n:]
        