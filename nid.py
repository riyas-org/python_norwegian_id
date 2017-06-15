'''
#Norsk id check
#ported to python on 15.06.2017 from nettskjema
#By Riyas 
'''

import datetime
import numpy as np


def isValidNationalIdNumber(nationalIdNumber):
	#if not np.isnan(nationalIdNumber) and nationalIdNumber.length == 11:
        if len(nationalIdNumber) == 11:
            if not passesModulo11Test(nationalIdNumber):
                return False
            # ID number with dates normalized for D and H numbers:
            normalizedNationalIdNumber = getNormalizedNationalIdNumber(nationalIdNumber)
            if not passesDateTest(normalizedNationalIdNumber):
                return False
            return True
        return False

def passesModulo11Test(nationalIdNumber):    
    WEIGHT_NUMBERS = [[3, 7, 6, 1, 8, 9, 4, 5, 2, 1, 0],[5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]]
    for  i in range(0,len(WEIGHT_NUMBERS),1):
        sum = 0
        for  j in range(0,len(WEIGHT_NUMBERS[i]), 1):
            sum += (int(nationalIdNumber[j], 10) * WEIGHT_NUMBERS[i][j])
        if sum % 11 is not 0:
            #import pdb; pdb.set_trace()
            return False
    return True

def getNormalizedNationalIdNumber(nationalIdNumber):
    # H numbers: 4 is added to the third digit, i.e. the first digit of month.
    # Hence, H numbers have months between 41 and 52
    month = getMonthInNationalIdNumber(nationalIdNumber)
    h = int(nationalIdNumber[2], 10)
    if month > 40 and month < 53:
        return nationalIdNumber[0:2] + str(h - 4) + nationalIdNumber[3:]
    # D numbers: 4 is added to the first digit, i.e. the first digit of day.
    # Hence, D numbers have days between 41 and 71
    day = getDayInNationallIdNumber(nationalIdNumber)
    d = int(nationalIdNumber[0], 10)
    if day > 40 and day < 72:
        return str(d - 4) + nationalIdNumber[(len(nationalIdNumber) - 10):]
    return nationalIdNumber

def passesDateTest(nationalIdNumber):
    try:
        day = getDayInNationallIdNumber(nationalIdNumber)
        month = getMonthInNationalIdNumber(nationalIdNumber)
        year = getYearInNationalIdNumber(nationalIdNumber)
        currentYear = getCurrentYear()
        daysInMonth = getDaysInMonth(month, year)        
        if year < 1900 or year > currentYear:
            return False
        if day < 1 or day > daysInMonth:
            return False
        if month < 1 or month > 12:
            return False        
    except Exception as err:
        return False
    return True

def getCurrentYear():
    return datetime.datetime.now().year

def getDayInNationallIdNumber(nationalIdNumber):
    return int(nationalIdNumber[0:2], 10)

def getMonthInNationalIdNumber(nationalIdNumber):
    return int(nationalIdNumber[2:4], 10)

def getYearInNationalIdNumber(nationalIdNumber):
        # Individual number is first three digits of the five-digit national id
        # number:
        individualNumber = int(nationalIdNumber[6: len(nationalIdNumber)- 2], 10)
        twoDigitYear = int(nationalIdNumber[4:6], 10)
        fourDigitYear = 0
        # Born between 1900-1999:
        if individualNumber < 500:
            fourDigitYear = twoDigitYear + 1900
            # Born between 1854-1899:
        elif individualNumber >= 500 and individualNumber < 750 and twoDigitYear >= 54:
            fourDigitYear = twoDigitYear + 1800
            # Born between 2000-2039:
        elif individualNumber >= 500 and individualNumber <= 999 and twoDigitYear < 40:
            fourDigitYear = twoDigitYear + 2000
            # Born between 1940-1999:
        elif individualNumber >= 900 and individualNumber <= 999 and twoDigitYear >= 40:
            fourDigitYear = twoDigitYear + 1900
        else:
            print "Illegal individual number: " + individualNumber

        return fourDigitYear


def getDaysInMonth(month, year):
    days = 31
    if month is 2:
        days = 29 if ((year % 4 is 0) and (year % 100 is not 0)) or (year % 400 is 0) else 28        
    elif (month is 4 or month is 6 or month is 9 or month is 11):
        days = 30
    return days
if __name__ == '__main__':
    print("This is a test result which is shown when %s is executed rather than imported" % __file__)
    print isValidNationalIdNumber('1234567890')
    exit()	

