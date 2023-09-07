FROM python:3.11-slim-bookworm

ARG UPDATECLI_VERSION=v0.54.0

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Updatecli
RUN curl -sL -o /tmp/updatecli_amd64.deb https://github.com/updatecli/updatecli/releases/download/$UPDATECLI_VERSION/updatecli_amd64.deb && \
    apt install /tmp/updatecli_amd64.deb

# Create the virtualenv and add it to the path
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY helm_dependency_bumper.py /helm_dependency_bumper.py

ENTRYPOINT [ "/entrypoint.sh" ]
