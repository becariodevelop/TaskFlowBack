-- Esquema
CREATE SCHEMA IF NOT EXISTS task_flow_ad_db_dev;

-------------------------------------------------------
-- Unidad Organizativa
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.unidad_organizativa(
    id_unidad_organizativa SERIAL PRIMARY KEY,
    nombre_unidad VARCHAR(100) NOT NULL
);

-------------------------------------------------------
-- Célula AD
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.celula_ad(
    id_celula_ad SERIAL PRIMARY KEY,
    id_unidad_organizativa INT NOT NULL,
    nombre_celula VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_unidad_organizativa)
        REFERENCES task_flow_ad_db_dev.unidad_organizativa(id_unidad_organizativa)
);

-------------------------------------------------------
-- Puesto
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.puesto(
    id_puesto SERIAL PRIMARY KEY,
    nombre_puesto VARCHAR(200) NOT NULL,
    id_celula_ad INT NOT NULL,
    FOREIGN KEY (id_celula_ad)
        REFERENCES task_flow_ad_db_dev.celula_ad(id_celula_ad)
);

-------------------------------------------------------
-- Estatus Colaborador
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.estatus_colaborador(
    id_estatus_colaborador SERIAL PRIMARY KEY,
    estatus VARCHAR(50) NOT NULL
);

-------------------------------------------------------
-- Colaborador
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.colaborador(
    id_colaborador SERIAL PRIMARY KEY,
    nombre_colaborador VARCHAR(100) NOT NULL,
    descripcion_puesto VARCHAR(200),
    id_puesto INT NOT NULL,
    id_celula_ad INT NOT NULL,
    id_unidad_organizativa INT NOT NULL,
    horas_diarias INT NOT NULL,
    horas_mes INT NOT NULL,
    id_estatus_colaborador INT NOT NULL,
    FOREIGN KEY (id_puesto) REFERENCES task_flow_ad_db_dev.puesto(id_puesto),
    FOREIGN KEY (id_celula_ad) REFERENCES task_flow_ad_db_dev.celula_ad(id_celula_ad),
    FOREIGN KEY (id_unidad_organizativa) REFERENCES task_flow_ad_db_dev.unidad_organizativa(id_unidad_organizativa),
    FOREIGN KEY (id_estatus_colaborador) REFERENCES task_flow_ad_db_dev.estatus_colaborador(id_estatus_colaborador)
);

-------------------------------------------------------
-- Roles de Acceso
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.roles_acceso(
    id_tipo_rol_acceso SERIAL PRIMARY KEY,
    rol_acceso VARCHAR(100) NOT NULL
);

-------------------------------------------------------
-- Usuario
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.usuario(
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(200) NOT NULL,
    clave VARCHAR(200) NOT NULL,
    id_colaborador INT NOT NULL,
    id_tipo_rol_acceso INT NOT NULL,
    FOREIGN KEY (id_colaborador) REFERENCES task_flow_ad_db_dev.colaborador(id_colaborador),
    FOREIGN KEY (id_tipo_rol_acceso) REFERENCES task_flow_ad_db_dev.roles_acceso(id_tipo_rol_acceso)
);

-------------------------------------------------------
-- Catálogo de Actividades
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.catalogo_actividades(
    id_actividad SERIAL PRIMARY KEY,
    nombre_actividad VARCHAR(200) NOT NULL,
    horas_actividad_empleadas_promedio NUMERIC(12,2),
    id_celula_ad INT NOT NULL,
    costo_unitario NUMERIC(12,2),
    FOREIGN KEY (id_celula_ad) REFERENCES task_flow_ad_db_dev.celula_ad(id_celula_ad)
);

-------------------------------------------------------
-- Estado Solicitud Actividad
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.estado_solicitud_actividad(
    id_estado_solicitud SERIAL PRIMARY KEY,
    nombre_estado_actividad VARCHAR(200) NOT NULL
);

-------------------------------------------------------
-- Estado Notificación Solicitud
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.estado_notificacion_solicitud_actividad(
    id_estado_notificacion SERIAL PRIMARY KEY,
    nombre_estado_notificacion VARCHAR(50) NOT NULL
);

-------------------------------------------------------
-- Solicitud Actividad
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.solicitud_actividad(
    id_solicitud SERIAL PRIMARY KEY,
    id_celula_ad INT NOT NULL,
    nombre_actividad VARCHAR(200) NOT NULL,
    descripcion_solicitud VARCHAR(200),
    id_estado_solicitud INT NOT NULL,
    id_usuario_solicitante INT NOT NULL,
    FOREIGN KEY (id_celula_ad) REFERENCES task_flow_ad_db_dev.celula_ad(id_celula_ad),
    FOREIGN KEY (id_estado_solicitud) REFERENCES task_flow_ad_db_dev.estado_solicitud_actividad(id_estado_solicitud),
    FOREIGN KEY (id_usuario_solicitante) REFERENCES task_flow_ad_db_dev.usuario(id_usuario)
);

-------------------------------------------------------
-- Notificación Solicitud Actividad
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.notificacion_solicitud_actividad(
    id_notificacion SERIAL PRIMARY KEY,
    id_usuario_destino INT NOT NULL,
    id_solicitud INT NOT NULL,
    id_actividad INT NOT NULL,
    id_estado_solicitud INT NOT NULL,
    id_estado_notificacion INT NOT NULL,
    mensaje VARCHAR(200),
    creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario_destino) REFERENCES task_flow_ad_db_dev.usuario(id_usuario),
    FOREIGN KEY (id_solicitud) REFERENCES task_flow_ad_db_dev.solicitud_actividad(id_solicitud),
    FOREIGN KEY (id_actividad) REFERENCES task_flow_ad_db_dev.catalogo_actividades(id_actividad),
    FOREIGN KEY (id_estado_solicitud) REFERENCES task_flow_ad_db_dev.estado_solicitud_actividad(id_estado_solicitud),
    FOREIGN KEY (id_estado_notificacion) REFERENCES task_flow_ad_db_dev.estado_notificacion_solicitud_actividad(id_estado_notificacion)
);

-------------------------------------------------------
-- Bitácora Actividad AD
-------------------------------------------------------
CREATE TABLE task_flow_ad_db_dev.bitacora_actividad_ad(
    id_bitacora_registro SERIAL PRIMARY KEY,
    fecha_registro DATE NOT NULL,
    id_celula_ad INT NOT NULL,
    nombre_celula VARCHAR(200),
    id_colaborador INT NOT NULL,
    nombre_colaborador VARCHAR(200),
    id_actividad INT NOT NULL,
    nombre_actividad VARCHAR(200),
    cantidad INT,
    id_unidad_organizativa INT NOT NULL,
    nombre_unidad_organizativa_cliente VARCHAR(200),
    FOREIGN KEY (id_celula_ad) REFERENCES task_flow_ad_db_dev.celula_ad(id_celula_ad),
    FOREIGN KEY (id_colaborador) REFERENCES task_flow_ad_db_dev.colaborador(id_colaborador),
    FOREIGN KEY (id_actividad) REFERENCES task_flow_ad_db_dev.catalogo_actividades(id_actividad),
    FOREIGN KEY (id_unidad_organizativa) REFERENCES task_flow_ad_db_dev.unidad_organizativa(id_unidad_organizativa)
);