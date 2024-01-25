import udi_interface
import logging
import sys
import time
import socket
import threading
import const
from nodes import ctl
from nodes import zone
from nodes import area


LOGGER = udi_interface.LOGGER
CUSTOM = udi_interface.Custom



class XRMessage():
    def __init__(self, poly, cmd='', data=''):
        self.poly = poly
        self.account = ''
        self.ipaddress = ''
        self.cmd_port = 0
        self.cmd_sock = None
        self.cmd_connected = False
        self.recv_port = 0;
        self.recv_sock = None
        self.recv_connected = False
        self.recv_thread = None
        self.resp_thread = None
        self.command = cmd
        self.data = data
        self.minutes_ago = 0
        self.ctl = None
        self.protocol_sync = threading.Semaphore(0)
        self.Event = b''
        self.Lenght = 0
        self.Type = b''
        self.Zone = b''
        self.Area = b''
        self.Area_name = b''
        self.User = b''
        self.Device = b''
        self.Time = b''
        self.Holiday = b''
        self.Date = b''
        self.Equip = b''
        self.Svc = b''
        self.EventQ = b''
        self.PgmInfo = b''
        

 
    def parameterHandler(self, params):
        self.parameters.load(params)
 
    def startListener(self):
        # Start a thread that listens for status updates from the  XR.
        self.stat_thread = threading.Thread(target=self.recvLoop, args=(self.processRecvMsg,))
        self.stat_thread.daemon = True
        self.stat_thread.start()
   

    def connectCmd(self):
        LOGGER.debug('Connecting to  XR cmd_port IP=: {} Port=: {}'.format(self.ipaddress, self.cmd_port))

        self.cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cmd_sock.settimeout(10) # allow 10 second for connection
        try:
            self.cmd_sock.connect((self.ipaddress, self.cmd_port))
            self.cmd_sock.setblocking(False)
        except:
            LOGGER.error('Failed to connect to XR Command port')
            

    '''
    Send request is used for commands that require addition handling
    because the arrive in multiple packets and require additional send
    '''
    def sendRequest(self, cmd, data, handler, n_queue, request_sync):
        error = True
        while error:
            self.connectCmd()
            self.command = cmd
            self.data = data        
            data = self.serializeCommand()
            data_len = len(data)
            error = False

            if self.sendToXR(data) == 0:
                error = True
                continue
            buf = bytearray(1000)
            st=0
            LOGGER.info('Waiting for response...')
            retry = 0
            while st == 0:
                try:
                    tcp = self.cmd_sock.recv(1000)
                except BlockingIOError:
                    time.sleep(0.5)
                    retry+=1
                    if retry > 20:
                        LOGGER.warning('Timed out waiting for response.')
                        error = True
                        break
                    continue
                except ConnectionResetError as msg:
                    LOGGER.error('Connection error: ' + str(msg))
                    error = True
                    break
                if len(tcp) == 0:
                    error = True
                    break
                LOGGER.debug('len= %s data= %s', len(tcp), tcp)
                LOGGER.debug('%s', '[{}]'.format(', '.join(hex(x) for x in tcp)))
                rcvData = tcp[0:]
                for b in rcvData:
                    if b == 0x0d:  # looking for end byte
                        buf[st] = b
                        message = self.deserializeReqResp(buf[0:st+1])
                        if message.data[0] == 0x2d: # If data starts with '_'' we are done
                            st = 1
                            break #Exit for loop and while loop st != 0
                        else:
                            LOGGER.debug('Found 0x0d Dispatching handler')
                            self.resp_thread = threading.Thread(target=handler, args=(message, self.protocol_sync, n_queue))
                            self.resp_thread.daemon = True
                            self.resp_thread.start()
                            self.protocol_sync.acquire()    #We will wait here until the response has been processed                  
                            #
                            # Send request for more data
                            #  
                            self.command = cmd
                            self.data = b''
                            data = self.serializeCommand()
                            if self.sendToXR(data) == 0:
                                raise RuntimeError("socket connection broken")
                            else:
                                st = 0
                                break 
                    else: 
                        buf[st] = b
                        st += 1
            LOGGER.info('sendRequest Completed releasing lock')
            request_sync.release()                  
            try:
                self.cmd_sock.shutdown(socket.SHUT_RDWR)
                self.cmd_sock.close()
            except:
                pass

    def sendCommand(self, cmd, data=b''):
        self.connectCmd()
        self.command = cmd
        self.data = data
        data = self.serializeCommand()

        if self.sendToXR(data) == 0:
            raise RuntimeError("socket connection broken")
        buf = bytearray(1000)
        st=0
        LOGGER.info('Waiting for response...')
        while st == 0:
            try:
                tcp = self.cmd_sock.recv(1000)
                LOGGER.debug('len= %s data= %s', len(tcp), tcp)
                LOGGER.debug('%s', '[{}]'.format(', '.join(hex(x) for x in tcp)))
                data = tcp[0:]
                for b in data:
                    if b == 0x0d:  # looking for end byte
                        buf[st] = b
                        message = self.deserializeCmdResp(buf[0:st+1])
                        break
                    else:
                        buf[st] = b
                        st += 1
            except BlockingIOError:
                LOGGER.debug('Waiting on data...')
                time.sleep(0.5)
                continue
            except ConnectionResetError as msg:
                LOGGER.error('Connection error: ' + str(msg))
            
        try:
            self.cmd_sock.shutdown(socket.SHUT_RDWR)
            self.cmd_sock.close()
        except:
            pass
        LOGGER.info('sendCommand Completed')
        return message

    def sendToXR(self,data):
        data_len = len(data)    
        totalsent = 0
        LOGGER.info('Sending to XR...')
        LOGGER.debug('%s\r%s','[{}]'.format(data), '[{}]'.format(', '.join(hex(x) for x in data)))

        while totalsent < data_len:
            try:
                sent = self.cmd_sock.send(data[totalsent:])
                totalsent += sent
            except socket.timeout:
                continue
        return totalsent
        
    def serializeCommand(self):
        return b''.join([b'\x02@', bytearray(self.account.encode()), self.command, self.data, b'\r'])

    def serializeResponse(self):
        return b''.join([b'\x02', bytearray(self.account.encode()), self.command, b'\r'])

 
    def recvLoop(self, handler):
        startup = True
        while True:
            try: 
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.bind(('', self.recv_port))
                s.listen(1)
            except socket.error as e: 
                LOGGER.error('Error will retry.. {}'.format(e)) 
                try:
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except:
                    pass
                time.sleep(2)
                continue        
            self.recv_connected = True
            LOGGER.info('Listening on receive port: {}'.format(self.recv_port))

            while True:
                try:
                    self.recv_sock, addr = s.accept()
                except socket.error as e: 
                    LOGGER.error('Error in socket accept  {}'.format(e)) 
                    self.recv_connected = False
                    break
                LOGGER.debug('Connection from {}'.format(addr))
                while True:
                    try:
                        tcp = self.recv_sock.recv(1024)
                        if not tcp:
                            break # No more data for now, go back to accept
                    except socket.error as e: 
                        LOGGER.error('Error in recv {}'.format(e))
                        self.recv_connected = False
                        break
                    LOGGER.debug('Received from XR: len= %s data= %s', len(tcp), tcp)
                    LOGGER.debug('len= %s data= %s', len(tcp), '[{}]'.format(', '.join(hex(x) for x in tcp)))
                    message = self.deserializeStatus(tcp[0:-1])
                    if startup:
                        if message.minutes_ago > 2:
                            LOGGER.debug('Tossing stale message from {} minutes ago'.format(message.minutes_ago))
                            self.sendAck()
                            continue
                        else:
                            startup = False        
                    message.parse()
                    handler(message)
                    self.sendAck()
                if self.recv_connected == False:
                    try:
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                    except:
                        pass
                    break
 
    def processRecvMsg(self, msg):

        c_node = self.poly.getNode('controller')
        try:  
            if msg.command == const._MSG_EVENT_ZONE_ALARM:
                z_node = self.getZoneNode(msg)
                stat = z_node.setNextStatus(msg.command)
                if z_node.ZoneType == const._XR_ZONE_TYPE_FIRE or z_node.ZoneType == const._XR_ZONE_TYPE_FIREVERIFY:
                    c_node.set_alarmState(const._XR_CTL_ALARM_STATE_FIRE)
                elif z_node.ZoneType == const._XR_ZONE_TYPE_CARBONMONOXIDE:
                    c_node.set_alarmState(const._XR_CTL_ALARM_STATE_CO)
                elif z_node.ZoneType == const._XR_ZONE_TYPE_SUPERVISORY:
                    c_node.set_alarmState(const._XR_CTL_ALARM_STATE_SUPERVISORY)
                else:
                    c_node.set_alarmState(const._XR_CTL_ALARM_STATE_ALARM)

            elif msg.command == const._MSG_EVENT_DEVICE_STATUS:
                if msg.Zone != b'': # Is it a zone status?
                    z_node = self.getZoneNode(msg)
                    if msg.Type == b'"DO':
                        z_node.set_state(const._XR_ZONE_STATE_OPEN)
                    elif msg.Type == b'"DC':
                        z_node.set_state(const._XR_ZONE_STATE_CLOSED)
                        stat = z_node.setNextStatus(const._MSG_EVENT_ZONE_CLOSE)
                if msg.Type == b'"ON':
                    o_node = self.getDeviceNode(msg)
                    o_node.set_status(const._XR_OUTPUT_STATUS_STEADY)
                elif msg.Type == b'"OF':
                    o_node = self.getDeviceNode(msg)
                    o_node.set_status(const._XR_OUTPUT_STATUS_OFF)
                elif msg.Type == b'"PL':
                    o_node = self.getDeviceNode(msg)
                    o_node.set_status(const._XR_OUTPUT_STATUS_PULSE)
                elif msg.Type == b'"TP':
                    o_node = self.getDeviceNode(msg)
                    o_node.set_status(const._XR_OUTPUT_STATUS_TEMPORAL3)
                elif msg.Type == b'"MO':
                    o_node = self.getDeviceNode(msg)
                    o_node.set_status(const._XR_OUTPUT_STATUS_MOMENTARY)
            elif msg.command == const._MSG_EVENT_ZONE_LOWBAT:   
                z_node = self.getZoneNode(msg)
                z_node.set_status(const._XR_ZONE_STATUS_LOWBATTERY)

            elif msg.command == const._MSG_EVENT_ZONE_MISSING:  
                z_node = self.getZoneNode(msg)
                z_node.set_status(const._XR_ZONE_STATUS_MISSING)

            elif msg.command == const._MSG_EVENT_ZONE_TAMPER:  
                z_node = self.getZoneNode(msg)
                z_node.set_status(const._XR_ZONE_STATUS_TAMPER)

            elif msg.command == const._MSG_EVENT_DOOR_ACCESS: 
                pass

            elif msg.command == const._MSG_EVENT_ARMING:      
                a_node = self.getAreaNode(msg)
                if msg.Type == b'"CL':
                    a_node.set_status(const._XR_AREA_STATUS_ARMED)
                    for n in self.poly.nodes():
                        if n.primary == a_node.address and const._XR_ZONE_NODE in n.id:
                            n.setNextStatus(const._MSG_EVENT_ARMED)
                    c_node.set_alarmState(c_node.getArmedStatus())    

                elif msg.Type == b'"OP':
                    a_node.set_status(const._XR_AREA_STATUS_DISARMED)
                    for n in self.poly.nodes():
                        if n.primary == a_node.address and const._XR_ZONE_NODE in n.id:
                            n.setNextStatus(const._MSG_EVENT_DISARMED)    
                    c_node.set_alarmState(c_node.getArmedStatus())    

            elif msg.command == const._MSG_EVENT_ZONE_RESTORE:
                z_node = self.getZoneNode(msg)
                stat = z_node.setNextStatus(msg.command)
                #z_node.reportCmd(const._XR_ZONE_CMD_RESTORED)

            elif msg.command == const._MSG_EVENT_SYSTEM_MSG:
                type = msg.Type
                if type == b'009':
                    c_node.set_battery(1)
                elif type == b'001':
                    c_node.set_battery(0)
                elif type == b'008':
                    c_node.set_ac(1)
                elif type == b'000':
                    c_node.set_ac(0)
                elif type == b'087':
                    c_node.set_lastMessage('Transmit Failed')
                elif type == b'153':
                    c_node.set_lastMessage('Communication Trouble')

            elif msg.command == const._MSG_EVENT_ZONE_TROUBLE:      #trouble
                z_node = self.getZoneNode(msg)
                z_node.set_status(const._XR_ZONE_STATUS_TROUBLE)

            elif msg.command == const._MSG_EVENT_ZONE_FAULT:      #fault
                z_node = self.getZoneNode(msg)
                z_node.set_state(const._XR_ZONE_STATE_OPEN)

            elif msg.command == const._MSG_EVENT_ZONE_BYPASS:      #bypass
                z_node = self.getZoneNode(msg)
                z_node.setNextStatus(msg.command)
                z_node.set_bypass(1)

            elif msg.command == const._MSG_EVENT_ZONE_RESET:      #unbypass
                z_node = self.getZoneNode(msg)
                z_node.setNextStatus(msg.command)
                z_node.set_bypass(0)
        except TypeError:
            pass
    '''
    Area can contain 1-3 numeric with optional " follow by area name
    '''
    def getAreaNode(self, msg):
        Anode = ''
        num , name = self.getNumName(msg.Area)
        msg.Area_name = name
        Aaddr = 'area_{:03}'.format(int(num))
        Anode = self.poly.getNode(Aaddr)
        if not Anode:
            LOGGER.error('poly.getNode failed to find {}'.format(Aaddr))
            raise TypeError('poly.getNode failed to find')
        return Anode
 
    '''
    Zone can contain 1-3 numeric with optional " follow by zone name
    '''
    def getZoneNode(self, msg):
        Znode = ''
        num , name = self.getNumName(msg.Zone)
        msg.Zone_name = name
        Zaddr = 'zone_{:03}'.format(int(num))
        Znode = self.poly.getNode(Zaddr)
        if not Znode:
            LOGGER.error('poly.getNode failed to find {}'.format(Zaddr))
            raise TypeError('poly.getNode failed to find')
        return Znode
    '''
    Device wil contain 1-3 numeric
    '''
    def getDeviceNode(self, msg):
        Dnode = ''
        num , name = self.getNumName(msg.Device)
        Daddr = 'output_{:03}'.format(int(num))
        Dnode = self.poly.getNode(Daddr)
        if not Dnode:
            LOGGER.error('poly.getNode failed to find {}'.format(Daddr))
            raise TypeError('poly.getNode failed to find')
        return Dnode
 
    '''
    This returns the numeric and namer of the Zone or Area Field
    '''
    def getNumName (self,field):
        Npos = field.find(b'"')
        if Npos == -1:
            num = field[0:]
            name = ''
        else:
            num = field[0:Npos]
            name = field[Npos:]

        return num, name
    
    def sendAck(self):
        self.command = const._MSG_ACK
        self.data = b''
        data = self.serializeResponse()
        LOGGER.debug('Sending ACK')
        self.recv_sock.send(data)
 
    @classmethod
    def deserializeStatus(cls, rawdata):

        if (rawdata[0:-1].find(b'\x26') == -1):
            cmdStart = 14
            minutes = 0
        else:
            cmdStart = 19
            minutes = int(rawdata[15:19].decode())

        command = rawdata[cmdStart:cmdStart+2]
        data = rawdata[cmdStart+2:]
        message = cls('', command, data)
        message.minutes_ago = int(rawdata[15:19].decode())
        return message
        

    @classmethod
    def deserializeReqResp(cls, rawdata):
        command = rawdata[8:11]
        data = rawdata[11:-1]
        message = cls('', command, data)
        LOGGER.debug ('command: {} data: {}'.format(message.command, message.data))
        return message

    @classmethod
    def deserializeCmdResp(cls, rawdata):
        cmdS = 8
        cmdE = 8
        if rawdata[9] == 0x057 or rawdata[9] == 0x05a: #'W' or 'Z'
            cmdE += 3
        else: 
            cmdE += 2
        command = rawdata[cmdS:cmdE]
        data = rawdata[cmdE:-1]
        message = cls('', command, data)

        LOGGER.debug ('command: {} data: {}'.format(message.command, message.data))
        return message

    def parse(self):
        self.Type   = self.getField(b'\\t')
        self.Zone   = self.getField(b'\\z')
        self.Area   = self.getField(b'\\a')
        self.User   = self.getField(b'\\u')
        self.Device = self.getField(b'\\v')
        self.Time   = self.getField(b'\\i')
        self.Holiday= self.getField(b'\\h')
        self.Date   = self.getField(b'\\d')
        self.Equip  = self.getField(b'\\g')
        self.EventQ = self.getField(b'\\e')

        LOGGER.info ('Command:{} Type:{} Area:{} User:{} Device:{} Time:{} Holiday:{} Date:{} Equiptment:{} EventQual:{}'
        .format(self.command, self.Type, self.Zone, self.Area, self.User, self.Device, self.Time, self.Holiday, self.Date, self.Equip, self.EventQ))

    def getField(self, field):
        result = b''
        Spos = self.data[0:].find(field)
        if Spos != -1:
            Spos+=3
            Epos = self.data[Spos:].find(b'\\')
            Epos += Spos
            result = self.data[Spos:Epos]
            LOGGER.debug('Parsed field: {} Data = {} '.format(field,result)) 
            LOGGER.debug('Parsed field: {} = {}  Spos:{}  Epos:{}'.format(field,result,Spos,Epos)) 
            LOGGER.debug('{}'.format(self.data))
        return result
    


