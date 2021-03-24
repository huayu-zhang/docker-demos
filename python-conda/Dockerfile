FROM continuumio/miniconda3

ARG ENV_NAME=conda_env

COPY . /home/

RUN conda env create -f /home/environment.yml
RUN echo "source activate "$ENV_NAME > ~/.bashrc
ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH

CMD "/bin/bash"

