import socket
from select import *
import argparse

class simple_server:
    
    def __init__(self):
        self.bufsize = 1024
        self.counter = 0
    def run(self, ip, port):
        # Parse command line arguments
        # host and port are parsed from command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', type=str, default='localhost', help='IP address')
        parser.add_argument('--port', type=int, default=10000, help='Port number')
        args = parser.parse_args()
        ip = args.host
        port = args.port

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to an IP address and a port
        server_socket.bind((ip, port))
        # Listen for incoming connections
        server_socket.listen(5) # Maximum number of queued connections
        print(f"Server is listening on {ip}:{port}")

        socketList = [server_socket]
        while True:
            try:
                read_sockets, write_socket, error_socket = select(socketList, [], [], 1)

                for sock in read_sockets:
                    if sock == server_socket:
                        # Accept a connection
                        # server_socket is a new socket object representing the client connection
                        client_socket, addr = server_socket.accept()
                        print(f"Connected by{addr[0]}:{addr[1]}")
                        socketList.append(client_socket)
                    else:
                        # Receive data from the client
                        try:                            
                            # Receive data from the client
                            data = sock.recv(self.bufsize)
                            if not data:
                                break
                            print(f"--------------------------------------------------------")
                            print(f"Received: \n{data.decode()}")
                            print(f"--------------------------------------------------------")
                            ipaddr = addr[0]+":"+str(addr[1])
                            
                            # Construct the response message
                            res_body = '''<html><head><title>simple web server</title>
                            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
                            <script>'''.encode("utf-8")
                            res_body += f'''
                                var ip = '{ip}'
                                var port = {port}
                                    '''.encode("utf-8")
                            res_body += '''console.log('javascript');
                                function btn(){
                                    Swal.fire({
                                        title: "<strong>HTML <u>example</u></strong>",
                                        icon: "info",
                                        html: `
                                            You can use <b>bold text</b>,
                                            <a href="#" autofocus>links</a>,
                                            and other HTML tags<br>
                                            <span class="badge text-bg-primary">Primary</span>
                                            <span class="badge text-bg-secondary">Secondary</span>
                                            <span class="badge text-bg-success">Success</span>
                                            <span class="badge text-bg-danger">Danger</span>
                                            <span class="badge text-bg-warning">Warning</span>
                                            <span class="badge text-bg-info">Info</span>
                                            <span class="badge text-bg-light">Light</span>
                                            <span class="badge text-bg-dark">Dark</span>
                                        `,
                                        showCloseButton: true,
                                        showCancelButton: true,
                                        focusConfirm: false,
                                        confirmButtonText: `
                                            <i class="fa fa-thumbs-up"></i> Great!
                                        `,
                                        confirmButtonAriaLabel: "Thumbs up, great!",
                                        cancelButtonText: `
                                            <i class="fa fa-thumbs-down"></i>
                                        `,
                                        cancelButtonAriaLabel: "Thumbs down"
                                    });
                                }
                                function btn2(){
                                    Swal.fire({
                                        position: "top-end",
                                        icon: "success",
                                        title: "Your work has been saved",
                                        showConfirmButton: false,
                                        timer: 1500
                                    });
                                }
                                // get
                                function btn_fetch(){
                                    var url = 'http://'+ip+':'+port+'/show?time1=value1&time2=value2'
                                    fetch(url)
                                    .then(response => console.log(response))
                                }
                                // post
                                function btn_fetch2(){
                                    var url = 'http://'+ip+':'+port+''
                                    fetch(url, {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({
                                            "name": "John Doe",
                                            "age": 30,
                                            "city": "New York"
                                        }),                                   
                                    })
                                    .then(response => console.log(response))
                                    .then((data) => {console.log(data)})
                                }
                                // ajax
                                function btn_ajax(){
                                    Swal.fire({
                                        title: "Submit your Github username",
                                        input: "text",
                                        inputAttributes: {
                                            autocapitalize: "off"
                                        },
                                        showCancelButton: true,
                                        confirmButtonText: "Look up",
                                        showLoaderOnConfirm: true,
                                        preConfirm: async (login) => {
                                            try {
                                            const githubUrl = `
                                                https://api.github.com/users/${login}
                                            `;
                                            const response = await fetch(githubUrl);
                                            if (!response.ok) {
                                                return Swal.showValidationMessage(`
                                                ${JSON.stringify(await response.json())}
                                                `);
                                            }
                                            return response.json();
                                            } catch (error) {
                                            Swal.showValidationMessage(`
                                                Request failed: ${error}
                                            `);
                                            }
                                        },
                                        allowOutsideClick: () => !Swal.isLoading()
                                        }).then((result) => {
                                        if (result.isConfirmed) {
                                            Swal.fire({
                                            title: `${result.value.login}'s avatar`,
                                            imageUrl: result.value.avatar_url
                                            });
                                        }
                                    });
                                }
                            </script>
                            </head>
                            <body>
                            hello world!<br>'''.encode("utf-8")
                            res_body += f'''
                            <p>Connected from: {ipaddr}</p>
                            <h2>Counter: {self.counter}</h2>
                            <button type="button" class="btn btn-primary" onclick="btn();">HTML Exam</button>
                            <button type="button" class="btn btn-outline-danger" onclick="btn2();">saved</button>
                            <button type="button" class="btn btn-warning" onclick="btn_ajax();">ajax</button>
                            <button type="button" class="btn btn-outline-info" onclick="btn_fetch();">fetch get</button>
                            <button type="button" class="btn btn-outline-danger" onclick="btn_fetch2();">fetch post</button>
                            </body>
                            </html>'''.encode("utf-8")
                            
                            # Construct the response header
                            res_header = (
                                "HTTP/1.1 200 OK",
                                "Server: Simple Server",
                                "Content-Length: "+str(len(res_body)),                
                                "Content-Type: text/html",
                                "\n")
                            
                            # Combine the header and body into a single response message
                            res_header = "\n".join(res_header).encode("utf-8")            
                            result = res_header + res_body

                            print(f"--------------------------------------------------------")
                            print(f"Response msg: \n{result}")
                            print(f"--------------------------------------------------------")

                            # Send data back to the client
                            # client_socket.sendall(f"Counter: {self.counter}".encode())
                            sock.sendall(result)
                            # Close the connection
                            sock.close()
                            socketList.remove(sock)
                        except Exception as e:
                            print(f"Error: {str(e)}")
                            sock.close()
                            socketList.remove(sock)
            except KeyboardInterrupt as e:
                print(f"Error: {str(e)}")
                server_socket.close()
                break

        print("Server is shutting down")
        # Close the server socket
        server_socket.close()
server = simple_server()
server.run('', 0)