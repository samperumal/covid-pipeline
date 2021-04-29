#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'docker_sample',
    default_args=default_args,
    # schedule_interval=timedelta(minutes=10),
    start_date=days_ago(0),
)

t3 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='sacorona/scrapy:latest',
    volumes = ["airflow_data_volume:/opt/scrapy/sacoronavirus/out"],
    network_mode='bridge',
    task_id='scrapy',
    dag=dag,
    auto_remove=True
)


t4 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='sacorona/tesseract:latest',
    volumes = ["airflow_data_volume:/var/data"],
    network_mode='bridge',
    task_id='tesseract',
    dag=dag,
    auto_remove=True
)

t5 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='sacorona/text-clean:latest',
    volumes = ["airflow_data_volume:/var/data"],
    network_mode='bridge',
    task_id='python-clean',
    environment={
		"POSTGRES_HOST_NAME": "db",
		"POSTGRES_USER_NAME": "postgres",
		"POSTGRES_PASSWORD": "example"
    },
    dag=dag,
    auto_remove=True
)

t6 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='sacorona/text-process:latest',
    volumes = ["airflow_data_volume:/var/data"],
    network_mode='bridge',
    task_id='r-analysis',
    dag=dag,
    auto_remove=True
)


t3 >> t4 >> t5 >> t6
