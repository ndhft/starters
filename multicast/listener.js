import dgram from "dgram";

const main = (args) => {
  if (args.length < 3) {
    console.log(
      "Usage: node mcast_listener.js (<multicast ip> <multicast port>)+ <local ip>"
    );
    return;
  }

  // Parse multicast IPs and ports
  const mcastIpPorts = args.slice(0, -1).reduce((acc, val, i, arr) => {
    if (i % 2 === 0) acc.push({ mcastIp: val, port: parseInt(arr[i + 1], 10) });
    return acc;
  }, []);
  const localIp = args.at(-1);

  // Create sockets for each multicast group
  mcastIpPorts.forEach(({ mcastIp, port }) => {
    const socket = dgram.createSocket({ type: "udp4", reuseAddr: true });

    socket.on("error", (err) => {
      console.error(`Socket error: ${err.message}`);
      socket.close();
    });

    socket.on("message", (msg, rinfo) => {
      console.log(
        `Received data from ${rinfo.address}:${rinfo.port} - ${msg.toString()}`
      );
    });

    socket.bind(port, () => {
      // Join the multicast group
      socket.addMembership(mcastIp, localIp);

      console.log(
        `Listening to multicast ${mcastIp}:${port} on local ip ${localIp}`
      );
    });
  });
};

// Run the main function
const args = process.argv.slice(2);
main(args);
