import os
import json

from arango import ArangoClient
from postprocessing.annotation import TableAnnotationAPIClient
from postprocessing.models import OrangePreprocessHeavy

# Useful References for ArangoDB graphs:
# https://python-driver-for-arangodb.readthedocs.io/en/master/graph.html#edge-collections
# https://python-driver-for-arangodb.readthedocs.io/en/master/specs.html#standardcollection
# https://stackoverflow.com/a/23708645


class ArangoTableProcessor:
    __TABLE_COLLECTION = 'parsed_tables'
    __PAGE_COLLECTION = 'visited_pages'
    __EDGE_COLLECTION = 'htw_edges'
    __GRAPH = 'htw'
    __DATABASE = '_system'

    def __init__(self):

        # load database configuration
        arango_host = os.environ.get('ARANGO_HOST', 'http://localhost:8529')
        if not arango_host:
            raise Exception('ARANGO_HOST not defined')
        raw_credentials = os.environ.get('ARANGO_CREDENTIALS', '{}')
        credentials = json.loads(raw_credentials)

        # connect to database
        client = ArangoClient(hosts=arango_host)
        self.db = client.db(self.__DATABASE, **credentials)

        # create collection for webpages (if necessary)
        if self.db.has_collection(self.__PAGE_COLLECTION):
            self.pages = self.db.collection(self.__PAGE_COLLECTION)
        else:
            self.pages = self.db.create_collection(self.__PAGE_COLLECTION)

        # insert pseudo vertex for starting point
        self.pages.insert({
            "_key": "htw_start",
            "table_ids": [],
            "page_title": "HTW Start",
            "timestamp": "",
            "referrer": "",
            "url": "http://localhost",
        })

        # create graph (if necessary)
        if self.db.has_graph(self.__GRAPH):
            self.graph = self.db.graph(self.__GRAPH)
        else:
            self.graph = self.db.create_graph(self.__GRAPH)

        # create edge collection (if necessary)
        if self.graph.has_edge_definition(self.__EDGE_COLLECTION):
            self.edges = self.graph.edge_collection(self.__EDGE_COLLECTION)
        else:
            self.edges = self.graph.create_edge_definition(
                edge_collection=self.__EDGE_COLLECTION,
                from_vertex_collections=[self.__PAGE_COLLECTION],
                to_vertex_collections=[
                    self.__TABLE_COLLECTION, self.__PAGE_COLLECTION],
            )

    def create_page_table_edges(self):
        """
        Creates 1) visited pages document for all tables in the database and
        2) the corresponding 'page-contains' graph edges between the visited
        pages and the parsed tables.
        NOTE: This is not idempotent. Running this operation multiple times on
        the same dataset will lead to duplicate pages and edges!
        """
        # get all unique URLs
        unique_urls = set()
        cursor = self.db.aql.execute(
            f"FOR table IN {self.__TABLE_COLLECTION} RETURN table.url",
        )
        for e in cursor:
            unique_urls.add(e)
        total_urls = len(unique_urls)
        print('Got %d unique URLs' % (total_urls,))

        # for each URL, fetch the corresponding tables
        processed = 0
        for url in unique_urls:
            # fetch relevant tables from db
            cursor = self.db.aql.execute(
                'FOR table IN parsed_tables FILTER table.url == @url RETURN table',
                bind_vars={'url': url},
            )
            if cursor.empty():
                print('WARNING: no tables found for URL %s, skipping' % (url,))
                continue

            # table_ids = [t['_key'] for t in cursor]
            table_ids = []
            title, timestamp, referrer = "", "", ""
            for t in cursor:
                table_ids.append(t['_id'])
                title = t['pageTitle']
                timestamp = t['timestamp']
                referrer = t['referrer']

            # create page entry
            page = {
                "table_ids": table_ids,
                "page_title": title,
                "timestamp": timestamp,
                "referrer": referrer,
                "url": url,
            }

            # insert page into database
            page_metadata = self.pages.insert(page)

            # create table edges
            for tid in table_ids:
                self.edges.link(
                    page_metadata['_id'],
                    tid,
                    data={
                        'type': 'page-contains',
                    },
                )

            processed += 1
            print('Processed %d out of %d URLs' % (processed, total_urls))

    def create_page_referrer_edges(self):
        """
        Creates the 'hyperlink' edges for all visited pages in the database,
        based on the referrer fields of the entries.
        NOTE: This is not idempotent. Running this operation multiple times on
        the same dataset will lead to duplicate edges!
        """

        # load all pages from database
        cursor = self.db.aql.execute(
            f"FOR page IN {self.__PAGE_COLLECTION} RETURN page",
        )
        all_pages = list(cursor)
        print("%d visited webpages" % (len(all_pages),))

        # lookup cache URL -> page id
        page_id_mapping = {}
        for page in all_pages:
            page_id_mapping[page['url']] = page['_id']

        # establish referrer edges for all pages
        processed = 0
        for page in all_pages:
            processed += 1
            referrer_url = page['referrer']
            referrer_id = page_id_mapping.get(referrer_url, '')
            if not referrer_url or not referrer_id:
                continue

            self.edges.link(
                referrer_id,
                page['_id'],
                data={
                    'type': 'hyperlink',
                }
            )

            print("Processed %d out of %d webpages" %
                  (processed, len(all_pages)))

    def backfill_preprocess_results(self):
        # Collect all pending tasks
        pending_tasks = []
        cursor = self.db.aql.execute(
            f"""
            FOR table IN {self.__TABLE_COLLECTION}
            FILTER table.preprocessing != null
            RETURN [table.preprocessing, table._id]
            """,
        )
        for preprocess, document_id in cursor:
            if 'task_id' in preprocess:
                pending_tasks.append([preprocess['task_id'], document_id])
            else:
                print("WARNING: unexpected preprocessing value found",
                      document_id, preprocess)

        # Try to backfill all the missing preprocessing results
        client = TableAnnotationAPIClient()
        for task_id, document_id in pending_tasks:
            task_status = client.get_preprocess_task_status(task_id)
            if task_status.get('task_status') == 'SUCCESS':
                task_result = client.get_preprocess_task_result_heavy(task_id)
                # NOTE:
                # The API is unreliable, and the following line is only
                # here because of the observed behaviour differs from
                # the documented behaviour
                if isinstance(task_result, list):
                    task_result = task_result[0]
                self.backfill_single_document(document_id, task_result)
                print("UPDATED: table (%s) preprocessing data" %
                      document_id)
            else:
                print('WARNING: no updates made to table %s (%s): %s' %
                      (document_id, task_id, task_status))

    # pylint: disable=broad-except
    def backfill_single_document(self, document_id, orange_data):
        try:
            orange_data = OrangePreprocessHeavy(orange_data)
            document = self.db.document(document_id)
            document['preprocessing'] = None
            document['tableOrientation'] = orange_data.orientation.orientation
            document['headers'] = orange_data.header.header
            document['relation'] = orange_data.restructured_table
            # TODO: figure this out from the response
            document['hasHeader'] = True
            self.db.update_document(document)
        except Exception as e:
            print("ERROR: Failed to update document", orange_data, e)


def main():
    job = ArangoTableProcessor()
    job.create_page_table_edges()
    job.create_page_referrer_edges()
    job.backfill_preprocess_results()


if __name__ == "__main__":
    main()
