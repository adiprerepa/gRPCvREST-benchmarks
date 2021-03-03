package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"time"
)

const (
	url = "192.168.88.143"
	grpcPort = 8888
	restPort = 8080
)

func uploadRestChunked(fileName string, chunkSize int64) {
	// client := &http.Client{}
	// req, err := http.NewRequest(http.MethodPut, url + "/upload-file", 

	f, err := os.Open(fileName)

	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	
	reader := bufio.NewReader(f)
	buf := make([]byte, chunkSize)
	start := time.Now()
	for {
		_, err := reader.Read(buf)
		if err != nil {
			if err != io.EOF {
				log.Fatal(err)
			}
			break
		}
		//fmt.Print(string(buf[:n]))
	}
	elapsed := time.Now().Sub(start)
	fmt.Printf("elapsed %+v", elapsed)
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("please include file name")
		return
	}
	uploadRestChunked(os.Args[1], 512)
}
