from util.util import Util as Ut
from util.buissnes import Bussines

class Remesa:
    conexion = None
    parameter_remesa = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_remesa = {
            "get": {
                "field": ["remesa_codigo", "remesa_cencoscodigo", "cencos_codigo", "empresa_codigo", "manifiesto_codigo"],
                "table": "tb_remesa",
                "where": " ",
            },
            "merge": {
                "on": "remesa_codigo",
                "how-inner": "inner",
                "how-left": "left",
                "how-right": "right",
            }
        }

    def get_remesa(self, dataframe_pivote):
        lista_manifiestos = list(dataframe_pivote["manifiesto_codigo"].fillna(0))
        where_manifiesto = Ut.configure_field(lista_manifiestos).replace("'", "")
        self.parameter_remesa["get"]["where"] = "manifiesto_codigo IN ( " + where_manifiesto + ")"

        df_remesa = Ut.get_dataframe(self.parameter_remesa, self.conexion)
        df_list_codigo_impreso = df_remesa[["remesa_codigo", "cencos_codigo", "empresa_codigo","remesa_cencoscodigo"]]
        df_codigo_impreso = Bussines(self.conexion).get_codigo_impreso(df_list_codigo_impreso)
        df_remesa = Ut.merge_dataframe(df_remesa, df_codigo_impreso,
                                           self.parameter_remesa["merge"]["how-left"],
                                           self.parameter_remesa["merge"]["on"])

        return df_remesa