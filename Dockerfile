FROM python:3.13-alpine

# Java runtime — нужен только для Allure CLI
RUN apk add --no-cache openjdk17-jre curl tar

# Allure CLI — генерация HTML-отчёта внутри контейнера
RUN curl -fsSL -o /tmp/allure.tgz \
    https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz && \
    tar -zxf /tmp/allure.tgz -C /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm /tmp/allure.tgz

WORKDIR /app

# Зависимости — отдельный слой, кэшируется пока requirements.txt не изменился
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Исходный код (secrets исключены через .dockerignore)
COPY . .

# Дефолтный запуск — все тесты с Allure-результатами
CMD ["pytest", "-v", "--alluredir=allure-results"]
