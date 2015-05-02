#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   udptun.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os
import time
import json
import errno
import fcntl
import struct
import socket
import select
import hashlib
import logging
import threading
import traceback


def inet_aton(a):
    return struct.unpack('!I', socket.inet_aton(a))[0]


def inet_ntoa(n):
    return socket.inet_ntoa(struct.pack('!I', n))


def fmt_packet(packet):
    src = socket.inet_ntoa(packet[16:20])
    dst = socket.inet_ntoa(packet[20:24])
    return '%s %s=>%s' % (repr(packet[:4]), src, dst)


def catch_exc_detail(func):
    def execute(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.error("%s(%s, %s): %s" % (func.__name__, args, kwargs, 
                traceback.format_exc()))
    return execute


class Tunnel(object):

    TUN_SET_IFF = 0x400454ca
    TUN_IFF = 0x0001
    TUN_MTU = 1480 - 20 - 8 - 4
    BUFFER_SIZE = 8192

    def __init__(self, ip=None):
        try:
            self.fd = os.open('/dev/net/tun', os.O_RDWR)
        except:
            self.fd = os.open('/dev/tun', os.O_RDWR)

        data = struct.pack('16sH', 't%d', self.TUN_IFF)
        ifs = fcntl.ioctl(self.fd, self.TUN_SET_IFF, data)
        self.name = ifs[:16].strip('\x00')

        os.system('ip link set %s up' % (self.name,))
        os.system('ip link set %s mtu %s' % (self.name, self.TUN_MTU))

        self.ip = None
        self.set_ip(ip)

    def set_ip(self, ip):
        if ip == self.ip:
            return

        if self.ip:
            cmd = 'ip addr del %s dev %s' % (self.ip, self.name)
            os.system(cmd)
            if __debug__:
                logging.warn('[CMD] %s' % (cmd,))

        self.ip = ip
        if self.ip:
            cmd = 'ip addr add %s dev %s' % (self.ip, self.name)
            os.system(cmd)
            if __debug__:
                logging.warn('[CMD] %s' % (cmd,))

    def setblocking(self, block):
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        if block:
            flags &= ~os.O_NONBLOCK
        else:
            flags |= os.O_NONBLOCK
        fcntl.fcntl(self.fd, fcntl.F_SETFL, flags)

    def fileno(self):
        return self.fd

    def read(self):
        return os.read(self.fd, self.BUFFER_SIZE)

    def write(self, packet):
        return os.write(self.fd, packet)


class EpollServerMixin(object):

    def setup(self, timeout=1):
        self.timeout = timeout
        self.epoll = select.epoll()
        self.callbacks = {}

    def register_callback(self, f, callback):
        self.epoll.register(f, select.EPOLLIN)
        self.callbacks[f.fileno()] = callback

    def serve_forever(self):
        while True:
            try:
                actives = self.epoll.poll(timeout=self.timeout)
            except IOError as err:
                continue

            for fileno, event in actives:
                self.callbacks[fileno]()


class UdpTunnel(EpollServerMixin):

    BUFFER_SIZE = 8192

    def __init__(self, ip=None):
        super(UdpTunnel, self).setup()

        self.tun = Tunnel(ip)
        self.tun.setblocking(False)

        from socket import socket, AF_INET, SOCK_DGRAM
        self.udp = socket(AF_INET, SOCK_DGRAM)
        self.udp.setblocking(False)

        self.register_callback(self.tun, self.on_tun_active)
        self.register_callback(self.udp, self.on_udp_active)

    def cal_token(self, data, key, __sort__=lambda x, y: cmp(x[0], y[0])):
        items = [(str(k), str(v)) for k, v in data.iteritems()]
        items.sort(__sort__)
        raw = ''.join([v for k, v in items]) + key
        return hashlib.md5(raw).hexdigest()

    @catch_exc_detail
    def call(self, __peer__, __method__, __key__, **kwargs):
        if __debug__:
            logging.debug('call %s at %s with %s: %s' % \
                    (__method__, __peer__, __key__, kwargs))
        kwargs['__method__'] = __method__
        kwargs['__token__'] = self.cal_token(kwargs, __key__)
        self.udp.sendto(json.dumps(kwargs), __peer__)

    def on_call(self, peer, packet):
        data = json.loads(packet)
        key = self.get_key(peer, data)
        if not key:
            return

        token = data.pop('__token__', None)
        if not token:
            return

        if token != self.cal_token(data, key):
            return

        method = data.pop('__method__', None)
        if not method:
            return

        self.do_call(peer, method, data)

    def on_tun_active(self):
        while True:
            try:
                packet = self.tun.read()
            except OSError as err:
                if err.errno == errno.EAGAIN:
                    break
                elif err.errno == errno.INTR:
                    continue
                raise

            self.send_tun_packet(packet)

    def on_udp_active(self):
        while True:
            try:
                packet, peer = self.udp.recvfrom(self.BUFFER_SIZE)
            except IOError as err:
                if err.errno == errno.EAGAIN:
                    break
                elif err.errno == errno.INTR:
                    continue
                raise

            if packet[0] == '{':
                self.on_call(peer, packet)
            else:
                self.send_udp_packet(packet)


class UdpTunnelServer(UdpTunnel):

    def __init__(self, ip='10.188.0.1/16', addr=':18800', conf='conf.py'):
        super(UdpTunnelServer, self).__init__(ip)

        self.conf = conf

        ip, netbits = ip.split('/')
        self.ip = inet_aton(ip)
        self.netbits = int(netbits)
        self.mask = ~(2 ** (32 - self.netbits) - 1)
        self.network = self.ip & self.mask

        addr, port = addr.split(':')
        addr = (addr, int(port))
        self.udp.bind(addr)

        self.route = {}

        t = threading.Thread(target=self.update_conf_forever)
        t.setDaemon(True)
        t.start()

    def update_conf_forever(self):
        while True:
            self.update_conf()
            time.sleep(1)

    def update_conf(self):
        conf = {}
        execfile(self.conf, conf)

        self.keys = conf.get('keys')
        self.user_index = conf.get('user_index')

    def get_key(self, peer, data):
        return self.keys.get(data.get('user'))

    def do_call(self, peer, method, kwargs):
        method = getattr(self, method, None)
        if not method:
            return
        method(peer, **kwargs)

    def register(self, peer, user):
        index = self.user_index.get(user)
        if not index:
            if __debug__:
                logging.warn('register ignore %s from %s' % (user, peer))
            return

        ip = self.network + index
        self.route[ip] = peer
        ip = '%s/%s' % (inet_ntoa(ip), self.netbits)
        self.call(peer, 'set_ip', self.keys.get(user), ip=ip)
        if __debug__:
            logging.info('register user %s from %s with %s' % (user, peer, ip))

    @catch_exc_detail
    def send_tun_packet(self, packet):
        dst = struct.unpack('!I', packet[20:24])[0]
        peer = self.route.get(dst)
        if peer:
            self.udp.sendto(packet, peer)
            if __debug__:
                logging.debug('send to udp %s: %s' % \
                        (peer, fmt_packet(packet)))

    @catch_exc_detail
    def send_udp_packet(self, packet):
        dst = struct.unpack('!I', packet[20:24])[0]
        if dst == self.ip:
            self.tun.write(packet)
            if __debug__:
                logging.debug('send to tun: %s' % \
                        (fmt_packet(packet),))
        elif dst & self.mask == self.network:
            peer = self.route.get(dst)
            if peer:
                self.udp.sendto(packet, peer)
                if __debug__:
                    logging.debug('send to udp %s: %s' % \
                            (peer, fmt_packet(packet)))
        else:
            self.tun.write(packet)


class UdpTunnelClient(UdpTunnel):

    def __init__(self, addr='vpn.icampus.us:18800', user='guest', key='asdf'):
        super(UdpTunnelClient, self).__init__()

        self.user = user
        self.key = key

        addr, port = addr.split(':')
        self.peer = (addr, int(port))

        t = threading.Thread(target=self.register_forever)
        t.setDaemon(True)
        t.start()

    def get_key(self, peer, data):
        return self.key

    def register_forever(self):
        while True:
            self.register(user=self.user)
            time.sleep(1)

    def register(self, user='guest'):
        self.call(self.peer, 'register', self.key, user=user)

    def do_call(self, peer, method, kwargs):
        method = getattr(self, method, None)
        if not method:
            return
        method(**kwargs)

    def set_ip(self, ip):
        self.tun.set_ip(ip)

    @catch_exc_detail
    def send_tun_packet(self, packet):
        self.udp.sendto(packet, self.peer)
        if __debug__:
            logging.debug('send to udp %s: %s' % \
                    (self.peer, fmt_packet(packet),))

    def send_udp_packet(self, packet):
        self.tun.write(packet)
        if __debug__:
            logging.debug('send to tun %s' % (fmt_packet(packet),))


def main():
    logging.basicConfig(level=logging.DEBUG)

    from optparse import OptionParser
    usage = 'usage: %prog -m server|client [-a addr:port] [-u user] [-k key]'
    parser = OptionParser(usage=usage)
    parser.add_option('-a', '--address', dest='addr', help='server address')
    parser.add_option('-c', '--config', dest='conf', help='config file')
    parser.add_option('-k', '--key', dest='key', help='key')
    parser.add_option('-m', '--mode', dest='mode', help='mode')
    parser.add_option('-n', '--net', dest='net', help='net')
    parser.add_option('-u', '--user', dest='user', help='user')

    options, args = parser.parse_args()
    if options.mode == 'client':
        UdpTunnelClient(addr=options.addr, user=options.user,
                key=options.key).serve_forever()
    elif options.mode == 'server':
        UdpTunnelServer(ip=options.net, addr=options.addr,
                conf=options.conf).serve_forever()
    else:
        parser.error('mode should be specified')
        parser.print_help()


if __name__ == '__main__':
    main()
