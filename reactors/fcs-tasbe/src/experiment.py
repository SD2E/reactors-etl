import json
from pprint import pprint
import logging

class Experiment:
  def __init__(self, experiment_filename, octave):
    self.octave = octave
    with open(experiment_filename) as f:
      self.obj = json.load(f)['tasbe_experimental_data']

    self.generate_experimental_array()

  def get_first_experiment_file(self):
    return self.obj['samples'][0]['file']

  def generate_experimental_array(self):
    self.octave.eval('file_pairs = {}')
    i =1 
    for sample in self.obj['samples']:
      self.octave.eval('file_pairs{{{0},1}} = \"{1}\"'.format(i,sample['sample']))
      self.octave.eval('file_pairs{{{0},2}} = {{[\'{1}\'] }} '.format(i,sample['file']))
      i+=1

    #self.octave.eval('file_pairs')
    #exit()
