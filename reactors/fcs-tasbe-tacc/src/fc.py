import json
import argparse
from oct2py import octave
import logging
from oct2py import Oct2Py, get_log
import pprint

# python fc.py --octave-method-path /opt/scripts/
#              --config fc.json --files LacI-CAGop_B10_B10_P3.fcs
#              --label "Dox 0.1" --title "sample_run"
#              --type "geo_mean_std"
#              --output 'moof.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--files', help='Input file(s) for experiment')
# [TODO] Learn whether readings actually has an expected cardinality > 1
# [TODO] Learn expected cardinality of files in a given reading
# [TODO] Learn how best to represent multiple entries for --files
# -files A,B,C,D
# -files A B C D
# -file A -file B -file C
#
# [NOTE] One possible way to skin this is to formalize a directory structure
#        for readings sets. We'd stage the directory in place then iterate over
#        it in code to discover the input data's structure and metadata. Or, a
#        top-level manifest could be provided. Either way, hand-eumerating more
#        than a few input files in error-prone and unwieldy
# Dummy implementation 1:
# agave://data-system-work/experiments/fcs/data/experiment001/readings
#    readings/
#      000000/
#        - metadata.json
#        - File1.fcs
#        - File2.fcs
#        - File3.fcs
# Dummy implementation 2:
# agave://data-system-work/experiments/fcs/data/experiment001/readings
#    readings/
#        -manifest.json
#        -File1.fcs
#        -File2.fcs
#        -File3.fcs

parser.add_argument('--label', help='Experiment label',
                    default='Experiment_label_0.1')
parser.add_argument('--title', help='Analysis title', default='sample_run')
# [TODO] Learn if there is a dictionary of analysis types for validating 
#        this parameter
parser.add_argument('--type', help='Analysis type', default='geo_mean_std')
parser.add_argument('--plots', help='Generate plots', default=True)
parser.add_argument('--plotsFolder', help='Plots folder name', default='plots')
parser.add_argument('--output', help='Name of output file',
                    default='output.csv')
# [TODO] Learn whether the set of controls and channels expressed in fc.json is stable
#        across an experimental series or longer. If so, could bundle a default fc.json
#        and control data with the image.  
parser.add_argument('--config', help='Configuration file for FC',
                    default='fc.json')
parser.add_argument('--octave-method-path',
                    help='directory for the helper octave functions',
                    default='/opt/scripts/')

class Cytometer:
    def __init__(self, obj):
        self.obj = obj

    def get_channel(self, channel_name):
        for i in self.obj['channels']:
            if i['name'] == channel_name:
                    return i


class Channel:
    def __init__(self,obj, cytometer):
        self.obj = obj
        self.calibration_filename = obj['calibration_file']
        self.cytometer = cytometer
        self.make_octave_object()

    def get_name(self):
        return self.obj['name']

    def make_octave_object(self):
        o = self.obj
        f = self.cytometer.get_channel(self.obj['name'])
        c,w = f['emission_filter']['center'],f['emission_filter']['width'],
        self.octave_obj = octave.create_color_channel(o['name'],o['label'],f['excitation_wavelength'],c,w,o['chart_color'])


class ColorModel:
    def __init__(self, obj, channels):
        self.obj = obj
        self.channels = channels
        self.create_calibration_list()
        self.create_color_pairs()
        self.create_color_channel_file_list()
        self.make_octave_color_model_object()

    def create_color_channel_file_list(self):
        self.color_channel_files = []
        for channel in self.channels:
            for cm_channels in self.obj['channels']:
                if cm_channels['name'] == channel.obj['name']:
                    self.color_channel_files.append(cm_channels['calibration_file'])

    def create_calibration_list(self):
        self.calibration_list = []
        self.channel_min_list = []
        for i in self.channels:
            for j in self.obj['channels']:
                if i.get_name() == j['name']:
                    self.calibration_list.append(j['calibration_file'])
                    self.channel_min_list.append(j['min'])
        print self.calibration_list

    def create_color_pairs(self):
        self.color_pairs = []
        self.color_files = []
        for pair in self.obj['cross_file_pairs']:
            cp = []
            for channel in pair['channels']:
                discovered = False
                for setting in self.channels:
                    if channel == setting.get_name():
                        cp.append(channel)
                        discovered = True
                if not discovered:
                    raise Exception("ColorModel::create_color_pairs: Unable to match {}".format(channel))

            cp.append(pair['file'])

            self.color_pairs.append(cp)
        print self.color_pairs

    def make_octave_color_model_object(self):
        o = self.obj
        self.octave_object = octave.create_color_model_object(o['bead_file'], o['blank_file'],o['bead_model'],o['bead_batch'],
o['translation_plot'],o['noise_plot'],o['FITC_channel_name'],self.channel_min_list)


class Experiment:
    def __init__(self, obj):
        self.obj = obj
        self.octave_object = None
        self.create_octave_object()
        self.create_output_file_list()

    def create_octave_object(self):
        o = self.obj['output']
        if o['type'] == 'geo_mean_std':
            plots_folder = ''
            if o['plots']:
                plots_folder = o['plots_folder']
            self.octave_output_object = octave.create_batch_histogram_output_object(o['plots'],o['plots_folder'],o['file'],o['title'])    

    def create_output_file_list(self):
        self.octave_readings_object = -1
        for r in self.obj['readings']:
            self.octave_readings_object = octave.create_output_file_list(self.octave_readings_object,r['label'],r['files']) 


def main(args):

    oc = Oct2Py(logger=get_log())
    oc.logger = get_log('new_log')
    oc.logger.setLevel(logging.DEBUG)

    with open(args.config) as f:
        configuration_object = json.load(f)

    # NEW CODE TO SEPARATE OUT SOME PARAMETERIZATION OF fc.json
    configuration_object['experiment'] = {}
    configuration_object['experiment']['readings'] = []
    configuration_object['experiment']['readings'].append(
        {'label': args.label, 'files': [args.files]})
    configuration_object['experiment']['output'] = {
        'title': args.title,
        'type': args.type,
        'plots': args.plots,
        'plots_folder': 'plots',
        'file': args.output
    }
    print json.dumps(configuration_object, indent=4)
    #sys.exit(0)
    # END NEW CODE

    octave.addpath(args.octave_method_path)

    print 'Making cytometer'
    cytometer = Cytometer(configuration_object['cytometer_configuration'])

    print 'Making color channel'

    color_channels = []
    color_files = []
    color_channels_octave_array = -1 # -1 is the initial state of the array for creast_color_channel_array function
    for channel in configuration_object['color_model']['channels']:
        c = Channel(channel, cytometer)
        color_channels.append(c)
    cm = ColorModel(configuration_object['color_model'], color_channels)

    bead_file = cm.obj['bead_file']
    blank_file = cm.obj['blank_file']
    bead_model = cm.obj['bead_model']

    octave_channel_objects = []
    channel_files = []
    for c in color_channels:
         octave_channel_objects.append(c.octave_obj)

    pprint.pprint(configuration_object['experiment'])
    output = Experiment(configuration_object['experiment'])

    print "bead file: {}".format(bead_file)
    print "\n\n"
    print "blank file: {}".format(blank_file)
    print "\n\n"
    print "channels: {}".format(pprint.pprint(octave_channel_objects))
    print "\n\n"
    print "color_files: {}".format(pprint.pprint(cm.color_channel_files))
    print "color_pair_files: {}".format(pprint.pprint(cm.color_pairs))
    # configuration_object['experiment'])
    octave.process_experiment(octave_channel_objects, cm.octave_object,
                              cm.color_channel_files, cm.color_pairs,
                              output.octave_output_object,
                              output.octave_readings_object)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
