package main

import (
    "net"
    "net/rpc"
)

func StartServer() {
    listener, _ := net.Listen("tcp", ":3000")
    defer listener.Close()
    rpc.Accept(listener)
}
