#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <fcntl.h>
#include <errno.h>
#include <termios.h> 
#include <unistd.h>

#include "wav.h"

#define READ_SIZE 255
#define WAV_SIZE 230400
#define BYTE_MAX 500000