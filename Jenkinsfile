pipeline {
    agent any

    stages {
        // Stage 1 is automatic (Declarative Checkout SCM)

        stage('Checkout Code') {
            steps {
                // Use HTTPS URL and the PAT credential (ID: github-pat)
                // This step replaces the previous complex SSH logic.
                git credentialsId: 'github-pat', url: 'https://github.com/Sindhura18/Playwright.git'
            }
        }

        stage('Setup and Run Tests') {
            steps {
                sh """
                source /home/ubuntu/my_automation_env/bin/activate
                pip install -r requirements.txt
                pytest tests/
                deactivate
                """
            }
        }
    }
}