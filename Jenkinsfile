pipeline {
    agent {
        docker {
            image 'python:3.6'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout(scm)
            }
        }
        
        stage('Install') {
            steps {
                sh('pip install -r requirements.txt')
            }
        }

        stage('Run checks') {
            steps {
                sh('python -m xmlrunner discover tests --output-file junit.xml')
            }
        }
    }
    post {
        always {
            junit 'junit.xml'
        }
    }
}