# QA Python Automation Lab

Практический проект для изучения QA-автоматизации на Python. Он продолжает идеи
`qa-sql-lab` (проверки качества данных с известным базовым уровнем дефектов) и
`qa-ts-automation-lab` (API/UI-тесты, тестовые данные, отчёты и CI).

## Что внутри

| Каталог | Назначение |
| --- | --- |
| `src/qa_python_lab/` | Локальный HTTP-сервер, API-клиент, правила качества данных и генератор баг-репорта |
| `tests/api/` | Позитивные, негативные и контрактные API-проверки |
| `tests/data/` | Контракт схемы SQLite, проверки качества данных и обнаружения новых дефектов |
| `tests/ui/` | Проверка страницы в Chromium через Playwright |
| `data/` | Учебные данные с намеренными ошибками |
| `test-cases/`, `bug-reports/` | Примеры ручного тест-кейса и баг-репорта |
| `qa-report/` | Генерируемая сводка прогона в JSON и Markdown (исключена из Git) |
| `.github/workflows/`, `.gitlab-ci.yml` | Отдельные CI-задачи для основных и браузерных тестов |

API и UI-тесты используют сервер, который стартует на `127.0.0.1` в фикстуре
pytest. Доступ в интернет и внешние тестовые сервисы им не нужны.

## Быстрый старт

Требуется Python 3.11 или новее. В PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[test]'
python -m pytest
```

По умолчанию запускаются API, проверки данных и утилит; браузерный тест
исключён. Для него дополнительно установите Playwright и Chromium:

```powershell
python -m pip install -e '.[test,ui]'
$env:PLAYWRIGHT_BROWSERS_PATH = (Join-Path (Get-Location) '.venv\browsers')
python -m playwright install chromium
python -m pytest -m ui
```

Полезные выборки:

```powershell
python -m pytest -m api
python -m pytest -m contract
python -m pytest -m data
python -m pytest -m smoke
python -m pytest -m 'not ui' --junitxml=qa-report/results.xml
```

`-m smoke` запускает только основной API-сценарий без браузера; для браузерной
проверки используйте `-m ui`. Каждый pytest-прогон создаёт
`qa-report/qa-summary.json` и `qa-report/qa-summary.md`: там есть итог каждого
выбранного теста, теги, время выполнения и статус контрольного правила.
JUnit XML можно прикрепить к CI-прогону. Папка `qa-report/` не хранится в Git.
Правила подсчёта описаны в [документации](docs/qa_reporting.md).

Запуск основных тестов в Docker:

```powershell
docker build -t qa-python-automation-lab .
docker run --rm qa-python-automation-lab
```

## Упражнения

1. Добавьте новый API-маршрут и проверьте успешный ответ, ошибку и контракт.
2. Добавьте намеренный дефект в `data/fixture.sql`, правило в `data_quality.py`
   и ожидаемое значение в `BASELINE`.
3. Исправьте один дефект в данных и обновите базовый уровень после проверки.
4. Расширьте `BugReport` для своего формата описания ошибок.

Базовый уровень качества данных означает ожидаемое число дефектов в учебной
фикстуре. Изменение этого числа видно как регрессия или исправление, поэтому
ожидаемые значения меняют осознанно после анализа данных.
