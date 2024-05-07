from flask import Blueprint
from flask import request
from src.core.models.config_model import Config
from src.core.models.request_model import Request
from src.core.models.user_model import User
from src.core.models.service_model import Service
from src.core.models.type_model import Type

api_stats_bp = Blueprint("stats_api", __name__, url_prefix="/api/stats")

@api_stats_bp.get("/")
def stats_Uno():
    try:
        estado={ "Creada":0,"Aceptada":0, "EnProceso":0, "Finalizada":0, "Rechazada":0, "Cancelada":0}
        re = Request.query.all()   

        for r in re:

            if r.current_status == "Creada":
                estado["Creada"]+= 1
            if r.current_status == "Aceptada":
                estado["Aceptada"]+= 1
            elif r.current_status == "En proceso":
                estado["EnProceso"]+= 1
            elif r.current_status == "Finalizada":
                estado["Finalizada"]= estado["Finalizada"] + 1
            elif r.current_status == "Rechazada":
                estado["Rechazada"]= estado["Rechazada"] + 1
            elif r.current_status == "Cancelada":
                estado["Cancelada"]= estado["Cancelada"] + 1

        return estado, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500
    


@api_stats_bp.get("/Barra")
def stats_UsuariosPorAño():
    try:
        user = User.get_all()
        #dic_mes_cant={ "Enero":0, "Febrero":0, "Marzo":0, "Abril":0, "Mayo":0, "Junio":0,
         #     "Julio":0, "Agosto":0, "Septiembre":0, "Octubre":0, "Noviembre":0, "Diciembre":0 }
              
        dic_mes_cant={ "January":0, "February":0, "March":0, "April":0, "May":0, "June":0,
              "July":0, "August":0, "September":0, "October":0, "November":0, "December":0 }
              
        for u in user:
            #obtengo fecha
            fecha = u.get_fecha() 
            #corto el mes      
            mes = fecha.strftime('%B')  
            #totalizo el mes
            dic_mes_cant[mes]+=1

        resp = dic_mes_cant
        return resp, 200

    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500


@api_stats_bp.get("/Barra2")
def stats_Barra():
    """ En re me quedo con todos los registros de la tabla servicios 
    En el bucle for chequeo cuantos servicios por tipo existen"""
    try:
        estado = {"Analisis": 0, "Desarrollo": 0, "Consultoria": 0}
        re = Service.query.all() 
        for r in re:
            if (r.habilite):
                if r.type.name == "Análisis":
                    estado["Analisis"] += 1
                elif r.type.name == "Desarrollo":
                    estado["Desarrollo"] += 1
                elif r.type.name == "Consultoria":
                    estado["Consultoria"] += 1

        return estado, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500
