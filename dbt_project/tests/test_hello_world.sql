{{ config(tags=['unit-test']) }}

{% call dbt_unit_testing.test ('hello_world','Basic functionality test') %}

  {% call dbt_unit_testing.expect(options={"input_format": "csv"}) %}
    hello_world
    1
  {% endcall %}

{% endcall %}