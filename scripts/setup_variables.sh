#!/bin/bash

ENV_VARS="

# Variabili per Java
export JAVA_BIN=\$(which java)
export JAVA_HOME=\$(dirname \$(dirname \$(readlink -f \$JAVA_BIN)))
export JCC_JDK=\$JAVA_HOME
export JCC_INCLUDES=\$JAVA_HOME/include:\$JAVA_HOME/include/linux
export JCC_LFLAGS=\"-L\$JAVA_HOME/lib/server:-ljvm\"

# Variabili per Python
export PYTHON_BIN=\$(which python3)
export PREFIX_PYTHON=\$(dirname \$(dirname \$(readlink -f \$PYTHON_BIN)))
export PYTHON=\$PREFIX_PYTHON/bin/python3
export JCC=\"\$PYTHON -m jcc\"

# Percorso delle librerie Java
export LD_LIBRARY_PATH=\"\$JAVA_HOME/lib/server:\$LD_LIBRARY_PATH\"
"

BASHRC_FILE="$HOME/.bashrc"

echo -e "$ENV_VARS" >> "$BASHRC_FILE"

source "$BASHRC_FILE"