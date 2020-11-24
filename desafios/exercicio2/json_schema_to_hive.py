from jsonschema2athena.generator import generate_query

_ATHENA_CLIENT = None


def create_hive_table_with_athena(query):
    """
    Função necessária para criação da tabela HIVE na AWS
    :param query: Script SQL de Create Table (str)
    :return: None
    """

    print(f"Query: {query}")
    _ATHENA_CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": f"s3://iti-query-results/"},
    )


def handler(
    database=None,
    table=None,
    schema=None,
    location=None,
    serde=None,
    serdeproperties=None,
):
    """
    #  Função principal
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função create_hive_table_with_athena para te auxiliar
        na criação da tabela HIVE, não é necessário alterá-la
    """
    query = generate_query(
        database=database,
        table=table,
        schema=schema,
        location=location,
        serde=serde,
        serdeproperties=serdeproperties,
    )
    create_hive_table_with_athena(query)
