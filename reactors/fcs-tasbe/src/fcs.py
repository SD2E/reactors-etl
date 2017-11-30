
import json
import argparse
from oct2py import Oct2Py
import pprint
import os 

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

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)
