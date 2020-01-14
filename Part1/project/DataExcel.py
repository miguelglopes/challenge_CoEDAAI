from data import config  # local
import pandas
import logging
from datetime import datetime
import xlrd


class ExcelFile:
    """
    Class that contains every needed information about the excel file, including its data.
    """

    def __init__(self, file: str = config.dataFile["nameS"], sheet: str = config.dataFile["sheetS"]):
        """
        Instantiates the class, including file, sheet, date of creation and dataframe

        Keyword Arguments:
            file {str} -- Excel file to be read (default: {config.dataFile["nameS"]})
            sheet {str} -- Excel sheet of the excel file (default: {config.dataFile["sheetS"]})
        """

        self.__file = file
        self.__sheet = sheet
        self.dataFrame = None
        # to get the date
        workbook = xlrd.open_workbook(self.__file)
        worksheet = workbook.sheet_by_name(self.__sheet)
        self.date = datetime.strptime(worksheet.cell(0, 1).value, "%d/%m/%Y %H:%M")
        self.__setDataFrame()

    def __setDataFrame(self):
        """
        Reads the excel data from the excel file. Preprocesses the information and stores it in a pandas dataframe. Creates new brands column.
        """

        # get data
        self.dataFrame = pandas.read_excel(self.__file, sheet_name=self.__sheet,
                                           skiprows=[0, 1, 2], header=0, dtype=str)

        # check if we have unknown columns.
        # Replace comma by point for float columns (numbers are formatted as text)
        for column in self.dataFrame.columns:
            if column not in config.columns["dataTypes"].keys():
                logging.warning("Column " + column +
                                " found in data file but is not in the configuration.")
            elif config.columns["dataTypes"][column] is float:
                self.dataFrame[column] = self.dataFrame[column].replace(',', '.', regex=True)

        # set data types. This is mandatory, otherwise, for instance, postal codes would be read as int, and we'd lose information
        self.dataFrame = self.dataFrame.astype(config.columns["dataTypes"])

        # generate new brands column
        self.dataFrame[config.rotulo["newS"]] = self.dataFrame[config.rotulo["originalS"]].apply(
            lambda row: ExcelFile.__compareBandStrings(row))

        logging.info("Loaded " + str(self.dataFrame.shape[0]) + " columns and " + str(
            self.dataFrame.shape[1]) + " rows from " + config.dataFile["nameS"] + " into memory. New brands column successfully created.")

    @staticmethod
    def __compareBandStrings(inputS: str) -> str:
        """
        Compares a string to the list of brands in config.rotulo["brandsL"]

        Arguments:
            inputS {string} -- Any string to compare to the list of brands 

        Returns:
            string -- returns one of the brands in config.rotulo["brandsL"] if inputS contains it
            or the string config.rotulo["otherS"] otherwise.
        """

        for brand in config.rotulo["brandsL"]:
            if brand in inputS:
                return brand

        return config.rotulo["otherS"]

        # TODO: what if it contains more than one brand? This was not taken into account.
