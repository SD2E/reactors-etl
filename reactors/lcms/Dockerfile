FROM python:2.7.13

ADD src/lcms.py /

RUN pip install argparse
RUN pip install pandas
RUN pip install pyteomics
RUN pip install lxml

CMD python ./lcms.py --in $IN --out $OUT
