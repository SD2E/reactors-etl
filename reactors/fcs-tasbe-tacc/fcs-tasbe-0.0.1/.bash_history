ls
python /opt/scripts/fc.py --octave-method-path /opt/scripts/ --label "Dox_0.1" --files "LacI-CAGop_B10_B10_P3.fcs" --type "geo_mean_std" --output "output.txt"
ls
python /opt/scripts/fc.py --octave-method-path /opt/scripts/ --label "Dox_0.1" --files "LacI-CAGop_B10_B10_P3.fcs" --type "geo_mean_std" --output "output.txt" > tester-internal.log
env > internal.env
exit
python -c "import os; print os.environ"
python -c "import os; print os.environ" > pythonenv.internal
exit
