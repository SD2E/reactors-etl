import json
from pprint import pprint
import math

class Analysis:
  def __init__(self,analysis_filename,octave):
    self.octave = octave
    with open(analysis_filename) as f:
      self.obj = json.load(f)['tasbe_analysis_parameters']

  def analyze(self):
    self.octave.eval('bins = BinSequence(0,0.1,10,\'log_bins\');');
    self.octave.eval('ap = AnalysisParameters(bins,{});')
    self.octave.eval('ap = setMinValidCount(ap,100\');')
    self.octave.eval('ap = AP=setPemDropThreshold(ap,5\');');
    self.octave.eval('ap = setUseAutoFluorescence(ap,false\');')
    
     
    self.octave.eval('[results sample_results] = per_color_constitutive_analysis(cm,file_pairs,channel_names,ap);')  
    a = self.octave.eval('length(sample_results)')
    
    self.results = []
    #self.octave.eval('results[1]')
    
    for i in xrange(1,int(a)+1):
      self.octave.eval('results {{{}}}.channel_names = channel_names'.format(i))
      r = self.octave.eval('results{{{}}};'.format(i))
      r['condition'] = self.octave.eval('file_pairs{{{},1 }};'.format(i))
      self.results.append(r)

    self.print_bin_counts(self.obj['channels'])

  def print_bin_counts(self,channels):

    a = self.octave.eval('length(channel_names)')
    color_order = {}
    
    for i in xrange(1,int(a)+1):
      color_order[self.octave.eval('channel_names{{1,{}}}'.format(i))] = i-1

    with open(self.obj['output']['file'],'w') as output_file: 
      print self.results[0]
      output_file.write('condition,channel,geo_mean,{}\n'.format(','.join([str(math.log(i,10)) for i in self.results[0].bincenters.tolist()[0]])))
      for c in channels:
        index = color_order[c]
        for r in self.results:
          csv_results = ','.join([str(i[index]) for i in r.bincounts.tolist()])
          output_file.write('{},{},{},{}\n'.format(r['condition'],c,r['means'],csv_results))
          print r

