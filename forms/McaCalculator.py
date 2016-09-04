from anvil import *
import google.auth, google.drive, google.mail
from google.drive import app_files
import calculations

class McaCalculator (McaCalculatorTemplate):
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
      gpa = calculations.get_gpa(self.input_gpa)
    except ValueError:
      proceed = self.print_error("Not a valid GPA you alien.")
      
    try:
      tests = calculations.get_tests(self.input_sat, self.input_act)
    except (ValueError, KeyError):
      proceed = self.print_error("Invalid test score(s) you dingus")
      
    try:
      rigor = calculations.get_rigor(self.input_math, self.input_science, self.input_english, self.input_foreign, self.input_perf)
    except ValueError:
      proceed = self.print_error("Not valid # of semesters you weirdo")
      
    try:
      ecs = calculations.get_ecs(self.input_workhrs, self.input_echrs, self.check_workmajor, self.check_leader)
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
