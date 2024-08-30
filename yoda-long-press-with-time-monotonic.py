# MQTT Disco Subscriber (ONLY LIGHTS)
# Note - I'll eventually put sound & neopixels in separate builds to better manage power,
# but am using a single subscriber while I debug.
import random
import board, time, mount_sd, audiomixer, adafruit_mpr121
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

mixer.voice[0].level = 0.3

# setup i2c & touchpads
i2c = board.STEMMA_I2C()
touch_pad = adafruit_mpr121.MPR121(i2c)

# phrase lists
bc_phrases = ["seeking_professor_g_you_are.mp3",
              "hungry_are_you_skittles_you_may_have.mp3",
              "welcome_you_are_happy_to_see_you.mp3",
              "strength_in_swift_and_circuit_python.mp3",
              "awesomeness_you_bring_yes.mp3",
              "wonder_i_am_a_person_for_others_are_you.mp3",
              "trust_in_the_one_who_is_bald_and_wears_a_beard_wise_he_is.mp3",
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

# set up phrases
# phrases = ["a_geek_you_will_become_study_hard_you_must.mp3",
#     "a_true_eagle_to_become_kind_you_must_be_mmm.mp3",
#     "a_true_friend_how_can_i_help.mp3",
#     "afraid_i_am_not_it_is.mp3",
#     "already_you_know_that_which_you_need.mp3",
#     "clear_your_mind_must_be_if_you_are_to_find_the_villains_behind_this_plot.mp3",
#     "awesomeness_you_bring_yes.mp3",
#     "bc_we_are.mp3",
#     "brilliant.mp3",
#     "certain_of_this_i_am.mp3",
#     "chosen_a_difficult_path_you_have_rise_to_the_challenge_you_must.mp3",
#     "cloudy_your_future_is_as_an_eagle_you_must_be.mp3",
#     "cough_laugh.mp3",
#     "difficult_question_you_ask.mp3",
#     "do_or_do_not_there_is_no_try.mp3",
#     "excuse_me.mp3",
#     "find_you_will_only_what_you_bring_in.mp3",
#     "god_bless_you.mp3",
#     "great.mp3",
#     "hilarious.mp3",
#     "hmm_this_even_yoda_does_not_know.mp3",
#     "huh.mp3",
#     "hungry_are_you_skittles_you_may_have.mp3",
#     "impossible.mp3",
#     "incredible.mp3",
#     "just_the_beginning_this_is.mp3",
#     "luck_you_do_not_need_study_hard_you_must.mp3",
#     "may_the_4th_be_with_you.mp3",
#     "may_the_force_be_with_you.mp3",
#     "mind_what_you_have_learned_save_you_it_can.mp3",
#     "mmm_(thoughtful).mp3",
#     "much_to_learn_you_have.mp3",
#     "nice.mp3",
#     "no_i_fear.mp3",
#     "no_i_sense_this_is.mp3",
#     "not_of_anything_to_say_about_it_i_have.mp3",
#     "oh.mp3",
#     "prepared_for_the_answer_are_you.mp3",
#     "questions_for_me_have_you_answer_them_I_will.mp3",
#     "seek_inside_yourself_you_must_in_there_the_answer_is.mp3",
#     "seeking_advice_are_you_young_padawan.mp3",
#     "seeking_professor_g_you_are.mp3",
#     "simple_question_you_ask.mp3",
#     "skilled_at_swift_have_a_sticker.mp3",
#     "sneeze_achoo.mp3",
#     "sneeze.mp3",
#     "study_hard_a_swift_jedi_you_will_become.mp3",
#     "taught_baldwin_to_fly_i_have.mp3",
#     "thank_you.mp3",
#     "the_answer_you_seek_is_yes.mp3",
#     "the_dark_side_clouds_everything_impossible_to_see_the_future_is.mp3",
#     "troubling_question_you_ask_clear_the_answer_is_not.mp3",
#     "trust_in_the_one_who_is_bald_and_wears_a_beard_wise_he_is.mp3",
#     "uncertain_this_is_mmm.mp3",
#     "unknown this is.mp3",
#     "use_the_force_teach_you_it_will.mp3",
#     "use_the_force_then_use_swift_build_an_app.mp3",
#     "use_the_force_wisely_its_power_for_good_you_must_use.mp3",
#     "welcome_you_are_happy_to_see_you.mp3",
#     "welcome.mp3",
#     "wish_you_well_i_do_may_the_force_be_with_you.mp3",
#     "wonder_i_am_a_person_for_others_are_you.mp3",
#     "wonderful.mp3",
#     "wow.mp3",
#     "yes.mp3",
#     "young_padawan_questions_for_me_have_you.mp3"]

# Function that plays mp3 using mixer
def play_mp3_voice(filename):
    decoder.file = open(path + filename, "rb")
    mixer.voice[0].play(decoder)
    while mixer.voice[0].playing:
        pass

phrase_number = 0
adafruit_mpr121.MPR121_Channel(touch_pad, 0).threshold = 24
adafruit_mpr121.MPR121_Channel(touch_pad, 5).threshold = 24
print(f"threshold Pad 0: {adafruit_mpr121.MPR121_Channel(touch_pad, 0).threshold}")
print(f"threshold Pad 5: {adafruit_mpr121.MPR121_Channel(touch_pad, 5).threshold}")

interval = 0.4

play_mp3_voice("yes.mp3")

while True:
    if touch_pad.is_touched(0):
        last_0_time = time.monotonic()
        time.sleep(interval)
    if touch_pad.is_touched(5):
        last_5_time = time.monotonic()
        time.sleep(interval)
    if touch_pad.is_touched(0) and (time.monotonic() - last_0_time) > interval:
        print(f"0 touched: {time.monotonic()}, {last_0_time}")
        print(f"BC Phrase: {bc_phrases[phrase_number]}")
        play_mp3_voice(bc_phrases[phrase_number])
        phrase_number = phrase_number + 1 if phrase_number < (len(bc_phrases)-1) else 0
        last_0_time = time.monotonic()
    if touch_pad.is_touched(5) and (time.monotonic() - last_5_time) > interval:
        print(f"0 touched: {time.monotonic()}, {last_5_time}")
        random_phrase = random.choice(answers)
        print(f"Advice phrase: {random_phrase}")
        play_mp3_voice(random_phrase)
        last_5_time = time.monotonic()

    last_0_time = time.monotonic()
    last_5_time = time.monotonic()