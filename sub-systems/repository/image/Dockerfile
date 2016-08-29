FROM hub.deepin.io/deepin/sshd

RUN apt-get update && \
    yes | DEBIAN_FRONTEND=noninteractive apt-get install python3-apt python3-flask python3-tornado git && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists
