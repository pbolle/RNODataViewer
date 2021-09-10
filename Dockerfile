FROM oci-reg-ztf.zeuthen.desy.de/radio/nu_radio_mc:latest
LABEL maintainer="The NuRadioReco Authors <physics-astro-nuradiomcdev@lists.uu.se>"
USER root

RUN apt-get update
RUN apt-get upgrade -y

# Install core dependencies
RUN pip install numpy scipy matplotlib tinydb>=4.1.1 tinydb-serialization aenum astropy radiotools>=0.2.0 h5py pyyaml peakutils requests pymongo dash plotly sphinx
RUN pip install cython
RUN pip install uproot awkward


# Install NuRadioReco
ADD RNODataViewer /usr/local/lib/python3.6/site-packages/RNODataViewer

USER   nuradio
EXPOSE 8049
WORKDIR /usr/local/lib/python3.6/site-packages/RNODataViewer/
CMD [ "python", "./monitoring.py","--port 8049", "--open-window"]