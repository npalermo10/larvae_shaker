## to install you need to run "sudo apt-get install -y python3-dev libasound2-dev" then install the module "sudo pip3 install simpleaudio"


import simpleaudio as sa
import time
import os
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

b4_shake_pin = 13
post_shake_pin = 19
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

note_freq = 100 ## in hz
play_duration = 2
## given in seconds (as float)
wait_time = 60 ## minutes wait between tones. Will not work if random_wait is true
random_wait = 0 ## if true (1) here then give random min and max minutes wait
rand_min_wait = 10 ## in minutes
rand_max_wait = 60 ## in minutes
total_time = 120 ## total run time of experiment given in 

save_dir = "./shaker_stim_info/"  ##where to save data

def writefile(filename, freq, duration):
    f=open(filename,"a")
    f.write("{}, {}, {}, {}\n".format(time.strftime('%H:%M:%S'), time.time(), freq, duration))
    f.close()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
T = play_duration
t = np.linspace(0, T, T * sample_rate, False)
audio = np.sin(note_freq * t * 2 * np.pi)
# normalize to 16-bit range
audio *= 32767 / np.max(np.abs(audio))
# convert to 16-bit data
audio = audio.astype(np.int16)

GPIO.output(b4_shake_pin, GPIO.HIGH)
time.sleep(1)
GPIO.output(b4_shake_pin, GPIO.LOW)
print("played on {}".format(time.asctime( time.localtime(time.time()))))
play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
file_name=(time.strftime('%Y_%m_%d.txt'))
file_name= save_dir + file_name
writefile(file_name, note_freq, play_duration)
last_play = time.time()
play_obj.wait_done()
GPIO.output(post_shake_pin, GPIO.HIGH)
time.sleep(60)
GPIO.output(post_shake_pin, GPIO.LOW)
        
start_time = time.time() ##time recorded as seconds since epoch
last_play = time.time()
running = True
while running:
    if random_wait:
        wait_time = randint(rand_min_wait, rand_max_wait+1)

    # start playback
    if time.time() - last_play >= wait_time*60:
        GPIO.output(b4_shake_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(b4_shake_pin, GPIO.LOW)
        print("played on {}".format(time.asctime( time.localtime(time.time()))))
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        file_name=(time.strftime('%Y_%m_%d.txt'))
        file_name= save_dir + file_name
        writefile(file_name, note_freq, play_duration)
        last_play = time.time()
        play_obj.wait_done()
        GPIO.output(post_shake_pin, GPIO.HIGH)
        time.sleep(60)
        GPIO.output(post_shake_pin, GPIO.LOW)
        
    if time.time() - start_time >= total_time*60:
        running = False
print("end")
