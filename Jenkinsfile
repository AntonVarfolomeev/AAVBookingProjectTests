pipeline {
    agent any

    environment {
        ENVIRONMENT = 'TEST' // можно менять на PROD через Jenkins параметры
    }

    stages {
        stage('Checkout') {
            steps {
                // Получаем код из Git
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                // Создаем виртуальное окружение и устанавливаем зависимости
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Запуск всех тестов с генерацией allure-results
                sh '. .venv/bin/activate && pytest tests --alluredir=allure-results --tb=short -q'
            }
        }

        stage('Allure Report') {
            steps {
                // Генерация отчета Allure
                sh 'allure generate allure-results --clean -o allure-report'
            }
        }
    }

    post {
        always {
            // Архивация результатов Allure
            archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
            // Можно добавить публикацию Allure через плагин Jenkins
        }
    }
}