CXX = g++
CFLAGS = -std=c++17 -Wall -O3

PROGS = unigram bigram
UNIGRAM_OBJS = unigram.o
BIGRAM_OBJS = bigram.o

all: $(PROGS)

unigram: $(UNIGRAM_OBJS)
	$(CXX) $(CFLAGS) $^ -o $@

bigram: $(BIGRAM_OBJS)
	$(CXX) $(CFLAGS) $^ -o $@

%.o: %.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@

clean:
	rm $(PROGS) $(UNIGRAM_OBJS) $(BIGRAM_OBJS)
