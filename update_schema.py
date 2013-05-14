import logging
#from rpx import User
from backend import Sketch
from backend import AppVersionCount
from google.appengine.ext import deferred
from google.appengine.ext import db

BATCH_SIZE = 300  # ideal batch size may vary based on entity size.
# For batch updates - change as necessary.
def UpdateSchema(cursor=None, num_updated=0):
    # query = Sketch.all()
    # version = AppVersionCount.all().get()
    # if cursor:
        # query.with_cursor(cursor)

    # to_put = []
    # count = 0
    # o_count = 0
    # for p in query.fetch(limit=BATCH_SIZE):
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        # count += 1
        # if (p.original == 'original'):
          # o_count += 1
        # to_put.append(p)

    # version.sketch_count = count
    # version.original_count = o_count
    # version.put()
    
    # if to_put:
        # db.put(to_put)
        # num_updated += len(to_put)
        # logging.debug(
            # 'Put %d entities to Datastore for a total of %d',
            # len(to_put), num_updated)
        # deferred.defer(
            # UpdateSchema, cursor=query.cursor(), num_updated=num_updated)
    # else:
        # logging.debug(
            # 'UpdateSchema complete with %d updates!', num_updated)