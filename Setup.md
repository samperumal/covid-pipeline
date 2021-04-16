## Initialisation

* Fixed azure package version in `Dockerfile-apache-airflow-2_0_1-fix`
	* Build image with: 
```
	docker build -f ./Dockerfile-apache-airflow-2_0_1-fix -t apache/airflow:2.0.1-fix .
```

* Initial setup: `docker-compose up airflow-init`

* Instance start: `docker-compose up -d`

## Use

* Airflow commands: `./airflow.sh <cmd>`

	* Instance info: `./airflow.sh info`

* Web interfaces
	* Airflow front end: http://localhost:8000
		* User/password: _airflow/airflow_
	* Flower monitoring for celery: http://localhost:5555

## Notes

Keep dag folder empty of other files, as it is regularly scanned for changes.

Redirect and permission unix socket `/var/run/docker.sock:/var/run/docker.sock` to enable DockerOperatordock