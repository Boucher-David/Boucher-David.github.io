from googleads import dfp

class getValueID:
    def __init__(self, key_id, path):
        self.path = path
        self.client = dfp.DfpClient.LoadFromStorage(self.path)
        self.key_id = key_id
        self.dfp = dfp

    def main(self):
        valueIDs = {}
        custom_targeting_service = self.client.GetService('CustomTargetingService', version='v201802')

        query = ('WHERE customTargetingKeyId IN (%s)' % (self.key_id))

        statement = self.dfp.FilterStatement(query)


        while True:
            response = custom_targeting_service.getCustomTargetingValuesByStatement(
                statement.ToStatement())
            if 'results' in response:
                for custom_targeting_value in response['results']:
                    valueIDs[custom_targeting_value['name']] = custom_targeting_value['id']

                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        return valueIDs