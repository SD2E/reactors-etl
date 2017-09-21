% This script processes flow cytometry data
%
%


function [CM] = process_fcs()
pkg load io;
bead_file = "/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_Beads_P3.fcs";
blank_file = "/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_blank_P3.fcs";
bead_model = "SpheroTech RCP-30-5A";
bead_batch = "Lot AA01, AA02, AA03, AA04, AB01, AB02, AC01, GAA01-R";
output = "";

color_channel_1 = 'FITC-A';

color_channel_1_name = 'EYFP';
color_channel_1_freq = 488;
color_channel_1_center = 515;
color_channel_1_width = 20;
color_channel_1_file = '/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_EYFP_P3.fcs';
color_channel_1_chart_color = 'y';

color_channel_2 = 'PE-Tx-Red-YG-A';
color_channel_2_name = 'mKate';
color_channel_2_freq = 561;
color_channel_2_center = 610;
color_channel_2_width = 20;
color_channel_2_file = '/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_mkate_P3.fcs';
color_channel_2_chart_color = 'r';

color_channel_3 = 'Pacific Blue-A';
color_channel_3_name = 'EBFP2';
color_channel_3_freq = 405;
color_channel_3_center = 450;
color_channel_3_width = 50;
color_channel_3_file = '/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_ebfp2_P3.fcs';
color_channel_3_chart_color = 'b';

color_file_123 = '/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_mkate_EBFP2_EYFP_P3.fcs';
color_file_132 = '/vagrant/TASBEFlowAnalytics-Tutorial/example_controls/2012-03-12_mkate_EBFP2_EYFP_P3.fcs';

FITC_channel_name = 'FITC-A';

AGP = AutogateParameters();
autogate = autodetect_gating(blank_file,AGP,'plots');

channels = {}; colorfiles = {};
channels{1} = Channel(color_channel_1, color_channel_1_freq, color_channel_1_center, color_channel_1_width);
channels{1} = setPrintName(channels{1}, color_channel_1_name); % Name to print on charts
channels{1} = setLineSpec(channels{1}, color_channel_1_chart_color); % Color for lines, when needed
colorfiles{1} = color_channel_1_file;

channels{2} = Channel(color_channel_2, color_channel_2_freq, color_channel_2_center, color_channel_2_width);
channels{2} = setPrintName(channels{2}, color_channel_2_name); % Name to print on charts
channels{2} = setLineSpec(channels{2}, color_channel_2_chart_color); % Color for lines, when needed
colorfiles{2} = color_channel_2_file;

channels{3} = Channel(color_channel_3, color_channel_3_freq, color_channel_3_center, color_channel_3_width);
channels{3} = setPrintName(channels{3}, color_channel_3_name); % Name to print on charts
channels{3} = setLineSpec(channels{3}, color_channel_3_chart_color); % Color for lines, when needed
colorfiles{3} = color_channel_3_file;


colorpairfiles{1} = {channels{1}, channels{2}, channels{3}, color_file_123};
colorpairfiles{2} = {channels{1}, channels{3}, channels{2}, color_file_132};

CM = ColorModel(bead_file, blank_file, channels, colorfiles, colorpairfiles);
CM=set_bead_plot(CM,0 ); % 2 = detailed plots; 1 = minimal plot; 0 = no plot
CM=set_translation_plot(CM, true);
CM=set_noise_plot(CM, true);

CM=set_bead_model(CM,bead_model); % Entry from BeadCatalog.xls matching your beads
CM=set_bead_batch(CM,bead_batch); % Entry from BeadCatalog.xls containing your lot:/bead

CM=set_bead_min(CM, 2);
% The peak threshold determines the minumum count per bin for something to
% be considered part of a peak.  Set if automated threshold finds too many or few peaks
%CM=set_bead_peak_threshold(CM, 200);
CM=set_FITC_channel_name(CM, FITC_channel_name);
% Ignore channel data for ith channel if below 10^[value(i)]
CM=set_translation_channel_min(CM,[2,2,2]);

settings = TASBESettings();
settings = setSetting(settings, 'path', 'plots');
% When dealing with very strong fluorescence, use secondary channel to segment
%settings = setSetting(settings,'SecondaryBeadChannel','PE-Texas_Red-A');
CM = add_filter(CM,autogate);

% Execute and save the model
CM=resolve(CM, settings);
%CM = 1
endfunction

