Tekton praktijkles

Voorbereiding in Readme.md 


Deel 1 - voorbeeld Task: 
- [ ] Zorg dat de GitOps Pipeline operator geïnstalleerd is.
- [ ] Maak de hello-task aan uit deel 1. Bekijk goed de configuratie van deze Task. Het is de bedoeling dat je deze straks zelf kan maken.
- [ ] Creëer de TaskRun uit deel 1 en zie het resultaat in OpenShift. Bekijk goed de configuratie van deze Taskrun. Het is de bedoeling dat je deze straks zelf kan maken.

Deel 2 - Gebruik parameter: 
- [ ] Open de volgende website: https://tekton.dev/docs/pipelines/ . Deze documentatie kun je gebruiken als hulpmiddel bij alle opdrachten. 
- [ ] Maak een Task en TaskRun aan waarin “Hello World” uit deel 1 vervangen is voor een parameter (tip: zie documentatie ‘Tasks’ en ‘Taskruns’). 
- [ ] Maak een nieuwe Task en TaskRun aan waarbij de Walvis zegt “Goodbye Jenkins”. Maak hierbij ook gebruik van een parameter field. 

Deel 3 - Pipelines:
- [ ] Maak een Pipeline en PipelineRun aan met daarin 2 Tasks
    - [ ] de eerste Task voert een hello-Task uit
    - [ ] de tweede Task voert een goodbye-Task uit met parameter. 

Deel 4 - Bericht schrijven - Workspace:
- [ ] Maak een Task “write-message” en TaskRun aan die een bericht “Hello World” schrijft naar een workspace (emptyDir). Gebruik in de Task het volgende script: 
	 #!/usr/bin/env sh
        cowsay $(params.message) > $(workspaces.messages.path)/message
        echo "file written to $(workspaces.messages.path)"
        ls -la $(workspaces.messages.path)

Deel 5 - Bericht lezen - Workspace: 
- [ ] Maak een nieuwe Task en TaskRun aan. Deze Task zal 2 ‘steps’ bevatten:
    - [ ] Voor de eerste step gebruiken we het script van deel 4. 
    - [ ] Maak een tweede step die het bericht van step 1 uitleest en print in de logs. 
        - [ ] Gebruik als image ‘alpine’

Deel 6 - Shared message - Pipeline - Workspace: 
- [ ] Maak een Task “read-message” aan die bestaat uit step 2 van de Task uit deel 5. 
- [ ] Maak een Pipeline aan die de volgende 2 Tasks bevat:
    - [ ] De Task “write-message” uit deel 4
    - [ ] De Task “read-message”
- [ ] Voor de PipelineRun maken we nu gebruik van een PersistentVolumeClaim om ons bericht in weg te schrijven. Deze kun je in de PipelineRun als volgt configureren: 
	spec: 
           …
	   workspaces:
    	     - name: pipeline-space
                volumeClaimTemplate:
        	  spec:
          	    accessModes:
                      - ReadWriteOnce
                    resources:
                      requests:
                        storage: 128Mi

Deel 7 - Repo clonen:
- Maak een Task “git-clone” en TaskRun aan. Het image dat we gebruiken is “alpine/git” Deze bevat het volgende script: 
###      #!/usr/bin/env sh
###      cd $(workspaces.source-code.path)
###      git clone $(params.url)
###      cd Breakout
###      git checkout $(params.revision)
###      ls -la
- Controleer of je geforkte repo op public staat.
- Zorg dat de URL in de TaskRun naar jouw fork repo en juiste revision (branch) verwijst.
- De workspace in de TaskRun wordt net zo geconfigureerd als in deel 6. 

Deel 8 - Python test - Pipeline - PVC:
- [ ] Maak een Task “python-test” aan. Deze bestaat uit 3 steps, die allemaal gebruik maken van het image “python:3.9”: 
    - [ ] Step 1 “create venv”: 
		        #!/usr/bin/env bash
       			cd $(workspaces.source-code.path)/Breakout/python-app
        		ls -la
    			python -m venv $PWD/venv
    - [ ] Step 2 “install dependencies”:
			#!/usr/bin/env bash
        		cd $(workspaces.source-code.path)/Breakout/python-app
        		ls -la
        		source $PWD/venv/bin/activate
        		pip install -r requirements.txt
    - [ ] Step 3 “run-tests”:
		        #!/usr/bin/env bash
        		cd $(workspaces.source-code.path)/Breakout/python-app
        		source $PWD/venv/bin/activate
        		python -m unittest test_app.py
- [ ] Maak een PersistentVolumeClaim aan met: (tip: Google)
    - [ ] accessModes: ReadWriteOnce
    - [ ] 512Mi storage requests
- [ ] Maak een Pipeline en PipelineRun aan die de volgende 2 Tasks uitvoert:
    - [ ] Clonen van de repo
    - [ ] Uitvoeren van de python test
    - [ ] Als Workspace gebruik je nu de PVC die je in de stap hiervoor hebt aangemaakt. In de PipelineRun kun je deze gebruiken met de volgende configuratie:
		spec:
		  …..
  		  workspaces:
    		    - name: (naam van je workspace)
      		       persistentVolumeClaim:
        	         claimName: (naam van je PVC)


Deel 9 - Build aftrappen:
- [ ] Maak een Task en TaskRun aan die de BuildConfig (van de setup) aftrappen. 
- Het image dat we gebruiken in deze Task is: 'quay.io/openshift/origin-cli:latest'
    - [ ] Het commando dat je hiervoor gebruikt in het script is “oc start-build ${params.buildconfig-name} -n (naam van je namespace)

Deel 10 - Triggers:
- [ ] Maak een EventListener aan met als interceptor github en als eventtype pull request (tip: zie documentatie Tekton)
- [ ] Maak een EventListenerRoute aan (het exposen van je el-service) met de volgende configuratie:
	apiVersion: route.openshift.io/v1
	kind: Route
	metadata:
  	 	name: github-el-route
	spec:
  		port:
			targetPort: http-listener
  		tls:
    			insecureEdgeTerminationPolicy: Redirect
    			termination: edge
  		to:
    			kind: Service
    			name: (naam van je el-service)
    			weight: 100
  		wildcardPolicy: None
- [ ] Maak een TriggerBinding aan met de parameter “revision” met als value “$(body.pull_request.head.sha)”. Dit zorgt ervoor dat de SHA van de commit ‘Head’ wordt meegegeven als data. 
- [ ] Maak een TriggerTemplate aan die de test-pipeline van deel 8 aftrapt. 
    - [ ] De parameter “revision” heeft in de TriggerTemplate de value “$(tt.params.revision)”
- [ ] Creëer een webhook op Github onder ‘repository settings’:
    - [ ] Payload URL: Vul hier de url in van de EventlistenerRoute
    - [ ] Content type: application/json
    - [ ] Secret: leeg (benodigd voor private repo’s. Als je repo nog op private staat, is het handig deze eerst naar public te zetten) (Uitdaging: als alles gelukt is, probeer dan eens je repo private te maken, een secret aan te maken en deze te verwerken in je EventListener)
    - [ ] Selecteer ‘let me select individual events’ en kies dan ‘pull requests’
- [ ] Zorg dat je repo op public staat
- [ ] Maak in je CLI een branch aan en 
    - [ ] verander in de ‘index.html’ bijvoorbeeld iets in de title. (Let op: Het kan zijn dat je de test_app.py hierdoor ook moet wijzigen)
    - [ ] Add, commit en push de verandering naar GitHub. 
    - [ ] Creëer een pull request van je branch naar de main branch. 
    - [ ] Zie in OpenShift wat er gebeurt…

 
