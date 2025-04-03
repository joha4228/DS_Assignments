package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"regexp"
	"sort"
	"strings"

	pb "go_server1/go_protos"

	"google.golang.org/grpc"
)

// Define global variables like this so that it is possible for the user to provide
// the values via the command line when running the program.
//
//	flag.Type("flagname", default_value, "help_message/flag_explaination")
var (
	port = flag.Int("port", 9000, "The server port")
)

// 'freqCountService' is used to implement the frequencyCalculater service.
type freqCountService struct {
	pb.FrequencyCalculatorServer
	//lock sync.Mutex // Mutual exclusion lock (not necesarry anyway, since there's no shared resources)
}

// https://benhoyt.com/writings/count-words/#other-languages
func (s *freqCountService) Calculate(ctx context.Context, t *pb.Textk) (*pb.WordCountList, error) {
	text := t.GetText()
	log.Printf("Recieved:\n%v", text) // %v prints the value of an argument in its default format.
	// Take out characters that are not letters or spaces.
	text = regexp.MustCompile(`[^a-zA-Z\s]+`).ReplaceAllString(text, "")
	words := strings.Fields(text) // convert to array; works like strings.Split but uses only space as seperator.
	wordMap := make(map[string]int32)
	for _, word := range words {
		if _, exists := wordMap[word]; exists { // Use _ bc we are only interested in the bool, i.e. if the key exists or not.
			word := strings.ToLower(word)
			wordMap[word]++
		} else {
			wordMap[word] = 1
		}

	}
	var wordfreqs = make([]*pb.WordCount, 0)

	for w, c := range wordMap {
		wc := &pb.WordCount{Word: w, Count: c}
		wordfreqs = append(wordfreqs, wc)
	}

	response := &pb.WordCountList{
		WordCounts: wordfreqs,
	}

	log.Printf("Returning:\n%v", response)
	return response, nil
}

func (s *freqCountService) Combine(stream pb.FrequencyCalculator_CombineServer) error {
	combined := make(map[string]int32)

	for {
		wc, err := stream.Recv()
		if err == io.EOF {
			// End of stream has been reached. Return the WordCounList sorted.
			sorted := sortMapByValue(combined)
			response := &pb.WordCountList{
				WordCounts: sorted,
			}
			log.Printf("Returning:\n%v", response)
			return stream.SendAndClose(response)
		}
		if err != nil {
			// Error reading from stream.
			return err
		}
		log.Printf("Recieved:\n%v", wc)
		// Add incomming WordCount elements to map
		combined[wc.Word] += wc.Count
	}
}

func sortMapByValue(m map[string]int32) []*pb.WordCount {
	// convert to list for sorting
	var entries []*pb.WordCount
	for k, v := range m {
		entry := &pb.WordCount{Word: k, Count: v}
		entries = append(entries, entry)
	}

	sort.Slice(entries, func(i, j int) bool {
		return entries[i].Count > entries[j].Count
	})

	return entries
}

func main() {
	flag.Parse() // Make the values of the flags available to main().

	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	server := &freqCountService{}                            // Create instance of freqCountService
	pb.RegisterFrequencyCalculatorServer(grpcServer, server) // Register server with the gRPC server
	// Start the server with .Serve()
	log.Printf("Waiting for requests...")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %s", err)
	}

}
