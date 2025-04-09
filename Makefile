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
	@expected_venv="$$(pwd)/$(VENV_PATH)"; \
	if [ "$$VIRTUAL_ENV" != "$$expected_venv" ]; then \
		echo "Ambiente virtual incorreto ativado. Execute 'source $(VENV_PATH)/bin/activate'."; \
		exit 1; \
	fi

# Target para criar ambiente virtual
venv:
	python3 -m venv $(VENV_PATH)
	@echo "Ambiente virtual criado em $(VENV_PATH)/. Use 'source $(VENV_PATH)/bin/activate' para ativar."

# Target para instalar dependências
install: check_venv
	@echo "Instalando dependências..."
	$(VENV_PATH)/bin/pip install --upgrade pip
	$(VENV_PATH)/bin/pip install flake8 mypy black isort autopep8 autoflake
	@if [ -f requirements.txt ]; then \
		$(VENV_PATH)/bin/pip install -r requirements.txt; \
	else \
		echo "Arquivo requirements.txt não encontrado."; \
	fi
	@echo "Dependências instaladas com sucesso!"

# Target para executar o programa principal
run: check_venv
	$(PYTHON) $(MAIN_FILE)

# Target para executar os testes
test: check_venv
	$(PYTHON) -m unittest discover -s $(SRC_DIR)

clean:
	@echo "Limpando arquivos temporários..."
	@rm -rf $(SRC_DIR)/__pycache__
	@rm -rf .mypy_cache .pytest_cache
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@echo "Limpeza concluída!"

# Target para verificar tipagem com mypy
typecheck: check_venv
	$(PYTHON) -m mypy --strict $(SRC_DIR)

# Target para verificar estilo de código com flake8
lint: check_venv
	$(PYTHON) -m flake8 $(SRC_DIR)

# Target para corrigir problemas de lint (modo restrito)
fix: check_venv
	@echo "Correções rigorosas em andamento..."
	@echo "Removendo imports/variáveis não utilizados..."
	@$(PYTHON) -m autoflake \
		--remove-all-unused-imports \
		--remove-unused-variables \
		--recursive \
		--in-place \
		$(SRC_DIR)
	@echo "Corrigindo todos os problemas PEP8 identificáveis..."
	@$(PYTHON) -m autopep8 \
		--aggressive \
		--aggressive \
		--recursive \
		--in-place \
		--select=E,W \
		--ignore=E501 \
		$(SRC_DIR)
	@echo "Verifique manualmente mudanças complexas!"

# Target para formatar o código (strict PEP8 + regras extras)
format: check_venv
	@echo "Formatação rigorosa em andamento..."
	@echo "Organizando imports com isort..."
	@$(PYTHON) -m isort \
		--profile=black \
		--atomic \
		$(SRC_DIR)
	@echo "Aplicando formatação Black..."
	@$(PYTHON) -m black \
		--line-length=79 \
		--target-version=py313 \
		$(SRC_DIR)
	@echo "Aplicando regras adicionais do PEP8..."
	@$(PYTHON) -m autopep8 \
		--aggressive \
		--aggressive \
		--recursive \
		--in-place \
		--select=E711,E713 \
		$(SRC_DIR)
	@echo "Formatação concluída. Verifique mudanças significativas!"

# Help - exibe comandos disponíveis
help:
	@echo "Comandos disponíveis:"
	@echo "  make venv       - Cria ambiente virtual Python (.venv)"
	@echo "  make install    - Instala dependências básicas + requirements.txt"
	@echo "  make run        - Executa o programa principal (main.py)"
	@echo "  make test       - Executa testes unitários na pasta src/tests"
	@echo "  make typecheck  - Verificação estática de tipos com mypy"
	@echo "  make lint       - Verificação de estilo com flake8"
	@echo "  make fix        - Correções automáticas (imports, formatação básica)"
	@echo "  make format     - Formatação completa (reorganiza imports, estilo PEP8)"
	@echo "  make clean      - Limpeza de arquivos temporários/cache"
	@echo "  make help       - Exibe esta ajuda"