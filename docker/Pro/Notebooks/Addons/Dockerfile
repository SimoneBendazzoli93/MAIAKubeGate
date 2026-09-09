ARG BASE_IMAGE
FROM ${BASE_IMAGE}
ARG DEBIAN_FRONTEND=noninteractive
USER root

ENV MATLAB_RELEASE=R2025b
COPY dependencies.txt /tmp/dependencies.txt

RUN apt-get update && \ 
    #apt-get install --no-install-recommends -y `cat /tmp/dependencies.txt` \
    apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* && \
    wget https://www.mathworks.com/mpm/glnxa64/mpm && chmod +x mpm

USER 1000720000
RUN sudo mkdir /opt/matlab && \
    sudo chmod -R 777 /opt/matlab && \
    sudo ./mpm install --release ${MATLAB_RELEASE} --products MATLAB --destination=/opt/matlab && \
    sudo ln -s /opt/matlab/bin/matlab /usr/bin/matlab

USER root
RUN apt update && apt install xvfb -y && \
    pip install jupyter-matlab-proxy --break-system-packages

RUN apt-get install r-base -y && apt-get install gdebi-core -y && wget https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2025.09.1-401-amd64.deb && \
    gdebi rstudio-server-2025.09.1-401-amd64.deb -n && \
    pip install jupyter-rsession-proxy --break-system-packages

#RUN pip install conda-store-server jupyterlab-conda-store

#RUN apt-get install python3-pyqt5.qtquick python3-pyqt5.qtsvg -y && pip install glueviz[recommended,qt]  glue-jupyterlab && pip install git+https://github.com/glue-viz/glue-jupyter.git


RUN pip install jupyter-ai jupyter-vscode-proxy --break-system-packages && pip install panel --break-system-packages

# watchfiles&& jupyter serverextension enable panel.io.jupyter_server_extension

RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.25/quarto-1.8.25-linux-amd64.deb && dpkg -i quarto-1.8.25-linux-amd64.deb && \
    #pip install glue-jupyterlab "glueviz[all,qt]" --break-system-packages && \
    apt-get install python3-pyqt5.qtquick python3-pyqt5.qtsvg -y

COPY Tools/Matlab/Matlab.desktop /etc/Matlab.desktop
COPY Tools/Matlab/Matlab_Logo.png /etc/Matlab_Logo.png
RUN chmod 777 /etc/Matlab.desktop && \
    chmod a+x /etc/Matlab.desktop

RUN pip install jupyterlab_nvdashboard --break-system-packages && \
    pip install jupyter-collaboration jupyter_app_launcher jupyter-resource-usage --break-system-packages
#RUN pip install "elyra[all]"
COPY start.sh /opt/start.sh

USER 1000720000
CMD ["jupyterhub-singleuser"]
ENTRYPOINT ["bash", "/opt/start.sh"]
