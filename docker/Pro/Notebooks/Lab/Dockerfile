ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ENV INSTALL_ZSH="1"
ENV INSTALL_SLICER="1"
#ENV INSTALL_FREESURFER="1"
ENV INSTALL_ITKSNAP="1"
ENV INSTALL_QUPATH="1"
ENV INSTALL_MITK="1"
ENV INSTALL_NAPARI="1"

USER 1000720000

CMD bash -c "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
  --NotebookApp.notebook_dir=/home/maia-user \
  --NotebookApp.token='' \
  --NotebookApp.password='' \
  --NotebookApp.base_url=${NB_PREFIX} \
  --NotebookApp.allow_origin='*' \
  --NotebookApp.disable_check_xsrf=True"

ENTRYPOINT ["bash", "/opt/start.sh"]
