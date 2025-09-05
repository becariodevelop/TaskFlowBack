-- DML TaskFlowAD
INSERT INTO task_flow_ad_db_dev.unidad_organizativa(nombre_unidad)
VALUES
('MENUDEO'),
('MAYOREO'),
('MAQUILAS'),
('DHARMALINE'),
('NEEN'),
('NUVAH'),
('MINIPISOS'),
('ADMINISTRACIÓN'),
('AGENCIA DIGITAL');

INSERT INTO task_flow_ad_db_dev.celula_ad(id_unidad_organizativa, nombre_celula)
VALUES
(9,'FORMULACIONES'),         -- id_celula_ad = 1
(9,'DESARROLLO WEB'),        -- id_celula_ad = 2
(9,'EMPAQUE'),               -- id_celula_ad = 3
(9,'DISEÑO SOCIAL'),         -- id_celula_ad = 4
(9,'DISEÑO AUDIOVISUAL');    -- id_celula_ad = 5

INSERT INTO task_flow_ad_db_dev.puesto(nombre_puesto, id_celula_ad)
VALUES
('Gerente',1),       -- id_puesto = 1
('Coordinador',2),   -- id_puesto = 2
('Colaborador',3),   -- id_puesto = 3
('Practicante',4);   -- id_puesto = 4

INSERT INTO task_flow_ad_db_dev.estatus_colaborador(estatus)
VALUES
('Activo'),   -- id_estatus_colaborador = 1
('Inactivo'); -- id_estatus_colaborador = 2

INSERT INTO task_flow_ad_db_dev.roles_acceso(rol_acceso)
VALUES
('GerenteADMaster'),  -- id_tipo_rol_acceso = 1
('Gerente'),          -- id_tipo_rol_acceso = 2
('CoordinadorAD'),    -- id_tipo_rol_acceso = 3
('Coordinador'),      -- id_tipo_rol_acceso = 4
('Colaborador');      -- id_tipo_rol_acceso = 5

INSERT INTO task_flow_ad_db_dev.estado_solicitud_actividad(nombre_estado_actividad)
VALUES
('Enviada'),          -- id_estado_solicitud = 1
('Aprobada/EnProceso'), -- id_estado_solicitud = 2
('Denegada'),         -- id_estado_solicitud = 3
('Realizada');        -- id_estado_solicitud = 4


INSERT INTO task_flow_ad_db_dev.estado_notificacion_solicitud_actividad(nombre_estado_notificacion)
VALUES
('Enviada'), -- id_estado_notificacion = 1
('Vista');   -- id_estado_notificacion = 2

--DQL General, no son los casos específicos

SELECT * FROM task_flow_ad_db_dev.unidad_organizativa;

SELECT * FROM task_flow_ad_db_dev.celula_ad;

SELECT * FROM task_flow_ad_db_dev.puesto;

SELECT * FROM task_flow_ad_db_dev.estatus_colaborador;

SELECT * FROM task_flow_ad_db_dev.roles_acceso;

SELECT * FROM task_flow_ad_db_dev.estado_solicitud_actividad;

SELECT * FROM task_flow_ad_db_dev.estado_notificacion_solicitud_actividad;


