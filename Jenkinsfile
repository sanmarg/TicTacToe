pipeline {
    agent any

    stages {
        stage('Cloning the repo') {
            steps {
                echo 'Clonning the repo'
                sh 'rm -rf TicTacToe'
                sh 'git clone https://github.com/sanmarg/TicTacToe'
                
            }
        }
        stage('Docker...') {
            steps {
                echo 'Building and deploying containers'
                sh 'docker rmi -f tictactoe'
                
                dir('TicTacToe') {
                sh 'docker build -t tictactoe .'
                sh 'docker run -itd --net=host tictactoe'
                }
            }
        }
        stage('Checking...') {
            steps {
                sh 'curl -I http://localhost:5000/'
            }
        }
    }
}
