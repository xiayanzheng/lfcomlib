from functools import reduce
from lfcomlib.Jessica import DaPr


class ForMSSQL:
    '''
    Config Template
       Config = {
       'Database':'TMS_ATL',
       'DBO':'dbo',
       'TableName':'M-Delivery',
       'WhereArgs':'[Name] IS NOT NULL',
       'NumberOfRow':1000,
       'Cols':[1,2,3],
       'Values':[1,2,3],
       }
    '''

    # def AddProc(self,Dataset):
    #

    def Make(self, OprType, Config):
        Unziped = {
            'Temp': [],
            'Cols': None,
            'Values': None,
            'WhereIsNotNull': None,
            'PrimeryKey': None,
            'WhereValues': None,
        }
        Primery = ['WhereValues']
        GUA = ['Cols', 'WhereIsNotNull', 'PrimeryKey']  # The gourp is using '[]'
        GUB = []  # The gourp is using ''''
        GUC = ['Values']
        for DataSet in Primery + GUA + GUB + GUC:
            if len(Config[DataSet]) > 0:
                for Element in Config[DataSet]:
                    if DataSet in GUA:
                        Unziped['Temp'].append("[%s]" % Element)
                    elif DataSet in GUB:
                        Unziped['Temp'].append("'%s'" % Element)
                    elif DataSet in GUC and Primery:
                        Unziped['Temp'].append(" %s = '%s' " % (Element))
                Unziped[DataSet] = reduce(lambda x, y: x + y, DaPr.insert_values_to_list(Unziped['Temp'], ","))
                Unziped['Temp'].clear()
            else:
                pass
        SQLTemplats = {
            'SelectRaw': "SELECT %s FROM [%s].[%s].[%s] " % (
            Config['SelectType'], Config['Database'], Config['DBO'], Config['TableName']),
            'Select': "SELECT %s %s FROM [%s].[%s].[%s] WHERE %s IS NOT NULL " % (
            Config['SelectType'], Unziped['Cols'], Config['Database'], Config['DBO'], Config['TableName'],
            Unziped['WhereIsNotNull']),
            'Insert': "INSERT INTO [%s].[%s].[%s](%s) VALUES(%s)" % (
            Config['Database'], Config['DBO'], Config['TableName'], Unziped['Cols'], Unziped['Values']),
            'Update': "UPDATE [%s].[%s].[%s] SET %s WHERE %s" % (
            Config['Database'], Config['DBO'], Config['TableName'], Unziped['Values'], Unziped['WhereValues'])
        }
        return SQLTemplats[OprType]