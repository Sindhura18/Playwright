pipeline {
    // Defines where the entire pipeline runs (Built-In Node/master)
    agent { label 'EC2-Agent' }

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

                # 3. Install dependencies
                pip install -r requirements.txt

                # 4. Install Playwright browser dependencies
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
        // These steps run regardless of the test result
        always {
            // CRITICAL FIX: The node block provides the FilePath context required for file operations.
            node(label: 'master') {

                // Use 'dir' to navigate into the report directory for publishing
                dir('PythonProjecttest') {
                    // 1. Publish the main HTML report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.', // Now relative to PythonProjecttest directory
                        reportFiles: 'report.html',
                        reportName: 'Playwright Report'
                    ])
                }

                // 2. Archive all artifacts (screenshots, logs, etc.)
                archiveArtifacts artifacts: 'PythonProjecttest/**/*', fingerprint: true

                // 3. Clean up the entire workspace
                cleanWs()
            }
        }
    }
}