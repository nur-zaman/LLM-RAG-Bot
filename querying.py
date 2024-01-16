from manage_embedding import load_index
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


async def data_querying(input_text: str):
    # Load index
    index = await load_index("data")
    engine = index.as_query_engine()

    # queries the index with the input text
    response = engine.query(input_text)
    response_text = response.response
    logging.info(response_text)
    return response_text
