#include "microphone.h" 




struct termios tty;

int main(int argc, char* argv[])
{
    int serial_port = open("/dev/ttyACM0", O_RDWR);

    if(serial_port < 0)
    {
        printf("Error %i from open: %s\n", errno, strerror(errno));
    }

    if(tcgetattr(serial_port, &tty) != 0) 
    {
        printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
    }   

    tty.c_cflag &= ~PARENB; // Clear parity bit, disabling parity (most common)
    tty.c_cflag &= ~CSTOPB; // Clear stop field, only one stop bit used in communication (most common)
    tty.c_cflag &= ~CSIZE; // Clear all the size bits, then use one of the statements below
    tty.c_cflag |= CS8; // 8 bits per byte (most common)
    //tty.c_cflag &= ~; // Disable RTS/CTS hardware flow control (most common)
    tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)
    tty.c_lflag &= ~ICANON;
    tty.c_lflag &= ~ECHO; // Disable echo
    tty.c_lflag &= ~ECHOE; // Disable erasure
    tty.c_lflag &= ~ECHONL; // Disable new-line echo
    tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
    tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes
    tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
    tty.c_oflag &= ~ONLCR; // Prevent conversion of newline to carriage return/line feed
    // tty.c_oflag &= ~OXTABS; // Prevent conversion of tabs to spaces (NOT PRESENT IN LINUX)
    // tty.c_oflag &= ~ONOEOT; // Prevent removal of C-d chars (0x004) in output (NOT PRESENT IN LINUX)
    tty.c_cc[VTIME] = 100;    // Wait for up to 1s (10 deciseconds), returning as soon as any data is received.
    tty.c_cc[VMIN] = 255;
    // Set in/out baud rate to be 1152000
    cfsetispeed(&tty, B115200);
    cfsetospeed(&tty, B115200);

    // Save tty settings, also checking for error
    if (tcsetattr(serial_port, TCSANOW, &tty) != 0) {
        printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
    }

    // Allocate memory for read buffer, set size according to your needs
    
    char final_read[READ_SIZE] = { 0 };
    int cursor = 0;

    // Read bytes. The behaviour of read() (e.g. does it block?,
    // how long does it block for?) depends on the configuration
    // settings above, specifically VMIN and VTIME
    int n;
    FILE* fptr = fopen("micbytes", "wb");

    while(cursor < BYTE_MAX)
    {
        n = read(serial_port, final_read, READ_SIZE);
        fwrite(&final_read, n, n, fptr);
        cursor += n; 
    }

    fclose(fptr);

    close(serial_port);

}