FROM jenkins/jenkins:lts-jdk17

USER root

# Python + the OS-level shared libraries Chromium needs (installed once at build time
# via Playwright's own dependency resolver, so it always matches this Playwright
# version - the actual browser binary is downloaded per-build into the job's venv,
# which needs no root access).
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-venv python3-pip curl ca-certificates && \
    python3 -m venv /opt/pwvenv && \
    /opt/pwvenv/bin/pip install --no-cache-dir --upgrade pip playwright && \
    /opt/pwvenv/bin/playwright install-deps chromium && \
    rm -rf /opt/pwvenv /var/lib/apt/lists/*

# Plugins installed at image build time so a fresh container already has them,
# rather than relying on manual install through the setup wizard.
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins
