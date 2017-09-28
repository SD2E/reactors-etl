function [cm] = create_color_model_object(bead_file,blank_file,bead_model,bead_batch,translation_plot,noise_plot, fitc_channel_name,channel_mins)
  cm.bead_file = bead_file
  cm.blank_file = blank_file
  cm.bead_model = bead_model
  cm.bead_batch = bead_batch
  cm.fitc_channel_name = fitc_channel_name
  cm.translation_plot = translation_plot
  cm.noise_plot = noise_plot
  cm.channel_mins = channel_mins 

end
