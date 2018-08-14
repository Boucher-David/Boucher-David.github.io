import json
import os
import googleads

class getLineItemID:

    def __init__(self, order_id, path):
        self.path = path
        self.client = googleads.dfp.DfpClient.LoadFromStorage(self.path)
        self.order_id = order_id



    def main(self):
        LINE_ITEM_ID = []  # Don't touch this.
        line_item_service = self.client.GetService('LineItemService', version='v201802')
        values = {
            'key': 'orderId',
            'value': {
                'xsi_type': 'NumberValue',
                'value': self.order_id
            }
        }
        query = ('WHERE orderId = :orderId')
        statement = googleads.dfp.FilterStatement(query, values)

        while True:
            # Get line items by statement.
            response = line_item_service.getLineItemsByStatement(statement.ToStatement())

            if 'results' in response:
                # Display results.
                for line_item in response['results']:
                    if (line_item.isArchived == False):
                        lineItemID = int(line_item['id'])
                        LINE_ITEM_ID.append(lineItemID)
                    else:
                        print(line_item.isArchived)
                statement.offset += googleads.dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
            return LINE_ITEM_ID