import json
import logging

class ColorModel:
  def __init__(self,color_model_filename,octave,process_control,cytometer): 
    self.octave = octave
    self.process_control = process_control
    self.cytometer = cytometer
    with open(color_model_filename) as f:
      self.obj = json.load(f)['tasbe_color_model_parameters']

    self.make_gating()
    self.make_color_model()

  def make_gating(self):
    if self.obj['tasbe_config']['gating']['type'] == 'auto':
      logging.debug('Making gating')
      blank = self.process_control.get_blank_filename()
      k_components = self.obj['tasbe_config']['gating']['k_components']
      self.octave.eval('agp = AutogateParameters(); agp.k_components={};'.format(k_components))
      self.octave.eval('gating = GMMGating(\'{}\',agp,\'plots\');'.format(blank))
      self.gating = self.octave.eval('gating')
      

  def make_color_model(self):
    blank = self.process_control.get_blank_filename()
    bead_info = self.process_control.get_bead_info()
    logging.debug('Making color model')
    print bead_info
    self.process_control.get_color_files()

    self.octave.eval('cm = ColorModel(\'{}\',\'{}\',side_channels,color_channel_files,[])'.format(bead_info['file'],blank))
    self.octave.eval('cm = set_translation_plot(cm,false);')
    self.octave.eval('cm = set_noise_plot(cm,false);')
    self.octave.eval('cm = set_bead_model(cm,\'{}\');'.format(bead_info['model']))
    #TODO ADD in channel min
    self.octave.eval('cm = set_translation_channel_min(cm,{})'.format(2))
    self.octave.eval('cm = set_bead_batch(cm,\'{}\')'.format(bead_info['batch']))
    self.octave.eval('cm = set_FITC_channel_name(cm,\'{}\')'.format(self.obj['ERF_channel_name']))
    self.octave.eval('settings = TASBESettings();')
    self.octave.eval('settings = setSetting(settings,\'channel_template_file\',\'{}\')'.format(blank))
    #TODO add min
    self.octave.eval('settings = setSetting(settings,\'path\',\'{}\');'.format('plots'))  
    
    self.octave.eval('cm = add_filter(cm,gating);') 
    self.octave.eval('pkg load io;')
    self.octave.eval('cm=resolve(cm, settings);')


