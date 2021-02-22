# import tempfile
# import os

# try:
#     import pandas as pd
# except ImportError:
#     import pip

#     pip.main(["install", "pandas"])
#     import pandas as pd


# with tempfile.TemporaryDirectory() as td:
#     f_name = os.path.join(td, "test.csv")

#     layer = iface.activeLayer()

#     QgsVectorFileWriter.writeAsVectorFormat(
#         layer,
#         f_name,
#         fileEncoding="utf-8",
#         driverName="CSV",
#     )
#     print(f_name)
#     data = pd.read_csv(f_name)
#     print(data.head())
#     print(f_name)

# import pip

# pip.main()