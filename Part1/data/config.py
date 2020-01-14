import logging

dataFile = {
    "nameS": r"Part1\data\preciosEESS_es.xls",
    "sheetS": "Page 1"
}

columns = {
    "dataTypes": {
        "Provincia": str,
        "Municipio": str,
        "Localidad": str,
        "Código postal": str,
        "Dirección": str,
        "Margen": str,
        "Longitud": float,
        "Latitud": float,
        "Precio gasolina 95": float,
        "Precio gasóleo A": float,
        "Precio gasóleo B": float,
        "Precio bioetanol": float,
        "Precio nuevo gasóleo A": float,
        "Precio biodiesel": float,
        "% éster metílico": float,
        "% bioalcohol": float,
        "Precio gasolina 98": float,
        "Precio gas natural comprimido": float,
        "Precio gas natural licuado": float,
        "Precio gases licuados del petróleo": float,
        "Rótulo": str,
        "Tipo venta": str,
        "Rem.": str,
        "Horario": str
    },
    "productColumns": ["Precio gasolina 95", "Precio gasóleo A", "Precio gasóleo B", "Precio bioetanol", 
                        "Precio nuevo gasóleo A", "Precio biodiesel", "% éster metílico", "% bioalcohol",
                        "Precio gasolina 98", "Precio gas natural comprimido", "Precio gas natural licuado",
                        "Precio gases licuados del petróleo"]
}

rotulo = {
    "originalS": "Rótulo",
    "newS": "Brands",
    "brandsL": ["ALCAMPO", "BALLENOIL", "BP", "CAMPSA", "CARREFOUR", "CEPSA", "E.LECLERC", "EROSKI", "GALP",
                "GAS EXPRESS", "PETRONOR", "PETROPRIX", "REPSOL", "REPOSTA", "SHELL"],
    "otherS": "OTHER"
}

DBConnectString = "mysql://admin:Temporal10$@pythontest.cadum2ishgbe.eu-west-1.rds.amazonaws.com:3306/stations?charset=utf8mb4"

logging.getLogger().setLevel(logging.INFO)
