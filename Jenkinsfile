pipeline {
    agent any

    stages {
        stage('Declarative: Checkout SCM') {
            // This stage is automatic and uses HTTPS to get the Jenkinsfile.
            // DO NOT PUT CUSTOM CODE HERE.
        }

        stage('Checkout Code') {
            steps {
                // Force Git to ignore strict host key checking for this build run
                sh 'git config --global core.sshCommand "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"'

                // Use the sshagent wrapper to inject the private key
                sshagent(['github-ssh-key']) {
                    // Fetch the code using the SSH URL
                    git credentialsId: 'github-ssh-key', url: 'git@github.com:Sindhura18/Playwright.git'
                }
            }
        }

        stage('Setup and Run Tests') {
            steps {
                sh """
                # Your environment setup commands remain here
                source /home/ubuntu/my_automation_env/bin/activate
                pip install -r requirements.txt
                pytest tests/
                deactivate
                """
            }
        }
    }
}