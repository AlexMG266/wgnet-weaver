# wgnet-weaver
CLI tool for automated WireGuard mesh network management. Generate, manage, and monitor secure VPN topologies for distributed teams.

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Badge en Desarrollo](https://img.shields.io/badge/STATUS-IN%20DEVELOP-green)


## Instalación y ejecución

### Requisitos

- Python 3.12+
- `make` (GNU Make)
- Dependencias de Python listadas en `requirements.txt`

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/alex-mosquera-gundin/wgnet-weaver.git
cd wgnet-weaver
```

2. Instalar dependencias en el entorno y ejecutar el proyecto:

````bash
make install  # Instala dependencias
python -m netweaver --help
make run ARGS="--help"  
make run ARGS="generate -i examples/example001.json -o ./configs
````