import socket
import select
import struct


def main(argv):

    if len(argv) < 3:
        print('Usage: mcast_listener.py (<multicast ip> <multicast port>)+ <local ip>')

    # get ip addresses and ports
    print(argv, [(i, i+1) for i in range(0, len(argv)-1, 2)])
    mcast_ip_ports = [(argv[i], int(argv[i+1]))
                      for i in range(0, len(argv)-1, 2)]
    local_ip = argv[-1]

    epoll = select.epoll()
    for mcast_ip, port in mcast_ip_ports:
        mcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # set reuse port
        mcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Bind to the server address
        mcast_sock.bind((mcast_ip, port))

        # Tell the operating system to add the socket to the multicast group
        # on local ip interface
        mreq = struct.pack('4s4s', socket.inet_aton(
            mcast_ip), socket.inet_aton(local_ip))
        mcast_sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Register the socket to epoll
        epoll.register(mcast_sock.fileno(), select.EPOLLIN)

        # Set the socket to non-blocking
        mcast_sock.setblocking(0)

        # Print the information
        print("Listening to multicast {}:{} on local ip {}".format(
            mcast_ip, port, local_ip))

    # Run the event loop
    while (True):
        events = epoll.poll(1)
        for _, event in events:
            if event == select.EPOLLIN:
                data, addr = mcast_sock.recvfrom(1024)
                print("Received data from {}: {}".format(addr, data))


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
