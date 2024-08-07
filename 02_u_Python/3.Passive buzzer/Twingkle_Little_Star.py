from machine import Pin, PWM
import utime

# Init Buzzer PWM
buz = PWM(Pin(13))
buz.duty_u16(int(65536/2)) # Duty = 50%

Note_Freqs = {'Do_0':523, 'Re_0':587, 'Mi_0':659, 'Fa_0':698, \
              'Sol_0':783, 'La_0':880, 'Ti_0':987, 'Do_1':1046,\
              'Re_1':1174, 'Mi_1':1318, 'Fa_1':1397, 'Sol_1':1568,\
              'La_1':1760, 'Ti_0':1975, 'Do_2':2093}

Twingkle_Little_Star = [['Do_0',0.5], ['Do_0',0.5], ['Sol_0',0.5], ['Sol_0',0.5], \
                        ['La_0',0.5], ['La_0',0.5], ['Sol_0',1], \
                        ['Fa_0',0.5], ['Fa_0',0.5], ['Mi_0',0.5], ['Mi_0',0.5],\
                        ['Re_0',0.5], ['Re_0',0.5], ['Do_0',1],\
                        ['Sol_0',0.5],['Sol_0',0.5],['Fa_0',0.5],['Fa_0',0.5],\
                        ['Mi_0',0.5], ['Mi_0',0.5], ['Re_0',1],\
                        ['Sol_0',0.5],['Sol_0',0.5],['Fa_0',0.5],['Fa_0',0.5],\
                        ['Mi_0',0.5], ['Mi_0',0.5], ['Re_0',1],\
                        ['Do_0',0.5], ['Do_0',0.5], ['Sol_0',0.5], ['Sol_0',0.5], \
                        ['La_0',0.5], ['La_0',0.5], ['Sol_0',1], \
                        ['Fa_0',0.5], ['Fa_0',0.5], ['Mi_0',0.5], ['Mi_0',0.5],\
                        ['Re_0',0.5], ['Re_0',0.5], ['Do_0',1]]

def pNote(freq, len):
    buz.freq(freq)
    utime.sleep(len)
    buz.deinit()
    utime.sleep(0.02)

def pMusic(music):
    for note, l in music:
        pNote(Note_Freqs[note], l)
    
if __name__ == '__main__' :
    pMusic(Twingkle_Little_Star)