package main

import (
    "net/rpc"
)

func StartClient(addr string) {
    client, _ := rpc.Dial("tcp", addr)
    defer client.Close()
}
