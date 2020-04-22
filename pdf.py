import io
import json
import camelot

from abc import abstractmethod


class PaymentData():
    """
    A class used to represent a data for tax reports at NDFL-3(Russia) 

    Attributes
    -----------
    date: int
        Date of payment at unixtime 
    
    payment_after_taxes: float
        Value of dollars which we had took after USA draw part of it
    
    CB_took_taxes: float
        Value of dollars which USA drawed part of it
    
    payment_by_a_paper: float
        Value of dollars which we got before pay taxes
    
    description: str
        Desciption of position at report
    """
    def __init__(self):
        self.date = 0
        self.payment_after_taxes = 0
        self.CB_took_taxes = 0
        self.payment_by_a_paper = 0
        self.description = ''
    
    def print(self):
        print(self.date, self.payment_after_taxes, self.CB_took_taxes, self.payment_by_a_paper, self.description)
    

class APdfReport():
    def __init__(self, pathToPdf):
        self.pathToPdf = pathToPdf

    def parse(self):
        tables = camelot.read_pdf(self.pathToPdf)

        kw = {"orient": "values"}

        ret_list = []

        for table in tables:
            parsed_json = json.loads(table.df.to_json(**kw))
            ret_list.extend(self.parseOneTableJson(parsed_json))
        
        return ret_list

    @abstractmethod
    def parseOneTableJson(self, json_table):
        pass


class TinkoffPdfReport(APdfReport):
    def __init__(self, pathToPdf):
        self.pathToPdf = pathToPdf
    
    def parseOneTableJson(self, json_table):
        ret_list = []
        for row_data in json_table:
            # Пропускаем заголовок
            if row_data[0].startswith('Дата'):
                continue
            ret_list.append(self.makeOnePayment(row_data))
        return ret_list

    def makeOnePayment(self, row_data):
        pd = PaymentData()
        pd.date = row_data[0]
        pd.payment_after_taxes = row_data[1]
        pd.CB_took_taxes = row_data[2]
        pd.payment_by_a_paper = row_data[3]
        pd.description = row_data[4].replace('\n', '')
        pd.print()
        return pd

