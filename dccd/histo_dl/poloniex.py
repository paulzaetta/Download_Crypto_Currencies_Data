#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2019-03-26 10:42:57
# @Last modified by: ArthurBernard
# @Last modified time: 2024-06-06 12:18:23

""" Objects to download historical data from Poloniex exchange.
.. currentmodule:: dccd.histo_dl.poloniex
.. autoclass:: FromPoloniex
   :members: import_data, save, get_data
   :show-inheritance:
"""

# Import built-in packages

# Import third-party packages
import requests
import json

# Import local packages
from dccd.histo_dl.exchange import ImportDataCryptoCurrencies

__all__ = ['FromPoloniex']


SPAN_HANDLER = {
    60: "MINUTE_1",
    300: "MINUTE_5",
    600: "MINUTE_10",
    900: "MINUTE_15",
    1800: "MINUTE_30",
    3600: "HOUR_1",
    7200: "HOUR_2",
    14400: "HOUR_4",
    21600: "HOUR_6",
    43200: "HOUR_12",
    86400: "DAY_1",
    86400 * 3: "DAY_3",
    86400 * 7: "WEEK_1",
    # MONTH_1,
}


class FromPoloniex(ImportDataCryptoCurrencies):
    """ Class to import crypto-currencies data from the Poloniex exchange.

    Parameters
    ----------
    path : str
        The path where data will be save.
    crypto : str
        The abreviation of the crypto-currency.
    span : {int, 'weekly', 'daily', 'hourly'}
        - If str, periodicity of observation.
        - If int, number of the seconds between each observation, minimal span\
            is 300 seconds.
    fiat : str
        A fiat currency or a crypto-currency. Poloniex don't allow fiat
        currencies, but USD theter.
    form : {'xlsx', 'csv'}
        Your favorit format. Only 'xlsx' and 'csv' for the moment.

    See Also
    --------
    FromBinance, FromGDax, FromKraken

    Notes
    -----
    See Poloniex API documentation [1]_ for more details on parameters.

    References
    ----------
    .. [1] https://docs.poloniex.com/#introduction

    Attributes
    ----------
    pair : str
        Pair symbol, `crypto + fiat`.
    start, end : int
        Timestamp to starting and ending download data.
    span : int
        Number of seconds between observations.
    full_path : str
        Path to save data.
    form : str
        Format to save data.

    Methods
    -------
    import_data
    save
    get_data

    """

    def __init__(self, path, crypto, span, fiat='USD', form='xlsx'):
        """ Initialize object. """
        if fiat in ['EUR', 'USD']:
            print("Poloniex don't allow fiat currencies.",
                  "The equivalent of US dollar is Tether USD as USDD.")
            self.fiat = fiat = 'USDT'
            #self.fiat = fiat = 'USDD'

        if crypto == 'XBT':
            crypto = 'BTC'

        ImportDataCryptoCurrencies.__init__(
            self, path, crypto, span, 'Poloniex', fiat, form
        )

        #self.pair = self.fiat + '_' + crypto
        self.pair = crypto + '_' + self.fiat
        self.full_path = self.path + '/Poloniex/Data/Clean_Data/'
        self.full_path += str(self.per) + '/'
        self.full_path += str(self.crypto) + str(self.fiat)

    def _import_data(self, start='last', end='now'):
        self.start, self.end = self._set_time(start, end)
        currencyPair = self.pair

        param = {
            #'command': 'returnChartData',
            #'currencyPair': self.pair,
            # 'interval': 'MINUTE_1',
            'interval': SPAN_HANDLER[self.span],
            'limit' : 500,
            'startTime': self.start * 1000,
            'endTime': self.end * 1000,
            #'period': self.span
        }

        url = f"https://api.poloniex.com/markets/{currencyPair}/candles"

        r = requests.get(url, param)
        json_data = json.loads(r.text)

        data = [{
            'low': float(e[0]),
            'high': float(e[1]),
            'open': float(e[2]),
            'close': float(e[3]),
            'quoteVolume': float(e[4]),
            'volume': float(e[5]),
            'weightedAverage': float(e[10]),
            'date': int(e[12] / 1000),
        } for e in json_data]

        return data
    


    def _import_data_huge(self, start='last', end='now'):
        self.start, self.end = self._set_time(start, end)

        finalEnd = self.end
        interval = 500*60
        startDate = self.start
        endDate = self.start + interval
        data = list()

        '''
        try: 
            while startDate < self.end * 1000 :
                data.append(self._import_data(startDate, endDate))
                i = interval
                startDate = startDate + i
                endDate = endDate + i
            return data
        except ValueError as e :
            return data, startDate, endDate, e
        '''

        while startDate < finalEnd:
            data.extend(self._import_data(startDate, endDate))
            i = interval
            startDate = startDate + i
            endDate = endDate + i
        return data, startDate, endDate
        


    def import_data(self, start='last', end='now'):
        """ Download data from Poloniex for specific time interval.

        Parameters
        ----------
        start : int or str
            Timestamp of the first observation of you want as int or date
            format 'yyyy-mm-dd hh:mm:ss' as string.
        end : int or str
            Timestamp of the last observation of you want as int or date
            format 'yyyy-mm-dd hh:mm:ss' as string.

        Returns
        -------
        data : pd.DataFrame
            Data sorted and cleaned in a data frame.

        """
        data = self._import_data(start=start, end=end)

        return self._sort_data(data)
