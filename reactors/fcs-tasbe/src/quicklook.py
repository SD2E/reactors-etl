import os
import shutil
import nbformat as nbf
import json
import datetime
from oct2py import io
import numpy as np

class Quicklook:
    def __init__(self,args, exp_analysis, octave):
        self.octave = octave
        self.args = args

        with open(self.args.analysis_parameters, 'r') as f:
            a = json.load(f)['tasbe_analysis_parameters']

            self.look = True
            #check for quicklook option set
            if not a['output']['quicklook']:
                self.look = False
                return


            self.quicklook_dir = a['output']['quicklook_folder']


            self.experiment_analysis = exp_analysis

            if not os.path.isdir(self.quicklook_dir):
                os.makedirs(self.quicklook_dir)

            if not os.path.isdir(self.quicklook_dir+'/quicklook_plots'):
                os.makedirs(self.quicklook_dir+'/quicklook_plots')



            with open(args.experimental_data, 'r') as f:
                self.expdata = json.load(f)['tasbe_experimental_data']
            with open(args.color_model_parameters, 'r') as f:
                self.channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']

    def make_notebook(self):

        if not self.look:
            return

        self.notebook = nbf.v4.new_notebook()

        self.make_header()
        self.make_gating()
        self.make_channel_calibration()
        self.make_channel_autofluorescence()
        self.make_compensation_matrices()
        self.make_translation_matrix()
        self.make_samples()

        with open(self.quicklook_dir + '/quicklook.ipynb', 'w') as ql_file:
            nbf.write(self.notebook, ql_file)


    def make_header(self):
        if 'rdf:about' in self.expdata:
            markdown = '## Data collection: {}'.format(self.expdata['rdf:about'])
        else:
            markdown = '## Data collection not specified in {}'.format(self.args.experimental_data)
        markdown += '\n\n# Analyzed at {} UTC'.format(datetime.datetime.utcnow())
        self.notebook['cells'].append(nbf.v4.new_markdown_cell(markdown))

    def make_gating(self):
        # Gating
        markdown = '## Gating autodetect using {0:.2f}% valid and non-saturated data'.format(
            100 * self.octave.eval('struct(gating).fraction_kept'))
        self.notebook['cells'].append(nbf.v4.new_markdown_cell(markdown))
        self.notebook['cells'].append(self.make_image_cell('plots/AutomaticGate-FSC-A-vs-SSC-A.png'))

    def make_channel_calibration(self):

        with open(self.args.color_model_parameters, 'r') as f:
            channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']

            self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Calibration beads'))
            for channel in channelparams:
                label = channel['label']
                self.notebook['cells'].append(nbf.v4.new_markdown_cell('## {}'.format(label)))
                self.notebook['cells'].append(self.make_image_cell('plots/bead-calibration-{}.png'.format(label)))

    def make_channel_autofluorescence(self):

        with open(self.args.color_model_parameters, 'r') as f:
            channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']

            self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Autofluorescence'))
            for channel in channelparams:
                label = channel['label']
                self.notebook['cells'].append(nbf.v4.new_markdown_cell('## {}'.format(label)))
                self.notebook['cells'].append(self.make_image_cell('plots/autofluorescence-{}.png'.format(label)))


    def make_compensation_matrices(self):

        with open(self.args.color_model_parameters, 'r') as f:
            channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']
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
                            shutil.copy2('plots/{}'.format(comp_imname), self.quicklook_dir + '/quicklook_plots')
                            shutil.copy2('plots/{}'.format(val_imname), self.quicklook_dir + '/quicklook_plots')
                            comp_matrix[-1].append('quicklook_plots/' + comp_imname)
                            val_matrix[-1].append('quicklook_plots/' + val_imname)
                self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Compensation models'))
                self.notebook['cells'].append(self.make_image_matrix_cell(comp_matrix))
                self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Compensated positive controls'))
                self.notebook['cells'].append(self.make_image_matrix_cell(val_matrix))

    def make_translation_matrix(self):
        with open(self.args.color_model_parameters, 'r') as f:
            channelparams = json.load(f)['tasbe_color_model_parameters']['channel_parameters']
            trans_matrix = []
            chan1_ind = 0;
            for chan1 in channelparams:
                for chan2 in channelparams[chan1_ind + 1:]:
                    trans_imname = 'color-translation-{}-to-{}.png'.format(chan1['label'], chan2['label'])
                    trans_imname_r = 'color-translation-{}-to-{}.png'.format(chan2['label'], chan1['label'])
                    if os.path.isfile('plots/' + trans_imname) or os.path.isfile('plots/' + trans_imname_r):
                        trans_matrix.append([])
                    if os.path.isfile('plots/' + trans_imname):
                        shutil.copy2('plots/' + trans_imname, self.quicklook_dir + '/quicklook_plots')
                        trans_matrix[-1].append('quicklook_plots/' + trans_imname)
                    if os.path.isfile('plots/' + trans_imname):
                        shutil.copy2('plots/' + trans_imname_r, self.quicklook_dir + '/quicklook_plots')
                        trans_matrix[-1].append('quicklook_plots/' + trans_imname_r)
                chan1_ind += 1
            self.notebook['cells'].append(nbf.v4.new_markdown_cell('# Translation models'))
            self.notebook['cells'].append(self.make_image_matrix_cell(trans_matrix))


    def make_samples(self):

        for sample in self.experiment_analysis.results:
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
            self.notebook['cells'].append(self.make_well_summary_cell(sample['condition'], means, stds, channel_names))

    def make_well_summary_cell(self, condition, means, stds, channels):
        markdown = '#### Condition: ' + condition
        markdown += '\n\n| Statistic ' + ''.join(['| {} '.format(c) for c in channels]) + '|'
        markdown += '\n|---' + ''.join(['|---' for c in channels]) + '|'
        markdown += '\n| Geo. Mean ' + ''.join(['| {0:.2f} '.format(float(m)) for m in means]) + '|'
        markdown += '\n| Geo. STD ' + ''.join(['| {0:.2f} '.format(float(s)) for s in stds]) + '|'
        plotfilename = self.octave.eval('sanitize_name("Exp-{}-bincounts");'.format(condition))
        if (len(plotfilename) > 75):
            plotfilename = 'X' + plotfilename[-74:]

        shutil.copy2('plots/{}.png'.format(plotfilename), self.quicklook_dir + '/quicklook_plots')
        markdown += '\n\n<img src="quicklook_plots/{}.png">'.format(plotfilename)
        return nbf.v4.new_markdown_cell(markdown)


    def make_image_matrix_cell(self,source_matrix):
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



    def make_image_cell(self, source):
        filename = source.split('/')[-1]
        if os.path.exists(source):
            markup = '<img src="quicklook_plots{}">'.format(filename)
            shutil.copy2(source, self.quicklook_dir + '/quicklook_plots/{}'.format(filename))
        else:
            markup = 'Image file {} not found'.format(source)
        return nbf.v4.new_markdown_cell(markup)

