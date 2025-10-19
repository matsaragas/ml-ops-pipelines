pipeline {
    agent any

    environment {
        PYTHON = '/usr/bin/local/python3'
        MODEL_PATH = 'models/new_model/model.pkl'
        IMAGE = 'mlops-demo/model:staging'
    }

    stages {
        stage('Clone Repository') {
            steps {
                //Clone Repository
                script {
                   echo 'Cloning Github Repository'
                   checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-git-token', url: 'https://github.com/matsaragas/ml-ops-pipelines.git']])
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                python3 -m pip install --upgrade pip
                python3 -m pip install -r requirements.txt
                """
            }
        }

        stage('Step 1 - Load Metadata') {
            steps {
                sh "${PYTHON} scripts/load_metadata.py models/new_model/metadata.json"
            }
        }

        stage('Step 2 - Run Evaluation') {
            steps {
                sh "${PYTHON} scripts/run_evaluation.py ${MODEL_PATH}"
            }
        }

        stage('Step 3 - Generate Report') {
            steps {
                sh "${PYTHON} scripts/generate_report.py"
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'report.md, evaluation_results.json', fingerprint: true
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def metrics = readJSON file: 'evaluation_results.json'
                    if (metrics.accuracy < 0.9) {
                        error("Model accuracy below threshold. Stopping pipeline.")
                    }
                }
            }
        }

        stage('Step 4 - Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE} ."
            }
        }

        stage('Step 5 - Deploy to Staging') {
            steps {
                sh """
                docker stop ml_model_staging || true
                docker rm ml_model_staging || true
                docker run -d --name ml_model_staging -p 8080:8080 ${IMAGE}
                """
            }
        }

        stage('Step 6 - Smoke Tests') {
            steps {
                sh "${PYTHON} scripts/smoke_tests.py"
            }
        }

        stage('Step 7 - Manual Approval for Production') {
            steps {
                input message: 'Promote model to production?', ok: 'Deploy'
            }
        }

        stage('Step 8 - Deploy to Production') {
            steps {
                sh "docker tag ${IMAGE} mlops-demo/model:prod"
                sh "docker push mlops-demo/model:prod"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
