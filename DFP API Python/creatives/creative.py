from googleads import dfp

class creative:

    def __init__(self,path, line_item_id, creative_ids,order_id):
        self.path = path
        self.line_item_id = line_item_id
        self.creative_ids = creative_ids
        self.order_id = order_id

    def main(self):
        client = dfp.DfpClient.LoadFromStorage(self.path)
        lica_service = client.GetService('LineItemCreativeAssociationService', version='v201802')
        licas = []
        licas.append({
            'creativeId': self.creative_ids,
            'lineItemId': self.line_item_id,
            'sizes': [
                {
                        'width': '1',
                        'height': '1',
                        'isAspectRatio': False
                },
                {
                        'width': '160',
                        'height': '600',
                        'isAspectRatio': False
                },
                {

                        'width': '200',
                        'height': '200',
                        'isAspectRatio': False

                },
                {

                        'width': '300',
                        'height': '250',
                        'isAspectRatio': False

                },
                {

                        'width': '300',
                        'height': '6000',
                        'isAspectRatio': False

                },
                {

                        'width': '320',
                        'height': '50',
                        'isAspectRatio': False
                },
                {

                        'width': '320',
                        'height': '100',
                        'isAspectRatio': False

                },
                {

                        'width': '336',
                        'height': '280',
                        'isAspectRatio': False

                },
                {

                        'width': '468',
                        'height': '60',
                        'isAspectRatio': False

                },
                {

                        'width': '468',
                        'height': '250',
                        'isAspectRatio': False

                },
                {

                        'width': '620',
                        'height': '250',
                        'isAspectRatio': False

                },
                {

                        'width': '728',
                        'height': '90',
                        'isAspectRatio': False

                },
                {

                        'width': '770',
                        'height': '250',
                        'isAspectRatio': False

                },
                {

                        'width': '970',
                        'height': '90',
                        'isAspectRatio': False

                }
            ]
        })
        licas = lica_service.createLineItemCreativeAssociations(licas)
        print("Creative {} added to line item {} in order {}".format(self.creative_ids, self.line_item_id, self.order_id))