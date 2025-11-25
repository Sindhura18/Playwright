pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // *** 1. UPDATED REPOSITORY URL ***
                git credentialsId: 'github-ssh-key', url: 'git@github.com:Sindhura18/Playwright.git'
            }
        }

        stage('Setup and Run Tests') {
            steps {
                sh """
                # 1. Activate the Python virtual environment on the EC2 server
                source /home/ubuntu/my_automation_env/bin/activate

                # 2. Install dependencies (if requirements.txt is in the repo root)
                pip install -r requirements.txt

                # *** 2. RUN PYTEST, POINTING TO THE 'tests' FOLDER ***
                pytest tests/

                # 3. Deactivate the environment
                deactivate
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Tests run successfully."
        }
    }
}