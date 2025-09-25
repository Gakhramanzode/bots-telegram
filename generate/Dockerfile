FROM golang:1.24 as builder

ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /build

COPY go.mod .

RUN go mod download

COPY . .

RUN go mod tidy && go build -o main .

FROM alpine:3.21

COPY --from=builder /build/main .

USER nobody

CMD ["./main"]
