pipeline{
    agent {label 'agent-01'}

    stages{
        stage('Get Code'){
            steps{
                git 'https://github.com/FeelNostalgic/jenkins-helloworld.git'
            }
        }
        stage('Static Analysis'){
            steps{
                sh'''
                pip install flake8
                flake8 --exit-zero --format=pylint app > flake8.out
                '''
                recordIssues tools: [flake8(pattern: 'flake8.out')],
                               qualityGates: [
                                   // Gate 1: 10 o más errores totales marcan el build como UNSTABLE (TRUE)
                                   [threshold: 10, type: 'TOTAL', unstable: true],
                                   // Gate 2: (ejemplo de redundancia, probablemente innecesaria)
                                    [threshold: 11, type: 'TOTAL', unstable: false]
                               ]
            }
        }
//         stage('Build Dependencies'){
//             steps{
//                 sh 'pip install -r requirements.txt'
//                 echo 'Dependencias instaladas. El WORKSPACE actual es:'
//                 sh 'ls -lah'
//             }
//         }
        stage('Tests'){
            parallel{
                stage('Unit Test'){
                    steps{
                        catchError(buildResult:'UNSTABLE', stageResult: 'FAILURE'){
                            sh'''
                            export PYTHONPATH=$(pwd)
                            pytest --junitxml=result-unit.xml test/unit
                            '''

                            stash name:'unit-res', includes:'result-unit.xml'
                        }
                    }
                }
                stage('Service Tests (E2E/Integration)'){
                    steps{
                        // Iniciar ambos servicios en background ('&')

                        // Iniciar FLASK en background
                        sh'''
                        export FLASK_APP=app/api.py
                        nohup flask run > flask.log 2>&1 &
                        '''

                        // Iniciar WireMock en background
                        // Usamos la ruta donde lo instalaste en el Dockerfile y '&'
                        sh'''
                        nohup java -jar /usr/local/bin/wiremock-standalone.jar --port 9090 --root-dir test/wiremock > wiremock.log 2>&1 &
                        '''

                        // Esperar un momento para que los servicios arranquen
                        echo 'Esperando 5 segundos para el arranque de servicios...'
                        sh 'sleep 5'

                        // Ejecutar las pruebas
                        sh'''
                        export PYTHONPATH=$(pwd)
                        pytest --junitxml=result-service.xml test/rest
                        '''

                        stash name:'rest-res', includes:'result-rest.xml'
                    }
                }
            }
        }

        stage('Results'){
            steps{
                unstash name:'unit-res'
                unstash name:'rest-res'
                junit 'result-unit.xml, result-service.xml'
            }
        }

        stage('Coverage'){
            steps{
                sh'''
                pip install coverage
                coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest test/unit
                coverage xml
                '''
                recordCoverage qualityGates: [
                [criticality: 'ERROR', integerThreshold: 85, metric: 'LINE', threshold: 85.0],
                [integerThreshold: 95, metric: 'LINE', threshold:95.0],
                [critically: 'ERROR', integerThreshold: 80, metric: 'BRANCH', threshold: 80.0],
                [integerThreshold: 90, metric: 'BRANCH', threshold: 90.0]],
                tools:
                [[parser: 'COBERTURA', pattern: 'coverage.xml']]
            }
        }

        stage('Security'){
            steps{
                sh '''
                pip install bandit
                bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools:
                [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                    qualityGates: [
                    [threshold: 10, type: 'TOTAL', unstable: true],
                    [threshold: 2, type: 'TOTAL', unstable: false]
                    ]
            }
        }
    }
}