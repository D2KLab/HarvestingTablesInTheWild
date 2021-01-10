import os
import json

from arango import ArangoClient

class ArangoTableProcessor():
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
        raw_credentials = os.environ.get('ARANGODB_CREDENTIALS', '{}')
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
                to_vertex_collections=[self.__TABLE_COLLECTION,self.__PAGE_COLLECTION],
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
                "table_ids":table_ids,
                "page_title":title,
                "timestamp":timestamp,
                "referrer":referrer,
                "url":url,
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

            print("Processed %d out of %d webpages" % (processed, len(all_pages)))

def main():
    job = ArangoTableProcessor()
    job.create_page_table_edges()
    job.create_page_referrer_edges()

if __name__ == "__main__":
    main()
