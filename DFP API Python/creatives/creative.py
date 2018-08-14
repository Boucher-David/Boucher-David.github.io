from googleads import dfp

class creative:

    def __init__(self,path, line_item_id, creative_ids,order_id):
        self.path = path
        self.line_item_id = line_item_id
        self.creative_ids = creative_ids
        self.order_id = order_id

    def main(self):
        client = dfp.DfpClient.LoadFromStorage(self.path)
        lica_service = client.GetService('LineItemCreativeAssociationService', version='v201711')
        licas = []
        licas.append({
            'creativeId': self.creative_ids,
            'lineItemId': self.line_item_id})
        licas = lica_service.createLineItemCreativeAssociations(licas)
        print("Creative {} added to line item {} in order {}".format(self.creative_ids, self.line_item_id, self.order_id))