import google.auth, google.drive, google.mail
from google.drive import app_files
# You can define variables and functions here, and use them from any form. For example:
#
#    import Module1
#
#    Module1.say_hello()
#

def get_gpa(input_gpa):
  gpa = float(input_gpa.text)*535.7
  if gpa > 2250:
    gpa = 2250
  return gpa
def get_tests(input_sat, input_sat):
  if not input_act.text:
    act = 0
  if not input_sat.text:
    sat = 0
  if input_sat.text:
    sat = int(input_sat.text) * 1.03125
  if input_act.text:
    actToSat = { #dict of act to new sat scores
      11:590,
      12:680,
      13:740,
      14:780,
      15:830,
      16:870,
      17:910,
      18:950,
      19:990,
      20:1030,
      21:1070,
      22:1110,
      23:1140,
      24:1180,
      25:1220,
      26:1260,
      27:1290,
      28:1320,
      29:1360,
      30:1400,
      31:1430,
      32:1470,
      33:1500,
      34:1540,
      35:1570,
      36:1600
    }
    actog = int(input_act.text)
    act = actToSat[actog] * 1.03125
  test = max(act,sat)
  if (test > 1650):
    test = 1650
  return test
def get_rigor(input_math, input_science, input_english, input_foreign, input_perf):
  math = (int(input_math.text) - 6)*125
  science = (int(input_science.text) - 4) * 50
  english = (int(input_english.text) - 8) * 50
  foreign = (int(input_foreign.text) - 4) * 25
  perf = (int(input_perf.text) - 2) * 25
  if (math > 500): math = 500
  if (science > 200): science = 200
  if (english > 100): english = 100
  if (foreign > 100): foreign = 100
  if (perf > 50): perf = 50
  
  return math + science + english + foreign + perf

def get_extras(hours, multiplier):
  if hours in range(1,6):
    return multiplier
  if hours in range(6, 11):
    return multiplier*2
  if hours in range(11, 16):
    return multiplier*3
  if hours in range(16,21):
    return multiplier * 4
  if hours > 21:
    return multiplier*5
  return 0

def get_ecs(input_workhrs, input_echrs, check_workmajor, check_leader):
  work = get_extras(int(input_workhrs.text), 20)
  ec = get_extras(int(input_echrs.text), 30)
  if (check_workmajor.checked): work += 50
  if (check_leader.checked): ec += 60
  total = work + ec if work+ec <= 350 else 350
  return total