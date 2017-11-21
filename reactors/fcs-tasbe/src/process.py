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
    for color in color_order:
      j+=1
      for channel in self.obj['channels']:
        if color == channel['name']:
          self.octave.eval('color_channel_files{'+str(i)+'} = \''+channel['calibration_file']+'\'')
          self.octave.eval('channels{{{}}} = setPrintName(channels{{{}}},\'{}\')'.format(j,j,color))
          self.octave.eval('side_channels{'+str(i)+'} = channels{'+str(j)+'};')
          self.octave.eval('channel_names{'+str(i)+'} = getName(channels{'+str(j)+'})')
          i+=1
