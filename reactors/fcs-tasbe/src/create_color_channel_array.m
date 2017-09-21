function array = create_color_channel_array(array)
  array
endfunction

%{
function [color_channel_array] = create_color_channel_array(channel,array)
  if(array == -1)
    color_channel_array = [channel]
  else
    color_channel_array = [array channel]
  endif

endfunction
%}
