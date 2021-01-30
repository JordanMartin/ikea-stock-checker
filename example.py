#!/usr/bin/env python3
#coding: utf-8

from stock_checker import StockChecker
import cli_ui as cli
import os
import signal
import sys

signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
clear = lambda: os.system('clear')

if __name__ == "__main__":
    checker = StockChecker('https://iows.ikea.com/retail/iows/fr/fr/stores/562/availability/ART')
    checker.add_ref('402.046.94', 'Range-couverts, bambou52x50 cm')
    checker.add_ref('502.056.26', 'Structure élément bas, blanc60x60x80 cm')
    checker.add_ref('702.061.25', 'Porte, motif noyer gris clair60x80 cm')
    checker.printAll()

    while True:
        try:
            print()
            checker.ask_ref()
            clear()
        except Exception as e:
            print(e)
            clear()
            cli.error('Cannot find the reference')
            print()
        
        checker.printAll()
