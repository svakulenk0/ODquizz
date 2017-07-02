#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 28, 2017
.. codeauthor: svitlana vakulenko
<svitlana.vakulenko@gmail.com>

Test table parsing service
'''

from pyyacp.yacp import YACParser

TEST_TABLE_URL = "https://www.wien.gv.at/finanzen/ogd/hunde-wien.csv"


def csvclean_service(url):
    '''
    returns parsed table object from the YACParser
    '''
    table = YACParser(url=url, sample_size=100)
    return table


def test_csvclean_service(url=TEST_TABLE_URL):
    table = csvclean_service(TEST_TABLE_URL)
    print table.meta
    print table.descriptionLines
    print table.header_line

    # for cell in table:
    #     print "; ".join(cell)
    for row in table.sample:
        print row
    return table.sample

if __name__ == "__main__":
    test_csvclean_service()

