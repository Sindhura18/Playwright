pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                // Fetch code using HTTPS and the PAT credential (ID: github-pat)
                git credentialsId: 'github-pat', url: 'https://github.com/Sindhura18/Playwright.git'
            }
        }

        stage('Setup and Run Tests') {
            steps {
                sh """
                # 1. Create venv locally inside the Jenkins workspace (./venv)
                python3 -m venv venv

                # 2. Activate the venv from the local path
                . venv/bin/activate

                # 3. Install dependencies (playwright will be installed here)
                pip install -r requirements.txt

                # 4. Install Playwright browser dependencies (CRITICAL STEP)
                playwright install

                # 5. Run Playwright tests
                pytest tests/

                # 6. Deactivate the virtual environment
                deactivate
                """
            }
        }
    }
}