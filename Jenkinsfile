// Jenkinsfile

pipeline {
    // Roda em qualquer agente Jenkins disponível
    agent any

    environment {
        
        BACKEND_IMAGE_NAME = "pfransozi/escola-devsecops"

        KUBE_CREDENTIALS_ID = "minikube-credentials"
    }

    stages {
        stage('1. Checkout') {
            steps {
                // Pega a versão mais recente do código do seu repositório
                git 'https://github.com/pFransozi/escola_projeto_devsecops.git'
            }
        }

        stage('2. Build e Testes do Backend') {
            steps {
                // Entra no diretório do backend para executar os comandos
                dir('sistema/backend') {
                    script {
                        // Conecta-se ao ambiente Docker do próprio Minikube.
                        // NOTA: O seu executor Jenkins precisa ter acesso ao comando 'minikube'.
                        sh 'eval $(minikube -p minikube docker-env)'

                        // Etapa de testes (placeholder). Idealmente, você rodaria seus testes aqui.
                        echo 'Rodando testes da aplicação...'
                        // Exemplo: sh 'pytest'

                        // Constrói a imagem Docker com uma tag única (o número do build)
                        def imageTag = "build-${env.BUILD_NUMBER}"
                        sh "docker build -t ${BACKEND_IMAGE_NAME}:${imageTag} ."
                        echo "Imagem ${BACKEND_IMAGE_NAME}:${imageTag} construída com sucesso."
                    }
                }
            }
        }

        stage('3. Deploy no Kubernetes') {
            steps {
                script {
                    def imageTag = "build-${env.BUILD_NUMBER}"
                    def fullImageName = "${BACKEND_IMAGE_NAME}:${imageTag}"

                    // Usa o arquivo de credencial do Kubernetes configurado no Jenkins
                    withKubeConfig([credentialsId: KUBE_CREDENTIALS_ID]) {
                        
                        // Atualiza a imagem do contêiner 'backend-app' no deployment 'web-deployment'
                        echo "Atualizando a imagem no Kubernetes para ${fullImageName}..."
                        sh "kubectl set image deployment/web-deployment backend-app=${fullImageName}"
                        
                        // Espera a atualização terminar e verifica o status para garantir o sucesso
                        echo "Verificando o status da implantação..."
                        sh "kubectl rollout status deployment/web-deployment"
                    }
                }
            }
        }
    }

    post {
        always {
            // Limpa o ambiente, desconectando do Docker do Minikube
            sh 'eval $(minikube -p minikube docker-env -u)'
            echo 'Pipeline concluído.'
        }
    }
}
