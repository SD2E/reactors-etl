import json
from pprint import pprint
import math
import oct2py
from wavelength_to_rgb import wavelength_to_rgb

class Analysis:
  def __init__(self,analysis_filename, cytometer_filename, octave):
    self.octave = octave
    with open(analysis_filename) as f:
      self.obj = json.load(f)['tasbe_analysis_parameters']
    with open(cytometer_filename) as f:
      self.cytometer_config = json.load(f)['tasbe_cytometer_configuration']

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
    
    longnames = self.octave.pull('channel_long_names')
    if type(longnames) == oct2py.io.Cell: longnames = longnames.tolist()
    if type(longnames[0]) == list: longnames = longnames[0]
    colorspecs = []
    for longname in longnames:
    		colorspecs.append(wavelength_to_rgb([x['emission_filter']['center'] for x in self.cytometer_config['channels'] if x['name'] == longname][0]))
    colorspecs = '{' + ','.join(colorspecs) + '}'
    self.octave.eval('outputsettings = OutputSettings("Exp", "", "", "{}");'.format(self.obj.get('output', {}).get('plots_folder', 'plots')))
#     self.octave.eval('outputsettings.FixedInputAxis = [1e4 1e10];')
    self.octave.eval('plot_batch_histograms(results, sample_results, outputsettings, {}, cm);'.format(colorspecs))
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

