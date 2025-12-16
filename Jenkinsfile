pipeline {
    // 1. Agent: Use the official Python Playwright Docker image
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:latest' 
            args '--shm-size=2g' 
        }
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Fetching code from GitHub..."
                git credentialsId: 'github-pat', url: 'https://github.com/Sindhura18/Playwright.git'
            }
        }

        stage('Install & Run Tests') {
            steps {
                // Since this runs inside the Playwright Docker agent, 'sh' works fine
                sh """
                pip install -r requirements.txt
                pytest tests/ --junitxml=test-results/junit-report.xml
                """
            }
        }
    }

    // Post-build actions for reporting and cleanup
    post {
        always {
            // These steps run on the container launched by the successful stage
            // We use 'script' to handle the file operations if needed, but it should work directly now.
            
            // 1. Publish JUnit results
            junit 'test-results/junit-report.xml'

            // 2. Publish the detailed HTML report
            publishHTML(target: [
                allowMissing: true, 
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'playwright-report', 
                reportFiles: 'index.html',
                reportName: 'Playwright HTML Report'
            ])

            // 3. Archive artifacts 
            archiveArtifacts artifacts: '**/*.log, **/*.png', fingerprint: true
            
            // 4. Clean up the Jenkins workspace (this step requires the FilePath context)
            cleanWs() 
        }
    }
}
