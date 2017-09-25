function [output_list] = create_output_file_list(list,label,files)
  if list== -1
    output_list = {}
  else
    output_list = list
  endif
 
  entity.label = label
  entity.files = {}
  for i =1:length(files)
    entity.files{i} = files{i}
  endfor

  entity
  output_list{length(output_list)+1} = entity
endfunction
