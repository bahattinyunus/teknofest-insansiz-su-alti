# 🔱 TEKNOFEST İSA Otonom Komut Seti

.PHONY: run test lint clean help

help:
	@echo "Komutlar:"
	@echo "  make run    - Command Center Dashboard'u başlatır"
	@echo "  make test   - Pytest ile tüm ünite testlerini çalıştırır"
	@echo "  make lint   - Flake8 ile kod standartlarını kontrol eder"
	@echo "  make clean  - __pycache__ ve geçici dosyaları temizler"

run:
	python src/dashboard.py

test:
	pytest tests/

lint:
	flake8 src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .flake8
