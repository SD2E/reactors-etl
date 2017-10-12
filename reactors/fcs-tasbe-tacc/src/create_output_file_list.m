function [output_list] = create_output_file_list(list,label,files)

  strcmp(typeinfo(list), 'scalar')

  if strcmp(typeinfo(list), 'cell') ==1
    output_list = list
  else
    output_list = {}
  endif

  output_list 
  list
  label
  files

  entity.label = label
  entity.files = {}
  for i =1:length(files)
    entity.files{i} = files{i}
  endfor

  entity
  output_list

  output_list{length(output_list)+1} = entity
endfunction
