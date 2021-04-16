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

t1 = BashOperator(task_id='print_date', bash_command='date', dag=dag)

t3 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='sacorona:latest',
    volumes = ["airflow_data_volume:/opt/scrapy/sacoronavirus/out"],
    network_mode='bridge',
    task_id='scrapy',
    dag=dag,
    auto_remove=True
)


t4 = DockerOperator(
    api_version='1.21',
    docker_url="unix://var/run/docker.sock",
    image='tesseractshadow/tesseract4re:latest',
    volumes = ["airflow_data_volume:/home/work/data"],
    network_mode='bridge',
    task_id='tesseract',
    # command=["/home/work/parse.sh", "data/sacorona/images"],
    dag=dag,
    auto_remove=True
)


t1 >> t3
t3 >> t4
