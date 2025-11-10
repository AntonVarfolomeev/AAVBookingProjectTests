pipeline {
    agent any

    environment {
        ENVIRONMENT = 'PROD'
        TEST_BASE_URL = 'https://restful-booker.herokuapp.com'   // на PROD оставляем тот же URL, если он совпадает
        PROD_BASE_URL = 'https://restful-booker.herokuapp.com'   // реальный PROD URL
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                   . .venv/bin/activate
                   echo "Environment: $ENVIRONMENT"
                   echo "Base URL: $PROD_BASE_URL"
                   pytest tests --alluredir=allure-results --tb=short -q
                '''
            }
        }

        stage('Allure Report') {
            steps {
                sh 'allure generate allure-results --clean -o allure-report'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
        }
    }
}