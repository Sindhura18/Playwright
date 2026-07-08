pipeline {
    agent any

    // Re-runs the suite every 2 hours so Grafana has a continuous stream of
    // pass/fail/duration history to chart, not just on-demand runs.
    triggers {
        cron('H */2 * * *')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Fetching code from GitHub..."
                git credentialsId: 'github-pat', url: 'https://github.com/Sindhura18/Playwright.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh """
                python3 -m venv venv
                . venv/bin/activate
                pip install --no-cache-dir -r requirements.txt
                playwright install chromium
                """
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([file(credentialsId: 'orangehrm-playwright-dotenv', variable: 'DOTENV_FILE')]) {
                    sh """
                    cp \$DOTENV_FILE .env
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results/junit-report.xml
                    """
                }
            }
        }
    }

    post {
        always {
            junit 'test-results/junit-report.xml'

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Playwright HTML Report'
            ])

            archiveArtifacts artifacts: 'report.html, screenshots/**', allowEmptyArchive: true, fingerprint: true
            cleanWs()
        }
    }
}
