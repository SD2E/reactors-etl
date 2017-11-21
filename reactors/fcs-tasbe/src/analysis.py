import json
from pprint import pprint

class Analysis:
  def __init__(self,analysis_filename,octave):
    self.octave = octave
    with open(analysis_filename) as f:
      self.obj = json.load(f)['tasbe_analysis_parameters']

  def analyze(self):
    self.octave.eval('bins = BinSequence(4,0.1,10,\'log_bins\')');
    self.octave.eval('ap = AnalysisParameters(bins,{});')
    self.octave.eval('ap = setMinValidCount(ap,10)')
    self.octave.eval('ap = setUseAutoFluorescence(ap,false\') ')
    self.octave.eval('file_pairs')
    self.octave.eval('channel_names')
    
    self.octave.eval('per_color_constitutive_analysis(cm,file_pairs,channel_names,ap)')  

