

function [channel] = create_color_model(name,label,wavelength,center,width,plot_color)

    channel.name = name
    channel.Laser = wavelength
    channel.FilterCenter = center
    channel.FilterWidth = width
    channel.PseudoUnits = 0
    channel.PrintName = label
    channel.LineSpec = plot_color

endfunction
