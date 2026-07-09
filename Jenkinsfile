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
                git url: 'https://github.com/Sindhura18/Playwright.git'
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
                // .env lives outside the workspace, in the Jenkins container's
                // persistent volume, since this pipeline only ever runs on the
                // built-in node (no remote agents to distribute a credential to).
                sh """
                cp /var/jenkins_home/dotenv_upload.env .env
                . venv/bin/activate
                pytest tests/ --junitxml=test-results/junit-report.xml
                """
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
