.PHONY: run test clean venv install typecheck lint fix help check_venv format

# Variáveis
PYTHON = .venv/bin/python3
SRC_DIR = src
MAIN_FILE = $(SRC_DIR)/main.py
VENV_PATH = .venv

# Verificação de ambiente virtual
check_venv:
	@if [ ! -d $(VENV_PATH) ]; then \
		echo "Ambiente virtual não encontrado. Execute 'make venv' primeiro."; \
		exit 1; \
	fi
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Ambiente virtual não está ativado. Execute 'source $(VENV_PATH)/bin/activate' primeiro."; \
		exit 1; \
	fi
	@if [ "$$VIRTUAL_ENV" != "$$VIRTUAL_ENV" ] || ! echo "$$VIRTUAL_ENV" | grep -q "$(VENV_PATH)"; then \
		echo "Ambiente virtual incorreto ativado. Execute 'source $(VENV_PATH)/bin/activate'."; \
		exit 1; \
	fi

# Target para criar ambiente virtual
venv:
	python3 -m venv $(VENV_PATH)
	@echo "Ambiente virtual criado em $(VENV_PATH)/. Use 'source $(VENV_PATH)/bin/activate' para ativar."

# Target para executar o programa principal
run: check_venv
	$(PYTHON) $(MAIN_FILE)

# Target para executar os testes
test: check_venv
	$(PYTHON) -m unittest discover -s $(SRC_DIR)

# Target para limpar arquivos cache
clean:
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf .mypy_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Target para verificar tipagem com mypy
typecheck: check_venv
	$(PYTHON) -m mypy --strict $(SRC_DIR)

# Target para verificar estilo de código com flake8
lint: check_venv
	$(PYTHON) -m flake8 $(SRC_DIR)

# Target para corrigir problemas de lint
fix: check_venv
	@echo "Removendo importações não utilizadas..."
	@$(PYTHON) -m autoflake --remove-all-unused-imports --recursive --in-place $(SRC_DIR)
	@echo "Corrigindo problemas de comprimento de linha..."
	@$(PYTHON) -m autopep8 --select=E501 --in-place --recursive $(SRC_DIR)
	@echo "Problemas de lint corrigidos. Execute 'make lint' para verificar os resultados."

# Target para formatar o código
format: check_venv
	@echo "Formatando o código com isort..."
	@$(PYTHON) -m isort $(SRC_DIR)
	@echo "Formatando o código com black..."
	@$(PYTHON) -m black $(SRC_DIR)
	@echo "Formatando o código com autopep8..."
	@$(PYTHON) -m autopep8 --in-place --aggressive --aggressive $(SRC_DIR)/*.py
	@echo "Código formatado com sucesso!"

# Target para instalar dependências
install: venv
	@echo "Instalando dependências..."
	$(VENV_PATH)/bin/pip install --upgrade pip
	$(VENV_PATH)/bin/pip install flake8 mypy black isort autopep8 autoflake
	@if [ -f requirements.txt ]; then \
		$(VENV_PATH)/bin/pip install -r requirements.txt; \
	else \
		echo "Arquivo requirements.txt não encontrado."; \
	fi
	@echo "Dependências instaladas com sucesso!"

# Help - exibe comandos disponíveis
help:
	@echo "Comandos disponíveis:"
	@echo "  make venv       - Cria ambiente virtual Python"
	@echo "  make install    - Instala dependências no ambiente virtual"
	@echo "  make run        - Executa o programa principal"
	@echo "  make test       - Executa os testes unitários"
	@echo "  make clean      - Remove arquivos de cache"
	@echo "  make format     - Formata o código usando black, isort e autopep8"
	@echo "  make fix        - Corrige problemas simples de lint automaticamente"
	@echo "  make lint       - Verifica estilo de código com flake8"
	@echo "  make typecheck  - Verifica tipagem com mypy"
	@echo "  make help       - Exibe esta mensagem de ajuda" 