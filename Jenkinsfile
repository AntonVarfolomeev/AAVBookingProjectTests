pipeline {
    agent any

    parameters {
        string(name: 'ENVIRONMENT', defaultValue: 'PROD', description: 'Environment to run tests against')
    }

    environment {
        ENVIRONMENT = "${params.ENVIRONMENT}"
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
                   export ENVIRONMENT="${ENVIRONMENT}"
                   export PROD_BASE_URL="${PROD_BASE_URL}"
                   export TEST_BASE_URL="${TEST_BASE_URL}"
                   echo "Environment: $ENVIRONMENT"
                   echo "PROD Base URL: $PROD_BASE_URL"
                   echo "TEST Base URL: $TEST_BASE_URL"
                   python -m pytest --alluredir=allure-results --tb=short -q
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