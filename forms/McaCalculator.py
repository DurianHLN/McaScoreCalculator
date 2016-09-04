from anvil import *
import google.auth, google.drive, google.mail
from google.drive import app_files

#Welcome to Git Beta! 
#Welcome from Darian's PC
class McaCalculator (McaCalculatorTemplate):
  def get_gpa(self):
    gpa = float(self.input_gpa.text)*535.7
    if gpa > 2250:
      gpa = 2250
    return gpa
  def get_tests(self):
    if not self.input_act.text:
      act = 0
    if not self.input_sat.text:
      sat = 0
    if self.input_sat.text:
      sat = int(self.input_sat.text) * 1.03125
    if self.input_act.text:
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
      actog = int(self.input_act.text)
      act = actToSat[actog] * 1.03125
    test = max(act,sat)
    if (test > 1650):
      test = 1650
    return test
  def get_rigor(self):
    math = (int(self.input_math.text) - 6)*125
    science = (int(self.input_science.text) - 4) * 50
    english = (int(self.input_english.text) - 8) * 50
    foreign = (int(self.input_foreign.text) - 4) * 25
    perf = (int(self.input_perf.text) - 2) * 25
    if (math > 500): math = 500
    if (science > 200): science = 200
    if (english > 100): english = 100
    if (foreign > 100): foreign = 100
    if (perf > 50): perf = 50
    
    return math + science + english + foreign + perf
  
  def get_extras(self, hours, multiplier):
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
  
  def get_ecs(self):
    work = self.get_extras(int(self.input_workhrs.text), 20)
    ec = self.get_extras(int(self.input_echrs.text), 30)
    if (self.check_workmajor.checked): work += 50
    if (self.check_leader.checked): ec += 60
    total = work + ec if work+ec <= 350 else 350
    return total
  
  def print_error(self, errormsg):
    self.label_errors.text = errormsg
    self.label_errors.visible = True
    self.label_result.visible = False
    return False
  
  def get_quip(self, mca):
    if mca >= 5000: return "Damn son why aren't you going to Yale then"
    elif mca >= 4700: return "You're probably going to get accepted into any major at Cal Poly SLO."
    elif mca >= 4000: return "You're probably going to get accepted, but maybe not for competitive majors."
    elif mca >= 3500: return "You may get accepted, but definitely not for any competitive majors."
    else: return "Hopefully you're applying for an obsure major or you're SOL mate."
    
  def button_submit_click (self, **event_args):
    proceed = True
    try:
      gpa = self.get_gpa()
    except ValueError:
      proceed = self.print_error("Not a valid GPA you alien.")
      
    try:
      tests = self.get_tests()
    except (ValueError, KeyError):
      proceed = self.print_error("Invalid test score(s) you dingus")
      
    try:
      rigor = self.get_rigor()
    except ValueError:
      proceed = self.print_error("Not valid # of semesters you weirdo")
      
    try:
      ecs = self.get_ecs()
    except ValueError:
      proceed = self.print_error("Not valid # of hours you nincompoop")
    if proceed:
      result = gpa + tests + rigor + ecs
      self.label_result.text = "Your MCA Score is %d.\n" % int(result)
      self.label_result.text += self.get_quip(result)
      
      self.label_result.visible = True
      self.label_errors.visible = False
      self.data_sheet.add_row(Name=self.input_name.text if (self.input_name.text) else "Anon", Score=result)

  def link_1_click (self, **event_args):
    # This method is called when the link is clicked
    self.link_csu.url = "http://www.csumentor.edu/planning/high_school/gpa_calculator.asp"


  def __init__(self, **kwargs):
    self.init_components(**kwargs) #must be at the top
    self.data_sheet = google.drive.app_files.mcanames.worksheets[0]
