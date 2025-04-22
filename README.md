# data-challenge

This challenge is composed of three exercises. In exercises 1 and 2, you will be evaluated based on code quality, optimization, and efficiency; in exercise 3, on your architecture design skills. Fork this project and save your work there, as we will review your submission in your own repository.

A tech company is beginning its data journey. As a first step, they decided to invest in creating an MVP of a data platform using AWS services (see Fig. 1) to validate its potential. Following best practices in platform development, the company adopted the principle of *analytics by design* from the beginning: all data producers have adapted to send events to the platform using a predefined and documented layout.

![Figure 1](img/mvp.png)

---

### 1. Your team was tasked with building this data ingestion flow, and **you** are responsible for the **Data Quality module** of this flow. This module should listen to a queue, validate the events transported through it using JSON Schemas stored in a repository, and forward them to another queue (`valid-events-queue`).

Build this module in Python using the files provided in the `exercicio1` folder. You may propose improvements, but be mindful of the following:

- Use the JSON Schema in the exercise folder (`schema.json`) to validate the event, **without** using external validation libraries. Ensure:
  - The data types of fields match what's in the schema.
  - Fields not defined in the schema are **not** accepted.

- The output event must be **identical** to the input event.

- Develop your code in the `event_validator.py` file. The `handler` function in this file is the one that gets triggered when a new event arrives in the queue. Use the `send_event_to_queue` function to send validated events.

- Run `python main.py` to simulate the flow.

#### ✅ Solution

**This solution uses the `pipenv` tool for consistent dependency management. To test it, follow these commands:**

1. Install pipenv and dependencies:  
   `$ pip install pipenv`

2. Clone this repository:  
   `$ git clone git@github.com:gPass0s/data-challenge.git`

3. Enter the project root:  
   `$ cd data-challange`

4. Initialize the virtual environment:  
   `$ pipenv install && pipenv shell`

5. Simulate the flow:  
   `$ pipenv run python desafios/exercicio1/main.py`

   Example output:
   ```bash
   ~/data-challenge$ pipenv run python desafios/exercicio1/main.py
   Response status code: [200]
   ```

6. Run the unit tests:  
   `$ pipenv run python -m pytest -vv tests/`

   Example output:
   ```bash
   ~/projects/data-challenge$ pipenv run python -m pytest -vv tests/
   ============================================================================= test session starts ==============================================================================
   platform linux -- Python 3.7.2, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /home/guilhermepassos/.local/share/virtualenvs/data-challenge-PTcfleLB/bin/python
   cachedir: .pytest_cache
   rootdir: /home/guilhermepassos/projects/data-challenge
   collected 6 items

   tests/test__checkers.py::test_schema PASSED                                                              [ 16%]
   tests/test__checkers.py::test_type PASSED                                                                [ 33%]
   tests/test__checkers.py::test_required PASSED                                                            [ 50%]
   tests/test__checkers.py::test_properties_fail PASSED                                                     [ 66%]
   tests/test__checkers.py::test_properties_pass PASSED                                                     [ 83%]
   tests/test__checkers.py::test_event_type PASSED                                                          [100%]

   ============================================================================== 6 passed in 0.03s ===============================================================================
   ```

---

### 2. It is very common for platform users to want to perform exploratory analysis on the events stored in the data platform. You had the idea of building a module that **automates the creation of tables in AWS Athena** using the same JSON Schema from the Data Quality module.

Build this module in Python using the files provided in the `exercicio2` folder, and ensure it generates `CREATE TABLE` queries including all fields and data types from the schema. Consider the following:

- Use the `json_schema_to_hive.py` file to develop your code, and the `create_hive_table_with_athena` function to create the table.

- Refer to the Athena `CREATE TABLE` documentation:  
  https://docs.aws.amazon.com/athena/latest/ug/create-table.html

- Run `python main.py` to simulate the process.

#### ✅ Solution

**Just like the previous solution, this one also uses `pipenv`. From step IV of the previous setup, execute the following:**

1. Simulate the flow:  
   `$ pipenv run python desafios/exercicio2/main.py`

   Example output:
   ```bash
   ~/projects/data-challenge$ pipenv run python desafios/exercicio2/main.py
   Query: CREATE EXTERNAL TABLE IF NOT EXISTS data-challange.events (
   eid STRING,
   documentNumber STRING,
   name STRING,
   age INTEGER,
   address STRUCT <
       street:STRING,
       number:INTEGER,
       mailAddress:BOOLEAN,
       >
   )
   ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
   WITH SERDEPROPERTIES (
   'input.regex' = '^(?!#)([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+([^ ]+)\s+[^\(]+[\(]([^\;]+).*\%20([^\/]+)[\/](.*)$'
   )
   LOCATION 's3://iti-query-results/';
   ```

---

### 3. The MVP succeeded! The business team identified many opportunities in the available data. You’ve now been tasked with proposing a **non-exhaustive architectural design** for a data platform. Don’t feel restricted by the MVP solution; you may use both cloud services and open-source solutions. Use Draw.io if you like, and ensure you meet the following requirements:

- Data ingestion solution  
- ETL pipeline  
- Storage solutions  
- Data catalog  

#### ✅ Solution

![Figure 1](img/solution.png)

**Notes on the architecture above:**

1. For data ingestion, we suggest using **Kinesis Data Streams (KDS)**. KDS allows events to be read multiple times during the retention window, enabling multiple consumers to access the same data. In other words, KDS implements a data **pub/sub** system.

2. Event schema validation is done using **AWS Glue Schema Registry**. According to its [documentation](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html), it supports validation and stream flow control using Apache Avro schemas and integrates with KDS as described [here](https://docs.aws.amazon.com/glue/latest/dg/schema-registry-integrations.html#schema-registry-integrations-kds).

3. Once validated, events trigger a **Lambda function** that processes and stores the events in a **partitioned structure on S3**.

4. Upon writing to S3, another Lambda is triggered. It checks whether a new partition (by minute, hour, or day) was created by consulting a **DynamoDB table** that tracks the first arrival timestamp for each period. If it’s the first event in a new partition, the Lambda runs `MSCK REPAIR TABLE` in Athena to expose the partition for querying.

5. **Glue Crawlers** are used programmatically to scan S3 data and update the **Glue Catalog**, which Athena queries.

6. Finally, events are available for **SQL querying via AWS Athena**.