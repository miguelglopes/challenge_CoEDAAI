from data import config  # local
from DataExcel import ExcelFile  # local, only for type hinting
from pandas.core.series import Series  # only for type hinting
from datetime import datetime  # only for type hinting
import SQLModel
from SQLModel import Provincia, Municipio, Localidad, Margen, Producto, Venta, Station, Price, Brands, Rem
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.session import Session


def __connectToDB():
    """
    Test connection to the database.
    """

    try:
        SQLModel.engine.connect()
    except OperationalError:
        logging.error("Unable to connect to the database. Check the connection string.")
        raise


def createTablesSchema():
    """
    Create database schema based on the SLQModel
    """

    __connectToDB()
    SQLModel.Base.metadata.create_all(SQLModel.engine)
    logging.info("Tables " + str(list(SQLModel.Base.metadata.tables.keys())) + " successfully created in the database.")


def insertPdTableToDB(dataFile: ExcelFile):
    """
    Persists the data contained in the dataFile to the database

    Arguments:
        dataFile {ExcelFile} - Object containing the data to be persisted
    """

    __connectToDB()
    Session = sessionmaker(bind=SQLModel.engine)
    session = Session()

    data = dataFile.dataFrame

    # convert dataframe to "SQL friendly"
    nonProductColumns = set(data.columns) - set(config.columns["productColumns"])
    newData = data.melt(id_vars=nonProductColumns, var_name="Producto", value_name="Precio")
    newData = newData.dropna(subset=['Precio'])

    logging.info("Inserting data to the database. Depending on the number of rows, this may take a while...")

    # insert row 1 by 1
    #newData.apply(lambda row: __addRowToSession(session, row, dataFile.date), axis=1)
    newData.apply(lambda row: __addRowToSession(session, row, dataFile.date), axis=1)

    # commit session
    session.commit()
    session.close()
    logging.info("Successfully persisted the data to the database.")
    # TODO COUNT affected rows. Requires further investigation


def __addRowToSession(session: Session, row: Series, fecha: datetime):
    """ 
    Add row of data to the database session to, eventually, be persisted to the database

    Arguments:
        session {Session} -- SQLAlchemy session
        row {Series} -- Data to be added to the session
        fecha {datetime} -- Date when the data was created
    """

    # TODO
    # The best way I found in order to not get integrity errors, was to try to get the information from the database and, if there isn't create it.
    # However, this probably isn't the most efficient way to do it. For this reason, this method takes a lot of time, depending on the number of rows.
    # Requires Further investigation.

    try:
        provincia = session.query(Provincia).filter(Provincia.Name == row["Provincia"]).one()
    except NoResultFound:
        provincia = Provincia(Name=row["Provincia"])

    try:
        municipio = session.query(Municipio).filter(Municipio.Name == row["Municipio"]).one()
    except NoResultFound:
        municipio = Municipio(Name=row["Municipio"], Provincia=provincia)

    try:
        localidad = session.query(Localidad).filter(Localidad.Name == row["Localidad"]).one()
    except NoResultFound:
        localidad = Localidad(Name=row["Localidad"], Municipio=municipio)

    try:
        margen = session.query(Margen).filter(Margen.Name == row["Margen"]).one()
    except NoResultFound:
        margen = Margen(ID=row["Margen"], Name=row["Margen"])

    try:
        station = session.query(Station).filter(Station.Longitud == row["Longitud"]).filter(
            Station.Latitud == row["Latitud"]).filter(Station.MargenID == row["Margen"]).one()
    except NoResultFound:
        station = Station(CodigoPostal=row["Código postal"], Localidad=localidad, Direccion=row["Dirección"],
                          Longitud=row["Longitud"], Latitud=row["Latitud"], Margen=margen)

    try:
        producto = session.query(Producto).filter(Producto.Name == row["Producto"]).one()
    except NoResultFound:
        producto = Producto(Name=row["Producto"])

    try:
        brands = session.query(Brands).filter(Brands.Name == row["Brands"]).one()
    except NoResultFound:
        brands = Brands(Name=row["Brands"])

    try:
        venta = session.query(Venta).filter(Venta.Name == row["Tipo venta"]).one()
    except NoResultFound:
        venta = Venta(Name=row["Tipo venta"], ID=row["Tipo venta"])

    try:
        rem = session.query(Rem).filter(Rem.Name == row["Rem."]).one()
    except NoResultFound:
        rem = Rem(Name=row["Rem."], ID=row["Rem."])

    if session.query(Price).filter(Price.ProductoID == producto.ID).filter(Price.StationID == station.ID).filter(Price.Fecha == fecha).scalar() == None:
        newRow = Price(Precio=row["Precio"], Rotulo=row["Rótulo"], Fecha=fecha.strftime("%Y/%m/%d %H:%M:%S"), Producto=producto, Station=station, Brands=brands,
                         Venta=venta, Rem=rem, Horario=row["Horario"])
        session.merge(newRow)
