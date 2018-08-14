from googleads import dfp
from datetime import *

class createLineItem:
    def __init__(self, path, order_id, adunit_id, increment, startingAmount, numberOfLines,key_id):
        self.path = path
        self.client = dfp.DfpClient.LoadFromStorage(self.path)
        self.order_id = order_id
        self.adunit_id = []
        self.increment = increment
        self.startingAmount = startingAmount
        self.numberOfLines = numberOfLines
        self.key_id = key_id

        for adunit in adunit_id:
            self.adunit_id.append({
                'adUnitId': '%s' % (adunit),
                'includeDescendants': True
            })

    def main(self, targetingValues):
        d = datetime.today() + timedelta(days=1)
        line_item_service = self.client.GetService('LineItemService', version='v201802')
        line_items = []
        microAmountIncrement = int(1000000 * self.increment)
        microAmountStarting = int(1000000 * self.startingAmount)

        for _ in range(self.numberOfLines):
            name_id = '{0:.2f}'.format(microAmountStarting / 1000000)
            value_id = targetingValues[str(name_id)]

            line_item = {
                'name': 'Prebid_%s' % (name_id),
                'orderId': '%s' % (self.order_id),
                'startDateTime': {
                    'date': {
                        'year': '%s' % (d.year),
                        'month': '%s' % (d.month),
                        'day': '%s' % (d.day)
                    },
                    'hour': '0',
                    'minute': '0',
                    'second': '0',
                    'timeZoneID': 'America/New_York'
                },
                'costType': 'CPM',
                'unlimitedEndDateTime': True,
                'creativeRotationType': 'EVEN',
                'lineItemType': 'PRICE_PRIORITY',
                'status': 'PAUSED',
                'allowOverbook': True,
                'skipInventoryCheck': True,
                'primaryGoal': {
                    'goalType': 'NONE'
                },
                'costPerUnit': {
                    'currencyCode': 'USD',
                    'microAmount': '%s' % (microAmountStarting)
                },
                'targeting': {
                    'inventoryTargeting': {
                        'targetedAdUnits': self.adunit_id
                    },
                    'customTargeting': {
                        'xsi_type': 'CustomCriteriaSet',
                        'logicalOperator': 'OR',
                        'children': {
                            'xsi_type': 'CustomCriteria',
                            'keyId': '%s' % (self.key_id),
                            'valueIds': '%s' % (value_id),
                            'operator': 'IS'
                        }
                    }
                },
                'creativePlaceholders': [
                    {
                        'size': {
                            'width': '1',
                            'height': '1',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '160',
                            'height': '600',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '200',
                            'height': '200',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '300',
                            'height': '250',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '300',
                            'height': '6000',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '320',
                            'height': '50',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '320',
                            'height': '100',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '336',
                            'height': '280',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '468',
                            'height': '60',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '468',
                            'height': '250',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '620',
                            'height': '250',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '728',
                            'height': '90',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '770',
                            'height': '250',
                            'isAspectRatio': False
                        }
                    },
                    {
                        'size': {
                            'width': '970',
                            'height': '90',
                            'isAspectRatio': False
                        }
                    }
                ]
            }
            line_items.append(line_item)
            print('Line item with name: {} and price: {} created. '.format(
                line_item['name'],
                line_item['costPerUnit']['microAmount']))
            microAmountStarting += microAmountIncrement
        line_items = line_item_service.createLineItems(line_items)