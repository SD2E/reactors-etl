import json
from pprint import pprint
import math
import oct2py

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
    
    colormapper = {u'EYFP': '[0.239, 1.0, 0.0]', \
    	u'mKate': '[1.0, 0.153, 0.0]', \
    	u'EBFP2': '[0.0, 0.157, 1.0]', \
    	u'GFP': '[0.0, 1.0, 0.098]'}
    # From https://www.leica-microsystems.com/science-lab/fluorescent-proteins-introduction-and-photo-spectral-characteristics/
    # and http://lsrtools.1apps.com/wavetorgb
    colorspecs = self.octave.pull('channel_names')
    if type(colorspecs) == oct2py.io.Cell: colorspecs = colorspecs.tolist()
    if type(colorspecs[0]) == list: colorspecs = colorspecs[0]
    colorspecs = '{' + ','.join([colormapper[x] for x in colorspecs]) + '}'
    self.octave.eval('outputsettings = OutputSettings("Exp", "", "", "plots");')
#     self.octave.eval('outputsettings.FixedInputAxis = [1e4 1e10];')
    self.octave.eval('plot_batch_histograms(results, sample_results, outputsettings, {}, cm);'.format(colorspecs))
    self.print_bin_counts(self.obj['channels'])

  def print_bin_counts(self,channels):

    a = self.octave.eval('length(channel_names)')
    color_order = {}
    
    for i in xrange(1,int(a)+1):
      color_order[self.octave.eval('channel_names{{1,{}}}'.format(i))] = i-1

    with open(self.obj['output']['file'],'w') as output_file: 
      output_file.write('condition,channel,{}\n'.format(','.join([str(math.log(i,10)) for i in self.results[0].bincenters.tolist()[0]])))
      for c in channels:
        index = color_order[c]
        for r in self.results:
          csv_results = ','.join([str(i[index]) for i in r.bincounts.tolist()])
          output_file.write('{},{},{}\n'.format(r['condition'],c,csv_results))

