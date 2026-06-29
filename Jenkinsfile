pipeline {
    agent any

    stages {
        stage('1. Checkout') {
            steps {
                echo '=== ÉTAPE 1 : Récupération du code source depuis Git ==='
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo '=== ÉTAPE 2 : Construction de l\'image Docker de l\'application ==='
                sh 'docker build -t app-devops .'
            }
        }

        stage('3. Run Tests') {
            steps {
                echo '=== ÉTAPE 3 : Exécution des tests unitaires et d\'intégration dans le conteneur ==='
                // Exécution des tests Pytest à l'intérieur du conteneur construit
                sh 'docker run --rm app-devops pytest /app/tests/'
            }
        }

        stage('4. Stop Old Containers') {
            steps {
                echo '=== ÉTAPE 4 : Arrêt et suppression des anciennes instances (cleanup) ==='
                sh 'docker compose down --remove-orphans || true'
            }
        }

        stage('5. Deploy with Docker Compose') {
            steps {
                echo '=== ÉTAPE 5 : Lancement du déploiement continu via Docker Compose ==='
                sh 'docker compose up -d --build'
            }
        }

        stage('6. Health Check') {
            steps {
                echo '=== ÉTAPE 6 : Vérification de la santé de l\'application (Health Check) ==='
                // Attente du démarrage complet des services (Postgres et Nginx compris)
                sleep 10
                // Le conteneur Jenkins n'étant pas sur le réseau de l'application,
                // le test est exécuté depuis un conteneur éphémère attaché à ce réseau,
                // plutôt que depuis "localhost" qui ne pointerait pas vers Nginx ici.
                sh 'docker run --rm --network helpdesk-pipeline_helpdesk-net curlimages/curl -f http://nginx/health'
            }
        }
    }

    post {
        always {
            echo '=== Fin du pipeline CI/CD ==='
        }
        success {
            echo '=== DÉPLOIEMENT RÉUSSI ET OPÉRATIONNEL ! ==='
        }
        failure {
            echo '=== ÉCHEC DU PIPELINE. VEUILLEZ VÉRIFIER LES LOGS DE LA MACHINE ==='
        }
    }
}