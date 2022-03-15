"""
TRANH201INFO3 sequencer test code
"""

# import gpiozero
import time
import sys

# from Step import Step #Step class
from LCDSequencer import LCDSequencer #LCD class
from Simulatelcd import Simulatelcd #Simulated LCD class, for testing purposes and/or when not running on a RPi
# from DACSequencer import DACSequencer #DAC class
# from RotaryEncoder import RotaryEncoder #Rotary encoder class
# TODO from ClockSequencer import ClockSequencer # Clock class
# from LEDSequence import LEDSequence #LEDs Sequence class (8 LEDs)
from Sequencer import Sequencer
from Tempo import Tempo
from Gate import Gate
from Env import SIMULATED_LCD, SIMULATED_DAC


def main(): # Main function, activated when sequencer launched
    
    global sequencer
    sequencer = Sequencer()
    global lcd
    if SIMULATED_LCD:
        lcd = Simulatelcd()
    else:
        lcd = LCDSequencer()
    lcd.toggleBacklight(True)
    #lcd.test()
    #time.sleep(5)
    
    global tempo
    tempo = Tempo(60, lcd) # initial tempo is 60 bpm
    global gate
    gate = Gate(sequencer.dac2, 0, lcd)
    
    #init_tempo = tempo.value
    #lcd.displayTempo(init_tempo)
    init_step = sequencer.noteSequence.step
    init_pitch = sequencer.noteSequence.note[sequencer.noteSequence.listSteps[sequencer.noteSequence.step][1]]
    init_octave = sequencer.noteSequence.listSteps[sequencer.noteSequence.step][0]
    lcd.displayStep(init_step, init_pitch, init_octave)

    '''
    note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    l_steps = []
    for i in range(8): #création de la liste des notes
        l_steps.append([0, 1]) #cette liste représente l'octave 0 et la note 1
    '''

    '''
    def increase_pitch():
        print("test increase pitch")
    def decrease_pitch():
        print("test decrease pitch")
    sequencer.buttonIncrOct.when_pressed = increase_pitch # TODO ?
    sequencer.buttonDecrOct.when_pressed = decrease_pitch # TODO ?
    '''
    
    #* sequencer.button1.when_pressed = ?.on # TODO
    sequencer.buttonIncrOct.when_pressed = sequencer.noteSequence.increaseOctave #?
    #!sequencer.buttonDecrOct.when_pressed = sequencer.noteSequence.decreaseOctave #?
    sequencer.buttonDecrOct.when_pressed = sequencer.noteSequence.increasePitch #!
    #* sequencer.buttonHearNote.when_pressed = sequencer.playNote

    sequencer.rotorPitch.when_rotated_clockwise = sequencer.noteSequence.increasePitch
    sequencer.rotorPitch.when_rotated_counter_clockwise = sequencer.noteSequence.decreasePitch
    sequencer.rotorTempo.when_rotated_clockwise = tempo.increaseTempo
    sequencer.rotorTempo.when_rotated_counter_clockwise = tempo.decreaseTempo
    #* sequencer.rotorGate.when_rotated_clockwise = gate.increaseGate # TODO
    #* sequencer.rotorGate.when_rotated_counter_clockwise = gate.decreaseGate # TODO
    sequencer.rotorCV1.when_rotated_clockwise = sequencer.cv1.increaseCV
    sequencer.rotorCV1.when_rotated_counter_clockwise = sequencer.cv1.decreaseCV
    sequencer.rotorCV2.when_rotated_clockwise = sequencer.cv2.increaseCV
    sequencer.rotorCV2.when_rotated_counter_clockwise = sequencer.cv2.decreaseCV
    sequencer.rotorCV3.when_rotated_clockwise = sequencer.cv3.increaseCV
    sequencer.rotorCV3.when_rotated_counter_clockwise = sequencer.cv3.decreaseCV
    sequencer.rotorStep.when_rotated_clockwise = sequencer.noteSequence.increaseStep
    sequencer.rotorStep.when_rotated_counter_clockwise = sequencer.noteSequence.decreaseStep

    # sequence led, sequence gate send following tempo

    ''' for testing :
    for p in range (10): # does the step sequence 10 times
        for i in range(0,7):
            #* gate.sendGateSignal(tempo)
            pitchDAC = 4096*(l_steps[i][1]/12) # need to add octaves
            sequencer.dac1.setVoltage(0, pitchDAC)
            time.sleep(60/tempo.value)
    '''
    #gpiozero.pause()
    #time.sleep(15)
    #raise SystemExit
    
    #lcd.clearRightLCD()
    while True: # works at the same time as the rotary encoders are turning and changing values
        print("testing")
        time.sleep(3)


def endSequencer():
    # Set the DACs to 0V and turns the LCD backlight off (executed when keyboard interrupt or other)
    global sequencer
    #sequencer = Sequencer() # ?
    global lcd
    #lcd = Simulatelcd() # ?
    for i in range(2):
        sequencer.dac1.setVoltage(i, 0)
        sequencer.dac2.setVoltage(i, 0)
        sequencer.dac3.setVoltage(i, 0)
    lcd.fullClearLCD()
    lcd.toggleBacklight(False)


if __name__ == "__main__":
    # launch main() if this file is launched (SequencerMain.py)
    try:
        main()
    except (KeyboardInterrupt, SystemExit):  # catches a keyboard interrupt
        print("Keyboard interrupt, stopping sequencer")
    finally:
        endSequencer() # stops the sequencer
        sys.exit(0)



'''
class Tempo: # needs to be changed ?
    # Tempo
    def __init__(self, current_tempo):
        self.current_tempo = current_tempo
    def changeTempo(self, new_tempo):
        self.current_tempo=new_tempo

class Clock: # needs to be changed
    # Clock
    def __init__(self):
        pass
    def ticking(self, tempo):
        print("tick")
        clock=0
        #time.sleep(60/self.tempo.current_tempo)
        #send a clock signal
        print("tack")
        clock=1
        time.sleep(60/tempo.current_tempo)
'''

'''
    # End of program:
    sequencer.dac1.setVoltage(0, 0)
    sequencer.dac2.setVoltage(0, 0)
    sequencer.dac3.setVoltage(0, 0)
    lcd.toggleBacklight(False)
'''

'''
    lcd = Simulatelcd() # initialization of a simulated LCD, to use when running the program outside of a RPi, it will just print out rather than display on the LCD
    #lcd = LCDSequencer.LCDSequencer() # LCD initialization
    tempo = Tempo(60) # Tempo initialization (default 60 bpm)
    #clock = Clock(tempo) # Clock initialization
    clock = ClockSequencer() # Clock initialization
    ledSequence = LEDSequence(8) # LEDs Sequence initialization (8 LEDs)

    #lcd.toggleBacklight(True) # Turns the backlight ON
    lcd.displayTempo(tempo.current_tempo) # shows the current tempo

    for i in range(1,5):
        # Start of the tick tack sequence (10 times)
        clock.ticking(tempo)
    
    tempo.changeTempo(120)
    lcd.displayTempo(tempo.current_tempo)

    for i in range(1,5):
        # Start of the tick tack sequence (10 times)
        clock.ticking(tempo)

    lcd.toggleBacklight(False) # Turns the backlight OFF for the end of the program
'''

''' Test code on RPi
    lcd.displayNote("A#",4)
    lcd.displayTempo(100)
    step7 = Step(7)
    time.sleep(5)
    lcd.displayStep(step7)
    time.sleep(5)
    lcd.clearLCD()
    lcd.toggleBacklight(False)
'''

