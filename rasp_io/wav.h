/* wav.h
 */

#include <stdio.h>
#include <assert.h>

#define FS 44100
 
#ifndef WAV_H
#define WAV_H
 
void write_wav(char * filename, unsigned long num_samples, short int * data, int s_rate);
    /* open a file named filename, write signed 16-bit values as a
        monoaural WAV file at the specified sampling rate
        and close the file
    */
 
#endif