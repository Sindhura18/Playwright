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

                # 2. Activate the venv from the local path (Using '.' for shell compatibility)
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

    post {
        // 'always' ensures these steps run regardless of the test failure/success
        always {
            // 1. Publish the main HTML report
            // The report and screenshots are in the 'PythonProjecttest' directory.
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'PythonProjecttest', // Confirmed folder name
                reportFiles: 'report.html',     // Confirmed report file name
                reportName: 'Playwright Report'
            ])

            // 2. Archive all artifacts, including the screenshots inside the report directory
            archiveArtifacts artifacts: 'PythonProjecttest/**/*', fingerprint: true

            // Optional: Clean up the workspace to free up disk space after the build
            cleanWs()
        }
    }
}