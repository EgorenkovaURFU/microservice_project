FROM python:3.8
WORKDIR /usr/src/app
COPY ./src ./
COPY ./requirements.txt ./
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
RUN pip install --no-cache-dir -r requirements.txt
CMD ['python', ./plots.py]