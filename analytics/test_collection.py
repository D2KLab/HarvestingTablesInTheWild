from uuid import uuid4
from analytics.collection import ArangoTableCollector


def test_arango_collector_append():
    collector = ArangoTableCollector()
    nonce = uuid4().hex
    mock_data = {
        "page_title": "Test Page",
        "timestamp": "2020-01-01T00:00:00Z",
        "table": {
            "Numers": ["1", "2"],
            "Letters": ["A", "B"]
        },
        "url": "http://test",
        "nonce": nonce
    }
    collector.append(mock_data)
    result_cursor = collector.db.aql.execute(
        'FOR doc IN parsed_tables FILTER doc.nonce == "%s" RETURN doc' % nonce)
    results = list(result_cursor)
    assert len(results) == 1
    document = results[0]
    for key, value in mock_data.items():
        assert key in document
        assert value == document[key]
