import json
from pprint import pprint
import logging

class Cytometer:
  def __init__(self,file_name,octave):
    with open(file_name) as f:
      self.obj = json.load(f)['tasbe_cytometer_configuration']
    
    self.octave = octave
    self.make_channels()

  def make_channels(self):
    channels = self.obj['channels']
    self.channels = []
    self.octave.eval('channels = {}')
    
    for i,c in enumerate(channels):
      logging.debug('Instantiating channel {}'.format(c['name']))
      f = c['emission_filter']
      self.octave.eval('c = Channel(\'{}\',{},{},{});'.format(c['name'],c['excitation_wavelength'],f['center'],f['width']))
      self.octave.eval('channels{'+str(i+1)+'} = c')
