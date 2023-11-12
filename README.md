# Basic Python Project Framework


Gera de forma automatica uma estrutura básica de pastas e arquivos para iniciar um novo projeto Python

### Objetivo Geral

O seguinte projeto objetiva a criação de pacote python responsável por criar uma estrura básica, de forma automática, para  um projeto Python, gerando todas as pastas e arquivos minimamente necessários para organizar um projeto.

por estrutura básica chamamos a seguinte estrutura:

    --| projeto_exemplo
        --| docs
        --| projeto_exemplo
                __init__.py
                main.py
        -- | testes
                __init__.py
                test_base.py
        -- | venv
            . instala-se pacotes básicos como pandas e pytest
        .gitignore # por padrão apenas ignorando o venv/*
        README.md
