from data import config  # local
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, CHAR, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# create sql engine
# this doesnt connect yet to the database
engine = create_engine(config.DBConnectString)
Base = declarative_base()


class Provincia(Base):
    __tablename__ = "Provincia"
    __table_args__ = (UniqueConstraint("Name", name="_nameProv_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Margen(Base):
    __tablename__ = "Margen"

    ID = Column(CHAR(1), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Producto(Base):
    __tablename__ = "Producto"
    __table_args__ = (UniqueConstraint("Name", name="_nameProd_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Venta(Base):
    __tablename__ = "Venta"

    ID = Column(CHAR(1), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Rem(Base):
    __tablename__ = "Rem"

    ID = Column(CHAR(2), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Brands(Base):
    __tablename__ = "Brands"
    __table_args__ = (UniqueConstraint("Name", name="_nameBrand_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String(50), nullable=False)


class Municipio(Base):
    __tablename__ = "Municipio"
    __table_args__ = (UniqueConstraint("Name", name="_nameMun_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String(50), nullable=False)
    ProvinciaID = Column(Integer, ForeignKey("Provincia.ID"), nullable=False)
    Provincia = relationship("Provincia")


class Localidad(Base):
    __tablename__ = "Localidad"
    __table_args__ = (UniqueConstraint("Name", name="_nameLocal_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Name = Column(String(50), nullable=False)
    MunicipioID = Column(Integer, ForeignKey("Municipio.ID"), nullable=False)
    Municipio = relationship("Municipio")


class Station(Base):
    __tablename__ = "Station"
    __table_args__ = (UniqueConstraint("Longitud", "Latitud", "MargenID", name="_PC_uc"),)

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    CodigoPostal = Column(CHAR(5), nullable=False)
    Direccion = Column(String(300), nullable=False)
    Longitud = Column(Numeric(20, 10), nullable=False)
    Latitud = Column(Numeric(20, 10), nullable=False)
    MargenID = Column(CHAR(1), ForeignKey("Margen.ID"), nullable=False)
    Margen = relationship("Margen")
    LocalidadID = Column(Integer, ForeignKey("Localidad.ID"), nullable=False)
    Localidad = relationship("Localidad")


class Price(Base):
    __tablename__ = "Price"
    __table_args__ = (UniqueConstraint("ProductoID", "StationID", "Fecha", name="_PSF_uc"),)
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Precio = Column(Numeric(20, 10), nullable=False)
    Rotulo = Column(String(300), nullable=False)
    Fecha = Column(DateTime, nullable=False)
    ProductoID = Column(Integer, ForeignKey("Producto.ID"), nullable=False)
    Producto = relationship("Producto")
    StationID = Column(Integer, ForeignKey("Station.ID"), nullable=False)
    Station = relationship("Station")
    BrandsID = Column(Integer, ForeignKey("Brands.ID"), nullable=False)
    Brands = relationship("Brands")
    VentaID = Column(CHAR(1), ForeignKey("Venta.ID"), nullable=False)
    Venta = relationship("Venta")
    RemID = Column(CHAR(2), ForeignKey("Rem.ID"), nullable=False)
    Rem = relationship("Rem")
    Horario = Column(String(200), nullable=False)
