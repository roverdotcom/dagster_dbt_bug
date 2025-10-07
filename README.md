# Bug

DBT assets launched with [--exclude tag:unit-test](https://github.com/roverdotcom/dagster_dbt_bug/blob/main/dagster_dbt_bug/__init__.py#L15) cause jobs to fail silently when using the EqualExperts/dbt_unit_testing DBT package.

# How to Reproduce

1. Install the DBT dependencies:  
   `uv run dbt deps --project-dir dbt_project`
2. Launch the Dagster webserver locally:  
   `uv run dagster dev`
3. Navigate to the Hello World job in your browser:  
   [http://localhost:3000/locations/dagster_dbt_bug/jobs/hello_world_job](http://localhost:3000/locations/dagster_dbt_bug/jobs/hello_world_job)
4. Materialize the job.
5. Observe that the `my_dbt_assets` step produces this log line:  
   `op ‘my_dbt_assets’ did not yield or return expected outputs {‘hello_world_test_hello_world’}.`
6. Observe that the `downstream_asset` was skipped.
7. Observe that the job is marked as successful despite the downstream asset being skipped.
