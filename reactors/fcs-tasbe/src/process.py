import json
import pprint 

class ProcessControl:
  def __init__(self,process_control_filename,octave):
    with open(process_control_filename) as f:
      self.obj = json.load(f)['tasbe_process_control_data']

    self.octave = octave

  def get_blank_filename(self):
    return self.obj['blank_file']


  def get_bead_info(self):
    b = {}
    b['batch'] = self.obj['bead_batch']
    b['model'] = self.obj['bead_model']
    b['file']  = self.obj['bead_file']
    return b

  def set_color_model(self,color_model):
    self.color_model = color_model
  
  def get_color_files(self):
    i = self.octave.eval('length(channels)')
    color_order = []
    for i in xrange(1,int(i)+1):
      print i,'\n\n'
      s = self.octave.eval('getName(channels{'+str(i)+'})');
      color_order.append(s)

    print color_order
    
    self.octave.eval('color_channel_files = {}')
    self.octave.eval('side_channels = {}')
    self.octave.eval('channel_names = {}')
    i = 1
    j = 0;
    print '\n\nProcessing channels\n\n'
    print 'color order:', color_order
    for color in color_order:
      j+=1
      for channel in self.obj['channels']:
        print color, channel['name']
        if color == channel['name']:
          self.octave.eval('color_channel_files{'+str(i)+'} = \''+channel['calibration_file']+'\'')
          self.octave.eval('channels{{{0}}} = setPrintName(channels{{{0}}},\'{1}\')'.format(j,self.color_model.channel_parameters[color]['label']))
          self.octave.eval('side_channels{'+str(i)+'} = channels{'+str(j)+'};')
          self.octave.eval('channel_names{'+str(i)+'} = getPrintName(channels{'+str(j)+'})')
          self.octave.eval('channel_long_names{'+str(i)+'} = getName(channels{'+str(j)+'})')
          i+=1

  # Can't be run until channels is built, by get_color_files
  def get_color_pair_files(self):
    pairs = self.obj['cross_file_pairs']
    self.octave.eval('colorpairfiles = {};')
    for a in range(1, len(pairs)+1): #index of analysis we're working on
      for chan in range(1, len(pairs[a-1]['channels']) + 1):
        self.octave.eval('for c = 1:length(channels); if strcmp(getName(channels{{c}}), "{}"); colorpairfiles{{{}}}{{{}}} = channels{{c}}; end; end;'.format(pairs[a-1]['channels'][chan-1], str(a), str(chan)))
      self.octave.eval('colorpairfiles{{{}}}{{end+1}} = "{}"'.format(str(a), pairs[a-1]['file']))      
