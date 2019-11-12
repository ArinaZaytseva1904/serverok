import asyncio


class Server(object):
    """Class for storing metrics"""
    def __init__(self):
        self.metrics = dict()

    def put(self, data):
        """Writing metrics to server memory"""
        data = data[4:].split()
        if data[0] not in self.metrics:
            self.metrics[data[0]] = [(data[1], data[2])]
            return 'ok\n\n'
        elif data[0] in self.metrics:
            for i in self.metrics:
                if i == data[0]:
                    if (data[1], data[2]) in self.metrics[data[0]]:
                        return 'ok\n\n'
                    else:
                        self.metrics[data[0]].append((data[1], data[2]))
                        return 'ok\n\n'
                else:
                    pass

    def doing(self):
        """Doing reply for server with all information"""
        reply = 'ok\n'
        for i in self.metrics:
            for j in self.metrics.get(i):
                reply += i + ' ' + j[0] + ' ' + j[1] + '\n'
        return reply

    def making(self, a):
        """Making reply for server by metric"""
        reply = 'ok\n'
        for i in self.metrics:
            if i == a:
                for j in self.metrics.get(a):
                    reply += i + ' ' + j[0] + ' ' + j[1] + '\n'
        return reply

    def get(self, data):
        """Getting metrics from server memory"""
        if len(data[4:].split()) != 1:
            return 'error\nwrong command\n\n'
        if self.metrics is None:
            return 'No data in dict yet'
        if data[:5] == 'get *':
            reply = self.doing()
        else:
            metric = data[4:].strip()
            if metric not in self.metrics:
                return 'ok\n\n'
            else:
                reply = self.making(metric)
        reply += '\n'
        return reply


class ServerProtocol(asyncio.Protocol):
    """Establishing a connection, receiving a data"""

    def connection_made(self, transport):
        """Establishing a connection"""
        self.transport = transport


    def data_received(self, data):
        """receiving a data"""
        self.process_data(data.decode())

    def process_data(self, data):
        """Putting or getting metrics"""
        command = data[:3]

        if command == 'put':
            reply = server.put(data)
        elif command == 'get':
            reply = server.get(data)
        else:
            reply = 'error\nwrong command\n\n'
        reply = reply.encode()
        self.transport.write(reply)


def run_server(host, port):
    """Run coroutine"""
    loop = asyncio.get_event_loop()
    coroutine_server = loop.create_server(ServerProtocol, host, int(port))
    server = loop.run_until_complete(coroutine_server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


server = Server()
run_server('127.0.0.1', 8888)
