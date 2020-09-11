CC ?= cc
CFLAGS += -Wno-all -O3 -march=native
LDFLAGS = -lm

all: program

program: perfectly_commented.c Makefile
	$(CC) $(CFLAGS) $(LDFLAGS) -o program perfectly_commented.c

test: program
	./program 100

time: program
	time ( ./program 100000000 > /dev/null )

.PHONY: all
