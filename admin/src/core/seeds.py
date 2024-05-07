from src.core.database import db
from src.core import models

def run():
    p_user_index = models.create_permission(name="user_index")
    p_user_create = models.create_permission(name="user_create")
    p_user_destroy = models.create_permission(name="user_destroy")
    p_user_update = models.create_permission(name="user_update")
    p_user_show = models.create_permission(name="user_show")
    p_institution_index = models.create_permission(name="institution_index")
    p_institution_create = models.create_permission(name="institution_create")
    p_institution_destroy = models.create_permission(name="institution_destroy")
    p_institution_update = models.create_permission(name="institution_update")
    p_institution_show = models.create_permission(name="institution_show")
    p_institution_activate = models.create_permission(name="institution_activate")
    p_institution_deactivate = models.create_permission(name="institution_deactivate")
    p_role_index = models.create_permission(name="role_index")
    p_role_create = models.create_permission(name="role_create")
    p_role_destroy = models.create_permission(name="role_destroy")
    p_role_update = models.create_permission(name="role_update")
    p_service_index = models.create_permission(name="service_index")
    p_service_create = models.create_permission(name="service_create")
    p_service_destroy = models.create_permission(name="service_destroy")
    p_service_update = models.create_permission(name="service_update")
    p_service_show = models.create_permission(name="service_show")
    p_request_index = models.create_permission(name="request_index")
    p_request_show = models.create_permission(name="request_show")
    p_request_update = models.create_permission(name="request_update")
    p_request_destroy = models.create_permission(name="request_destroy")
    p_config_show = models.create_permission(name="config_show")
    p_config_update = models.create_permission(name="config_update")

    r_superadmin = models.create_role(name="Super Administrador")
    r_owner = models.create_role(name="Dueño")
    r_admin = models.create_role(name="Administrador")
    r_operator = models.create_role(name="Operador")

    r_superadmin.add_permission(p_user_index)
    r_superadmin.add_permission(p_user_create)
    r_superadmin.add_permission(p_user_update)
    r_superadmin.add_permission(p_user_show)
    r_superadmin.add_permission(p_user_destroy)
    r_superadmin.add_permission(p_institution_index)
    r_superadmin.add_permission(p_institution_create)
    r_superadmin.add_permission(p_institution_update)
    r_superadmin.add_permission(p_institution_show)
    r_superadmin.add_permission(p_institution_destroy)
    r_superadmin.add_permission(p_institution_activate)
    r_superadmin.add_permission(p_institution_deactivate)
    r_superadmin.add_permission(p_config_show)
    r_superadmin.add_permission(p_config_update)
    '''Agrego permisos para CRUD de Servicios al superadmin'''
    r_superadmin.add_permission(p_role_index)
    r_superadmin.add_permission(p_role_create)
    r_superadmin.add_permission(p_role_update)
    r_superadmin.add_permission(p_role_destroy)
    r_superadmin.add_permission(p_service_index)
    r_superadmin.add_permission(p_service_create)
    r_superadmin.add_permission(p_service_update)
    r_superadmin.add_permission(p_service_show)
    r_superadmin.add_permission(p_service_destroy)
    r_superadmin.add_permission(p_request_index)
    r_superadmin.add_permission(p_request_show)
    r_superadmin.add_permission(p_request_update)


    r_owner.add_permission(p_role_index)
    r_owner.add_permission(p_role_create)
    r_owner.add_permission(p_role_update)
    r_owner.add_permission(p_role_destroy)
    r_owner.add_permission(p_service_index)
    r_owner.add_permission(p_service_create)
    r_owner.add_permission(p_service_update)
    r_owner.add_permission(p_service_show)
    r_owner.add_permission(p_service_destroy)
    r_owner.add_permission(p_request_index)
    r_owner.add_permission(p_request_show)
    r_owner.add_permission(p_request_update)
    r_owner.add_permission(p_request_destroy)
    r_admin.add_permission(p_service_index)
    r_admin.add_permission(p_service_create)
    r_admin.add_permission(p_service_update)
    r_admin.add_permission(p_service_show)
    r_admin.add_permission(p_service_destroy)
    r_admin.add_permission(p_request_index)
    r_admin.add_permission(p_request_show)
    r_admin.add_permission(p_request_update)
    r_admin.add_permission(p_request_destroy)
    r_operator.add_permission(p_service_index)
    r_operator.add_permission(p_service_create)
    r_operator.add_permission(p_service_update)
    r_operator.add_permission(p_service_show)
    r_operator.add_permission(p_request_index)
    r_operator.add_permission(p_request_show)
    r_operator.add_permission(p_request_update)

    # creacion usuario super administrador
    superAdmin = models.crear_usuario(
        username="super",
        password="1234",
        email="super@gmail.com",
        first_name="Super",
        last_name="Super",
    )

    superAdmin.add_role(role=r_superadmin)

    dueño = models.crear_usuario(
        username="dueño",
        password="1234",
        email="dueno@gmail.com",
        first_name="dueño",
        last_name="dueño",
    )

    admin = models.crear_usuario(
        username="admin",
        password="1234",
        email="admin@gmail.com",
        first_name="admin",
        last_name="admin",
    )

    operador = models.crear_usuario(
        username="operador",
        password="1234",
        email="operador@gmail.com",
        first_name="operador",
        last_name="operador",
    )

    # creacion instituciones
    institution1 = models.create_institution(
        name="Institución 1",
        information="Información 1",
        address="Dirección 1",
        location="-34.9033059;-57.937703",
        web="https://www.institucion1.com",
        keywords_list=["Palabra clave 1", "Palabra clave 2"],
        date_time="Horario 1",
        contact="Contacto 1",
    )
    institution2 = models.create_institution(
        name="Institución 2",
        information="Información 2",
        address="Dirección 2",
        location="-34.9033059;-57.937703",
        web="https://www.institucion2.com",
        keywords_list=["Palabra clave 1", "Palabra clave 2"],
        date_time="Horario 2",
        contact="Contacto 2",
    )
    institution3 = models.create_institution(
        name="Institución 3",
        information="Información 3",
        address="Dirección 3",
        location="-34.9033059;-57.937703",
        web="https://www.institucion3.com",
        keywords_list=["Palabra clave 1", "Palabra clave 2"],
        date_time="Horario 3",
        contact="Contacto 3",
    )
    institution4 = models.create_institution(
        name="Institución 4",
        information="Información 4",
        address="Dirección 4",
        location="-34.9033059;-57.937703",
        web="https://www.institucion4.com",
        keywords_list=["Palabra clave 1", "Palabra clave 2"],
        date_time="Horario 4",
        contact="Contacto 4",
    )
    institution5 = models.create_institution(
        name="Institución 5",
        information="Información 5",
        address="Dirección 5",
        location="-34.9033059;-57.937703",
        web="https://www.institucion5.com",
        keywords_list=["Palabra clave 1", "Palabra clave 2"],
        date_time="Horario 5",
        contact="Contacto 5",
    )

    type1 = models.create_type(name="Análisis")
    type2 = models.create_type(name="Consultoria")
    type3 = models.create_type(name="Desarrollo")

    # creacion servicios
    service1 = models.create_service(
        title="Servicio 1",
        description="Descripción 1",
        keywords_list=["PalabraClave1", "PalabraClave2"],
        type_id = type1.id,
    )
    service2 = models.create_service(
        title="Servicio 2",
        description="Descripción 2",
        keywords_list=["PalabraClave1", "PalabraClave2"],
        type_id = type2.id,
    )
    service3 = models.create_service(
        title="Servicio 3",
        description="Descripción 3",
        keywords_list=["PalabraClave1", "PalabraClave2"],
        type_id = type3.id,
    )
    service4 = models.create_service(
        title="Servicio 4",
        description="Descripción 4",
        keywords_list=["PalabraClave1", "PalabraClave2"],
        type_id = type1.id,
    )
    institution1.add_service(service1)
    institution2.add_service(service2)
    institution3.add_service(service3)
    institution1.add_service(service4)

    # creacion configuracion
    config = models.create_config(
        cant=4,
        contact="(0221) 6543211",
        email="admin@gmail.com",
        state=True,
        information = "Sistema en Mantenimiento",
    )

    # creación de estados de solicitudes
    status1 = models.create_request_status(name="Creada")
    status2 = models.create_request_status(name="Aceptada")
    status3 = models.create_request_status(name="En proceso")
    status4 = models.create_request_status(name="Finalizada")
    status5 = models.create_request_status(name="Rechazada")
    status6 = models.create_request_status(name="Cancelada")