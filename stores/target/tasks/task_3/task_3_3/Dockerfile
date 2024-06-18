FROM ubuntu:22.04

## Install specific node.js version
# Source: https://stackoverflow.com/a/57546198
ENV NODE_VERSION=18.14.2
RUN apt-get -y update
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

## Use WORKDIR prior to npm installations
# Source: https://stackoverflow.com/a/65443098
WORKDIR /usr/app

COPY package.json .
COPY package-lock.json .
RUN npm clean-install

COPY unique_products_urls.json .

COPY src src
COPY last_products_info_extraction.js .

CMD ["node", "./last_products_info_extraction.js"]
