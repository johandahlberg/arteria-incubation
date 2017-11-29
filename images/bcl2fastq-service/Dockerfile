FROM centos:7

WORKDIR /tmp
RUN yum install -y epel-release
RUN yum update -y
RUN yum install -y unzip python-pip python-virtualenv git gcc-c++ wget
RUN wget ftp://webdata2:webdata2@ussd-ftp.illumina.com/downloads/software/bcl2fastq/bcl2fastq2-v2.17.1.14-Linux-x86_64.zip
RUN unzip bcl2fastq2-v2.17.1.14-Linux-x86_64.zip
RUN yum install -y bcl2fastq2-v2.17.1.14-Linux-x86_64.rpm

# setup arteria-runfolder service
WORKDIR /
RUN git clone https://github.com/arteria-project/arteria-bcl2fastq.git
RUN pip install -r ./arteria-bcl2fastq/requirements/dev ./arteria-bcl2fastq
COPY app.config ./arteria-bcl2fastq/config/
RUN mkdir /bcl2fastq_logs

EXPOSE 80
CMD bcl2fastq-ws --debug --port 80 --config ./arteria-bcl2fastq/config/

