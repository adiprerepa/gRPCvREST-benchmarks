package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

const (
	url = "192.168.88.143"
	grpcPort = 8888
	restPort = 8080
)

func upload_rest_chunked(fileName string, chunkSize int64) {
	// client := &http.Client{}
	// req, err := http.NewRequest(http.MethodPut, url + "/upload-file", 

	file, err := os.Open(fileName)

	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	
	reader := bufio.NewReader(f)
	buf := make([]byte, 1024)
	for {
		n, err := reader.Read(buf)
		if err != nil {
			if err != io.EOF {
				log.Fatal(err)
			}
			break
		}
		fmt.Print(string(buf[0:n]))
	}
}

func main() {

}
