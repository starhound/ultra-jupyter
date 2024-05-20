# Start from the Jupyter base-notebook image
FROM jupyter/base-notebook:latest

# Switch to root to install dependencies
USER root

# Install wget, necessary tools, and language-specific dependencies
RUN apt-get update && apt-get install -y wget apt-transport-https gnupg nodejs npm \
    ruby ruby-dev curl python3-pip gcc make cmake openjdk-11-jdk libzmq3-dev libssl-dev \
    erlang-dev erlang-tools erlang-eunit libtinfo-dev libzmq3-dev libcairo2-dev libpango1.0-dev libmagic-dev libblas-dev liblapack-dev \
    lua5.3 luarocks php-cli php-pear php-dev r-base lsb-release cpanminus \
    nettle-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install mamba
RUN conda install -c conda-forge mamba

RUN git clone https://github.com/guysv/ilua.git --recurse-submodules && \
    cd ilua && \
    pip install -e . --user && \
    python setup.py install_data -d ~/.local 

# Install .NET SDK 8.0
RUN wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-8.0

# Install IJava
RUN git clone https://github.com/SpencerPark/IJava.git && \
    cd IJava && \
    ./gradlew installKernel

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    source $HOME/.cargo/env

# Install Go
RUN wget https://golang.org/dl/go1.18.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.18.4.linux-amd64.tar.gz && \
    rm go1.18.4.linux-amd64.tar.gz

# Install Matlab
RUN pip install matlab matlab_kernel

# Install Pike
RUN pip install pike_kernel
RUN python -m pike_kernel.install

# Install ILua
RUN pip install ilua

# Install Kotlin
RUN pip install kotlin-jupyter-kernel 

# Switch to jovyan user for installing dotnet interactive in Jupyter
USER ${NB_UID}

# Set environment variables for the jovyan user
ENV PATH="/home/jovyan/.dotnet/tools:${PATH}"
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/home/jovyan/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# Create the .dotnet directory and set the appropriate permissions
RUN mkdir -p /home/jovyan/.dotnet && \
    chown -R ${NB_UID}:users /home/jovyan/.dotnet

# Install .NET Interactive
RUN dotnet tool install -g Microsoft.dotnet-interactive

# Ensure the Jupyter kernels and runtime directories exist and are writable
USER root
RUN mkdir -p /home/jovyan/.local/share/jupyter/kernels /home/jovyan/.local/share/jupyter/runtime && \
    chown -R ${NB_UID}:${NB_GID} /home/jovyan/.local/share/jupyter
USER ${NB_UID}

# Run dotnet interactive install as jovyan user
RUN /home/jovyan/.dotnet/tools/dotnet-interactive jupyter install

# Switch to root to install various language kernels
USER root

RUN pip install jupyter-c-kernel
RUN install_c_kernel

# Install ijavascript kernel
RUN npm install -g ijavascript && \
    ijsinstall --install=global

# Install ITypeScript kernel
RUN npm install -g itypescript && \
    its --install=global

# Install Bash kernel
RUN pip install bash_kernel && \
    python -m bash_kernel.install

# Install SQL kernel
RUN pip install mariadb_kernel
RUN python -m mariadb_kernel.install

# Install IRuby kernel
RUN gem install iruby && \
    iruby register --force

# Install Rust kernel (Evcxr)
RUN /home/jovyan/.cargo/bin/cargo install evcxr_jupyter && \
    /home/jovyan/.cargo/bin/evcxr_jupyter --install

# Install Scala kernel (almond)
RUN curl -Lo coursier https://git.io/coursier-cli && \
    chmod +x coursier && \
    ./coursier launch --fork almond -- --install && \
    rm coursier

# zsh kernel
RUN python -m pip install notebook zsh_jupyter_kernel

# Install Julia kernel
RUN curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-1.8.5-linux-x86_64.tar.gz" | tar -xz -C /opt/ && \
    ln -s /opt/julia-1.8.5/bin/julia /usr/local/bin/julia && \
    julia -e 'using Pkg; Pkg.add("IJulia"); using IJulia; IJulia.installkernel("Julia")'

# Install Go kernel (gophernotes)
RUN go install github.com/gopherdata/gophernotes@latest && \
    mkdir -p /home/jovyan/.local/share/jupyter/kernels/gophernotes && \
    cp $GOPATH/pkg/mod/github.com/gopherdata/gophernotes@*/kernel/* /home/jovyan/.local/share/jupyter/kernels/gophernotes

# Install R kernel
RUN R -e "install.packages('IRkernel', repos='http://cran.r-project.org')" && \
     R -e "IRkernel::installspec()"

# Install Octave
RUN pip install octave_kernel
RUN python -m octave_kernel install --user

# Install C/C++ kernel (xeus-cling)
RUN conda install -c conda-forge xeus-cling

# Install Emacs Lisp
RUN git clone https://github.com/shwina/ielisp && \
    cd ielisp && \
    python install.py

# Install Elm
RUN pip install elm_kernel
RUN python -m elm_kernel.install

# Install Erlang, Elixir, LFE
RUN wget https://github.com/filmor/ierl/releases/download/v0.6.0/ierl && \
    chmod +x ierl && \
    ./ierl install erlang && \
    ./ierl install elixir && \
    ./ierl install lfe

# Install Whitespace (lol)
RUN apt install libzmq3-dev libzmq5
RUN git clone https://github.com/makiuchi-d/whitenote.git && cd whitenote && go install . && jupyter kernelspec install --name=whitenote --user ./kernel

# Install Dart
RUN apt-get update && apt-get install -y apt-transport-https && \
    wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list && \
    apt-get update && apt-get install -y dart
# Set Dart PATH
ENV PATH="/usr/lib/dart/bin:${PATH}"

# Install Dart Jupyter Kernel
RUN git clone https://github.com/vickumar1981/jupyter-dart-kernel && \
    cd jupyter-dart-kernel && \
    pip install -e ./ && \
    jupyter kernelspec install --user jupyterdartkernel

# Vim Script Kernel
RUN git clone https://github.com/mattn/vim_kernel && \
    cd vim_kernel && \
    python setup.py install && \
    python -m vim_kernel.install

# SSH Kernel
RUN pip install -U sshkernel
RUN python -m sshkernel install 

# Install required packages
RUN apt-get update && apt-get install -y python3-pip git libtinfo-dev libzmq3-dev libcairo2-dev libpango1.0-dev libmagic-dev libblas-dev liblapack-dev

# Install Haskell Stack
RUN curl -sSL https://get.haskellstack.org/ | sh

# Set environment variable for Stack root
ENV STACK_ROOT=/home/jovyan/.local/stack
ENV PATH=/home/jovyan/.local/bin:$PATH

# Install IHaskell
RUN git clone https://github.com/gibiansky/IHaskell && \
    cd IHaskell && \
    pip3 install --user -r requirements.txt && \
    stack install --fast && \
    ihaskell install --stack

# LiveScript Kernel
RUN npm install -g livescript jp-livescript
RUN jp-livescript-install

# Coconut 
RUN pip install coconut
RUN coconut --jupyter install 

# MicroPython
RUN pip install jupyter_micropython_kernel
RUN python -m jupyter_micropython_kernel.install

# Hy
RUN pip3 install hy
RUN pip3 install git+https://github.com/ekaschalk/jedhy.git
RUN pip3 install git+https://github.com/Calysto/calysto_hy.git
RUN python3 -m calysto_hy install

# Calysto Processing
RUN pip3 install --upgrade calysto_processing --user
RUN python3 -m calysto_processing install --user

# Calysto Scheme
RUN pip3 install --upgrade calysto-scheme
RUN python3 -m calysto_scheme install

# SetlX
RUN pip install isetlx
RUN python -m isetlx.install

# Dyalog APL
RUN pip install dyalog-jupyter-kernel
RUN python -m 'dyalog_kernel' install

# Ansible
RUN pip install ansible-kernel
RUN python -m ansible_kernel.install

# Dot
RUN apt-get install graphviz libann0 libcdt5 libcgraph6 libgts-0.7-5 libgts-bin libgvc6 libgvpr2 liblab-gamut1 libpathplan4
RUN pip install dot_kernel
RUN install-dot-kernel

# Common Workflow Language
RUN pip3 install cwltool
RUN pip install cwlkernel

# CircuitPython
RUN git clone https://github.com/adafruit/circuitpython_jupyter_kernel && \
    cd circuitpython_jupyter_kernel && \
    python3 setup.py install && \
    python3 -m circuitpython_kernel.install

# Fortran 
RUN apt install gfortran

RUN git clone https://github.com/ZedThree/jupyter-fortran-kernel && \
    cd jupyter-fortran-kernel && \
    pip install -e . && \
    jupyter-kernelspec install fortran_spec/

# Elasticsearch 
RUN pip3 install elasticsearch_kernel
RUN python3 -m elasticsearch_kernel.install

# Forth
RUN apt install gforth gforth-common gforth-lib
RUN git clone https://github.com/sohang3112/iforth && \
    cd iforth && \
    pip install -e . && \
    jupyter kernelspec install ./kernelspec --user

# ARM
RUN pip install arm-jupyter-kernel
RUN python -m arm_kernel.install

# Poetry
RUN apt install pipx -y
RUN pipx install poetry
RUN pip3 install --user poetry-kernel
RUN poetry init -n
RUN poetry add ipykernel

# Switch back to jovyan user
USER ${NB_UID}

RUN jupyter kernelspec list 

# Ensure the default command is correct
CMD ["start-notebook.sh"]
