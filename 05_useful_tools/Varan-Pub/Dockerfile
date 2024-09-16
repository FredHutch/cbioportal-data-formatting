# Filename: PythonVaran
FROM buschlab/vep:110-GRCh37
USER root
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&\
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev openssl git &&\
    apt-get install -y software-properties-common ca-certificates &&\
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libssl-dev libreadline-dev libffi-dev wget libbz2-dev libsqlite3-dev vcftools bcftools && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /python && cd /python && \
    wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz && \
    tar -zxvf Python-3.11.1.tgz && \
    cd Python-3.11.1 && \
    ls -lhR && \
    ./configure --enable-optimizations && \
    make install && \
    rm -rf /python

COPY . /
WORKDIR /
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r oncokb-annotator/requirements/pip3.txt
RUN python3 -m pip install -r oncokb-annotator/requirements/common.txt
#ENV VCF2MAF_URL https://api.github.com/repos/mskcc/vcf2maf/tarball/v1.6.21
# RUN curl -L -o mskcc-vcf2maf.tar.gz $VCF2MAF_URL; tar -zxf mskcc-vcf2maf.tar.gz;
# RUN rm mskcc-vcf2maf.tar.gz

CMD [ "bash"]
