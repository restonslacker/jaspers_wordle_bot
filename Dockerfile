FROM continuumio/miniconda3

RUN conda create -n wordle \
    && conda update --all --name wordle \
    && conda clean --all -y
