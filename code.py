# Make It Talk - Prof. John Gallaugher's animation of
import board, mount_sd, audiomixer, adafruit_mpr121, random
from adafruit_debouncer import Button
from audiomp3 import MP3Decoder
try:
   from audioio import AudioOut # Comment out above & uncomment this for DAC boards
except ImportError:
   try:
       from audiopwmio import PWMAudioOut as AudioOut
   except ImportError:
       print("This board does not support audio out")

# use speaker location to create an AudioOut object named audio
audio = AudioOut(board.GP15) # use board.GP# for pin number for audio out on a Pico

# setup path as name of folder + / where sounds are stored on CIRCUITPY
path = "/sd/yoda/"

# Create Mixer
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # This is where you might hear a pop

# setup the MP#Decoder object first & only once
filename = "brilliant.mp3"
mp3_file = open(path + filename, "rb") # read in data from file
decoder = MP3Decoder(mp3_file)

#
sayings = ["seeking_professor_g_you_are.mp3",
              "hungry_are_you_skittles_you_may_have.mp3",
              "welcome_you_are_happy_to_see_you.mp3",
              "strength_in_swift_and_circuit_python.mp3",
              "awesomeness_you_bring_yes.mp3",
              "wonder_i_am_a_person_for_others_are_you.mp3",
              "trust_in_the_one_who_is_bald_and_wears_a_beard_wise_he_is.mp3",
              "young_padawan_questions_for_me_have_you.mp3"
              "a_true_eagle_to_become_kind_you_must_be_mmm.mp3",
              "a_geek_you_will_become_study_hard_you_must.mp3"]

answers = ["already_you_know_that_which_you_need.mp3",
           "certain_of_this_i_am.mp3",
           "chosen_a_difficult_path_you_have_rise_to_the_challenge_you_must.mp3",
           "cloudy_your_future_is_as_an_eagle_you_must_be.mp3",
           "difficult_question_you_ask.mp3",
           "do_or_do_not_there_is_no_try.mp3",
           "hmm_this_even_yoda_does_not_know.mp3",
           "no_i_fear.mp3",
           "no_i_sense_this_is.mp3",
           "not_of_anything_to_say_about_it_i_have.mp3",
           "prepared_for_the_answer_are_you.mp3",
           "seek_inside_yourself_you_must_in_there_the_answer_is.mp3",
           "the_answer_you_seek_is_yes.mp3",
           "the_dark_side_clouds_everything_impossible_to_see_the_future_is.mp3",
           "troubling_question_you_ask_clear_the_answer_is_not.mp3",
           "uncertain_this_is_mmm.mp3",
           "unknown this is.mp3",
           "use_the_force_teach_you_it_will.mp3",
           "yes.mp3"]

# Function that plays mp3 using mixer
def play_mp3_voice(filename):
    decoder.file = open(path + filename, "rb")
    mixer.voice[0].play(decoder)
    while mixer.voice[0].playing:
        pass

# setup i2c & touchpads
i2c = board.STEMMA_I2C()
touch_pad = adafruit_mpr121.MPR121(i2c)
button_0 = Button(touch_pad[0], value_when_pressed=True)
button_5 = Button(touch_pad[5], value_when_pressed=True)

phrase_number = 0
interval = 0.4

while True:
    button_0.update()
    button_5.update()
    if button_0.pressed:
        print(f"Saying: {sayings[phrase_number]}")
        play_mp3_voice(sayings[phrase_number])
        phrase_number = phrase_number + 1 if phrase_number < (len(sayings)-1) else 0
    if button_5.pressed:
        random_phrase = random.choice(answers)
        print(f"Advice phrase: {random_phrase}")
        play_mp3_voice(random_phrase)
