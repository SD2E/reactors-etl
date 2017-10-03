## Orig

```
CMD python /src/fc.py --config $CONFIG --octave-method-path /src/
```

### Warnings

fig2dev not available

Plots SHOULD be created in the working directory...

## Target COnfig 1

docker run -it -w="/home" -v $PWD:/home -e "CONFIG=fc.json" fcs bash


Hide the octave-workspace file using $HOME/.octaverc

https://stackoverflow.com/a/23636289


```
octave_core_file_name (".octave-workspace")
```

### Target command

```
CMD python /opt/scripts/fc.py --octave-method-path /opt/octave-methods --config $CONFIG 
```

### Singularity

[TODO] Build a Vagrant box emulating the TACC HPC environment for testing