package main

import (
    "errors"
)

type Response struct {
    Message string
}

type Request struct {
    Name string
}

type Handler struct {}

func (h *Handler) Execute(req Request, res *Response) (err error) {
    if req.Name == "" {
        err = errors.New("Name is required")
        return
    }

    res.Message = "Got you, " + req.Name
    return
}
