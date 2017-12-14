
import json
import argparse
from oct2py import Oct2Py, io
import pprint
import os

import nbformat as nbf
import datetime
import time
import shutil
import numpy as np

from cytometer import Cytometer
from process import ProcessControl
from color_model import ColorModel
from experiment import Experiment
from analysis import Analysis 

import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--cytometer-configuration',required=True,help='Configuration specifying channel names, excitation wavelengths, and filters')
parser.add_argument('--process-control',required=True,help='Configuration specifying calibration, negative control, and cross file pairs')
parser.add_argument('--experimental-data',required = True, help='Configuration specifying experimental conditions for input file')
parser.add_argument('--color-model-parameters',required=True,help='Configuration specifying how TASBE will build color model')
parser.add_argument('--analysis-parameters',required=True,help='Analysis file')
parser.add_argument('--octave-method-path',help='directory for the helper octave functions')

target_dir = 'output'

def main(args):
  octave = Oct2Py()
  octave.addpath('/vagrant/TASBEFlowAnalytics/code')
  cytometer = Cytometer(args.cytometer_configuration,octave) 
  process = ProcessControl(args.process_control,octave)
  color_model = ColorModel(args.color_model_parameters,octave,process,cytometer)
  experiment_data = Experiment(args.experimental_data,octave)
  experiment_analysis = Analysis(args.analysis_parameters,octave)
	
  color_model.make_gating(experiment_data)
  color_model.make_color_model()
  experiment_analysis.analyze()
  
# Start building quick look
  if not os.path.isdir(target_dir + '/quicklook_plots'):
    os.makedirs(target_dir + '/quicklook_plots')
  quicklook = nbf.v4.new_notebook()
  with open(args.experimental_data, 'r') as f:
    expdata = json.load(f)['tasbe_experimental_data']
  with open(args.color_model_parameters, 'r') as f:
    channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']

# Header
  if 'rdf:about' in expdata:
  	markdown = '## Data collection: {}'.format(expdata['rdf:about'])
  else:
  	markdown = '## Data collection not specified in {}'.format(args.experimental_data)
  markdown += '\n\n# Analyzed at {} UTC'.format(datetime.datetime.utcnow())
  quicklook['cells'].append(nbf.v4.new_markdown_cell(markdown))

# Gating
  markdown = '## Gating autodetect using {0:.2f}% valid and non-saturated data'.format(100*color_model.octave.eval('struct(gating).fraction_kept'))
  quicklook['cells'].append(nbf.v4.new_markdown_cell(markdown))
  quicklook['cells'].append(make_image_cell('plots/AutomaticGate-FSC-A-vs-SSC-A.png'))

# Channel calibration  
  quicklook['cells'].append(nbf.v4.new_markdown_cell('# Calibration beads'))
  for channel in channelparams:
  	label = channel['label']
  	quicklook['cells'].append(nbf.v4.new_markdown_cell('## {}'.format(label)))
  	quicklook['cells'].append(make_image_cell('plots/bead-calibration-{}.png'.format(label)))

# Channel autofluorescence  
  quicklook['cells'].append(nbf.v4.new_markdown_cell('# Autofluorescence'))
  for channel in channelparams:
  	label = channel['label']
  	quicklook['cells'].append(nbf.v4.new_markdown_cell('## {}'.format(label)))
  	quicklook['cells'].append(make_image_cell('plots/autofluorescence-{}.png'.format(label)))

# Compensation matrices
  if len(channelparams) > 1:
    comp_matrix = []
    val_matrix = []
    for rowchan in channelparams:
      comp_matrix.append([])
      val_matrix.append([])
      for colchan in channelparams:
        if rowchan != colchan:
          comp_imname = 'color-compensation-{}-for-{}.png'.format(rowchan['label'], colchan['label'])
          val_imname = 'compensated-{}-vs-positive-{}.png'.format(rowchan['label'], colchan['label'])
          shutil.copy2('plots/{}'.format(comp_imname), target_dir + '/quicklook_plots')
          shutil.copy2('plots/{}'.format(val_imname), target_dir + '/quicklook_plots')
          comp_matrix[-1].append('quicklook_plots/' + comp_imname)
          val_matrix[-1].append('quicklook_plots/' + val_imname)
    quicklook['cells'].append(nbf.v4.new_markdown_cell('# Compensation models'))
    quicklook['cells'].append(make_image_matrix_cell(comp_matrix))
    quicklook['cells'].append(nbf.v4.new_markdown_cell('# Compensated positive controls'))
    quicklook['cells'].append(make_image_matrix_cell(val_matrix))
# Translation matrix
    trans_matrix = []
    chan1_ind = 0;
    for chan1 in channelparams:
      for chan2 in channelparams[chan1_ind + 1:]:
        trans_imname = 'color-translation-{}-to-{}.png'.format(chan1['label'], chan2['label'])
        trans_imname_r = 'color-translation-{}-to-{}.png'.format(chan2['label'], chan1['label'])
        if os.path.isfile('plots/' + trans_imname) or os.path.isfile('plots/' + trans_imname_r):
          trans_matrix.append([])
        if os.path.isfile('plots/' + trans_imname):
          shutil.copy2('plots/' + trans_imname, target_dir + '/quicklook_plots')
          trans_matrix[-1].append('quicklook_plots/' + trans_imname)
        if os.path.isfile('plots/' + trans_imname):
          shutil.copy2('plots/' + trans_imname_r, target_dir + '/quicklook_plots')
          trans_matrix[-1].append('quicklook_plots/' + trans_imname_r)
      chan1_ind += 1
    quicklook['cells'].append(nbf.v4.new_markdown_cell('# Translation models'))
    quicklook['cells'].append(make_image_matrix_cell(trans_matrix))

# Data for each sample  
  for sample in experiment_analysis.results:
    means = sample['means']
    if type(means) == io.Cell: means = means.tolist()
    try:
      means = means[0]
    except:
      means = [means]
    stds = sample['stds']
    if type(stds) == io.Cell: stds = stds.tolist()[0]
    try:
      stds = stds[0]
    except:
      stds = [stds]
    channel_names = sample['channel_names']
    if type(channel_names) == io.Cell: channel_names = channel_names.tolist()[0]
    if type(channel_names[0]) == list: channel_names = channel_names[0]
    quicklook['cells'].append(make_well_summary_cell(octave, sample['condition'], means, stds, channel_names))
  
# Save report
  with open(target_dir + '/quicklook.ipynb', 'w') as ql_file:
  		nbf.write(quicklook, ql_file)
  
def make_image_matrix_cell(source_matrix):
  markup = '<table>\n'
  n_rows = len(source_matrix)
  n_cols = len(source_matrix[0])
  for ri in range(n_rows):
    markup += '<tr>\n'
    for ci in range(n_cols):
      markup += "<td><img src='{}' /></td>".format(source_matrix[ri][ci])
    markup += '</tr>\n'
  markup += '</table>'
  return nbf.v4.new_markdown_cell(markup)

def make_well_summary_cell(octave, condition, means, stds, channels):
  markdown = '#### Condition: ' + condition;
  markdown += '\n\n| Statistic ' + ''.join(['| {} '.format(c) for c in channels]) + '|'
  markdown += '\n|---' + ''.join(['|---' for c in channels]) + '|'
  markdown += '\n| Geo. Mean ' + ''.join(['| {0:.2f} '.format(float(m)) for m in means]) + '|'
  markdown += '\n| Geo. STD ' + ''.join(['| {0:.2f} '.format(float(s)) for s in stds]) + '|'
  plotfilename = octave.eval('sanitize_name("Exp-{}-bincounts");'.format(condition))
  if (len(plotfilename) > 75):
    plotfilename = 'X' + plotfilename[-74:]

  shutil.copy2('plots/{}.png'.format(plotfilename), target_dir + '/quicklook_plots')
  markdown += '\n\n<img src="quicklook_plots/{}.png">'.format(plotfilename)
  return nbf.v4.new_markdown_cell(markdown)

def make_image_cell(source):
	if os.path.exists(source):
		markup = '<img src="quicklook_{}">'.format(source)
		shutil.copy2(source, target_dir + '/quicklook_plots')
	else:
		markup = 'Image file {} not found'.format(source)
	return nbf.v4.new_markdown_cell(markup)

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)
