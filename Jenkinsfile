pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                // Fetch code using HTTPS and the PAT credential (ID: github-pat)
                // This resolves all prior SSH authentication issues.
                git credentialsId: 'github-pat', url: 'https://github.com/Sindhura18/Playwright.git'
            }
        }

        stage('Setup and Run Tests') {
            steps {
                sh """
                # 1. Activate the Python Virtual Environment using the '.' command
                . /home/ubuntu/my_automation_env/bin/activate

                # 2. Install dependencies
                pip install -r requirements.txt

                # 3. Run Playwright tests
                pytest tests/

                # 4. Deactivate the virtual environment
                deactivate
                """
            }
        }
    }
}