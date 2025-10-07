from pathlib import Path

from dagster import asset, AssetExecutionContext, AssetSelection, define_asset_job, Definitions
from dagster_duckdb import DuckDBResource
from dagster_dbt import dbt_assets, DbtProject, DbtCliResource


my_project = DbtProject(project_dir=Path(__file__).parent.parent / "dbt_project")
my_project.prepare_if_dev()

dbt = DbtCliResource(project_dir=my_project)

@dbt_assets(
    manifest=my_project.manifest_path,
    exclude="tag:unit-test"
)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@asset(deps=[my_dbt_assets])
def downstream_asset(context: AssetExecutionContext) -> None:
    context.log.info("Hello world!")

hello_world_job = define_asset_job(
    name="hello_world_job",
    selection=AssetSelection.assets("downstream_asset").upstream()
)

defs = Definitions(
    assets=[my_dbt_assets, downstream_asset],
    jobs=[hello_world_job],
    schedules=[],
    sensors=[],
    resources={
        "duckdb": DuckDBResource(database=":memory:"),
        "dbt": dbt,
    },
)
