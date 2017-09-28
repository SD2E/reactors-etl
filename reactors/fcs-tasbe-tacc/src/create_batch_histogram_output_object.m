function [output_object] = create_batch_histogram_output_object(plots,plots_folder,file,title)
  output_object.type = "batch_histogram"
  output_object.plots = plots
  output_object.plots_folder = plots_folder
  output_object.file = file 
  output_object.title = title
endfunction
