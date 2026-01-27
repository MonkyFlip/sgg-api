-- ============================================
-- SISTEMA GESTOR DE GIMNASIOS (SGG)
-- Base de Datos MySQL
-- ============================================

-- Base de Datos
CREATE DATABASE sgg;
USE sgg;

-- TABLA: gimnasios
-- Almacena información de cada gimnasio registrado en el sistema
CREATE TABLE gimnasios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    direccion VARCHAR(300),
    telefono VARCHAR(20),
    email VARCHAR(150) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    codigo_unico VARCHAR(50) UNIQUE NOT NULL, -- Código único para identificar el gimnasio
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLA: roles
-- Define los roles del sistema
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE, -- super_admin, admin, entrenador, cliente
    descripcion VARCHAR(255),
    permisos JSON -- Almacena permisos específicos del rol
);

-- TABLA: usuarios
-- Almacena todos los usuarios del sistema
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    rol_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    genero ENUM('masculino', 'femenino', 'otro'),
    foto_perfil_url VARCHAR(500),
    direccion VARCHAR(300),
    documento_identidad VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- TABLA: membresias_tipos
-- Define los tipos de membresías disponibles
CREATE TABLE membresias_tipos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL, -- Mensual, Trimestral, Anual, etc.
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    duracion_dias INT NOT NULL, -- Duración en días
    beneficios JSON, -- Lista de beneficios incluidos
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE
);

-- TABLA: membresias
-- Almacena las membresías activas/históricas de los clientes
CREATE TABLE membresias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    membresia_tipo_id INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('activa', 'vencida', 'cancelada', 'suspendida') DEFAULT 'activa',
    precio_pagado DECIMAL(10, 2) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (membresia_tipo_id) REFERENCES membresias_tipos(id)
);

-- TABLA: accesos
-- Registra las entradas y salidas de los usuarios al gimnasio
CREATE TABLE accesos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    gimnasio_id INT NOT NULL,
    fecha_hora_entrada DATETIME NOT NULL,
    fecha_hora_salida DATETIME,
    tipo_acceso ENUM('entrada', 'salida') NOT NULL,
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE
);

-- TABLA: entrenadores_clientes
-- Relación entre entrenadores y sus clientes asignados
CREATE TABLE entrenadores_clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entrenador_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_asignacion DATE NOT NULL,
    fecha_finalizacion DATE,
    activo BOOLEAN DEFAULT TRUE,
    notas TEXT,
    FOREIGN KEY (entrenador_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unico_entrenador_cliente (entrenador_id, cliente_id, activo)
);

-- TABLA: clases
-- Define las clases grupales disponibles
CREATE TABLE clases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    entrenador_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL, -- Yoga, Spinning, CrossFit, etc.
    descripcion TEXT,
    capacidad_maxima INT NOT NULL,
    duracion_minutos INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (entrenador_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: clases_horarios
-- Horarios específicos de cada clase
CREATE TABLE clases_horarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    clase_id INT NOT NULL,
    dia_semana ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (clase_id) REFERENCES clases(id) ON DELETE CASCADE
);

-- TABLA: reservas
-- Reservas de clientes para clases
CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    clase_horario_id INT NOT NULL,
    fecha_reserva DATE NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'asistio', 'no_asistio') DEFAULT 'confirmada',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_horario_id) REFERENCES clases_horarios(id) ON DELETE CASCADE,
    UNIQUE KEY reserva_unica (usuario_id, clase_horario_id, fecha_reserva)
);

-- TABLA: productos_categorias
-- Categorías de productos
CREATE TABLE productos_categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL, -- Suplementos, Merchandising, Bebidas, etc.
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE
);

-- TABLA: productos
-- Productos disponibles para venta
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    categoria_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 0,
    imagen_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES productos_categorias(id)
);

-- TABLA: facturas
-- Facturas generadas por ventas y membresías
CREATE TABLE facturas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    usuario_id INT NOT NULL,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    tipo ENUM('membresia', 'producto', 'mixta') NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    impuestos DECIMAL(10, 2) DEFAULT 0,
    descuentos DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'pagada', 'cancelada', 'anulada') DEFAULT 'pendiente',
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia', 'otro'),
    notas TEXT,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_pago DATETIME,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: facturas_detalle
-- Detalle de productos/servicios en cada factura
CREATE TABLE facturas_detalle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    factura_id INT NOT NULL,
    concepto VARCHAR(255) NOT NULL, -- Descripción del item
    tipo_item ENUM('membresia', 'producto') NOT NULL,
    item_id INT, -- ID de membresía o producto
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
);

-- TABLA: pagos
-- Registro de pagos realizados
CREATE TABLE pagos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    factura_id INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia', 'otro') NOT NULL,
    referencia VARCHAR(100), -- Número de referencia/transacción
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
);

-- TABLA: inventario_categorias
-- Categorías de equipamiento
CREATE TABLE inventario_categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL, -- Máquinas, Pesas, Accesorios, etc.
    descripcion TEXT,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE
);

-- TABLA: inventario
-- Control de equipamiento del gimnasio
CREATE TABLE inventario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    categoria_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    codigo VARCHAR(50), -- Código de inventario
    cantidad INT NOT NULL DEFAULT 1,
    estado ENUM('excelente', 'bueno', 'regular', 'malo', 'fuera_servicio') DEFAULT 'bueno',
    fecha_adquisicion DATE,
    costo DECIMAL(10, 2),
    ubicacion VARCHAR(200), -- Área del gimnasio
    fecha_ultimo_mantenimiento DATE,
    fecha_proximo_mantenimiento DATE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES inventario_categorias(id)
);

-- TABLA: rutinas
-- Rutinas de entrenamiento
CREATE TABLE rutinas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gimnasio_id INT NOT NULL,
    creador_id INT NOT NULL, -- ID del entrenador que creó la rutina
    cliente_id INT, -- NULL si es rutina general, o ID del cliente si es personalizada
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    objetivo VARCHAR(255), -- Pérdida de peso, ganancia muscular, etc.
    nivel ENUM('principiante', 'intermedio', 'avanzado') NOT NULL,
    tipo ENUM('general', 'personalizada') NOT NULL,
    duracion_semanas INT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE,
    FOREIGN KEY (creador_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: rutinas_ejercicios
-- Ejercicios que componen cada rutina
CREATE TABLE rutinas_ejercicios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rutina_id INT NOT NULL,
    dia_semana ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    orden INT NOT NULL, -- Orden del ejercicio en el día
    nombre_ejercicio VARCHAR(200) NOT NULL,
    descripcion TEXT,
    series INT NOT NULL,
    repeticiones VARCHAR(50), -- "12" o "12-15" o "al fallo"
    peso VARCHAR(50), -- "20kg" o "peso corporal"
    descanso_segundos INT,
    notas TEXT,
    video_url VARCHAR(500),
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id) ON DELETE CASCADE
);

-- TABLA: progreso_fisico
-- Registro de avances físicos de los clientes
CREATE TABLE progreso_fisico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha_registro DATE NOT NULL,
    peso DECIMAL(5, 2),
    altura DECIMAL(5, 2),
    imc DECIMAL(5, 2),
    porcentaje_grasa DECIMAL(5, 2),
    masa_muscular DECIMAL(5, 2),
    circunferencia_pecho DECIMAL(5, 2),
    circunferencia_cintura DECIMAL(5, 2),
    circunferencia_cadera DECIMAL(5, 2),
    circunferencia_brazo DECIMAL(5, 2),
    circunferencia_pierna DECIMAL(5, 2),
    foto_frontal_url VARCHAR(500),
    foto_lateral_url VARCHAR(500),
    foto_posterior_url VARCHAR(500),
    notas TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: dietas
-- Planes alimenticios asignados por entrenadores
CREATE TABLE dietas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entrenador_id INT NOT NULL,
    cliente_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    objetivo VARCHAR(255),
    calorias_totales INT,
    proteinas_gramos DECIMAL(6, 2),
    carbohidratos_gramos DECIMAL(6, 2),
    grasas_gramos DECIMAL(6, 2),
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entrenador_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: dietas_comidas
-- Comidas del plan alimenticio
CREATE TABLE dietas_comidas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dieta_id INT NOT NULL,
    tipo_comida ENUM('desayuno', 'colacion_am', 'almuerzo', 'colacion_pm', 'cena', 'colacion_noche') NOT NULL,
    hora_sugerida TIME,
    descripcion TEXT NOT NULL,
    calorias INT,
    proteinas_gramos DECIMAL(6, 2),
    carbohidratos_gramos DECIMAL(6, 2),
    grasas_gramos DECIMAL(6, 2),
    notas TEXT,
    FOREIGN KEY (dieta_id) REFERENCES dietas(id) ON DELETE CASCADE
);

-- TABLA: notificaciones
-- Sistema de notificaciones para usuarios
CREATE TABLE notificaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo ENUM('informacion', 'recordatorio', 'alerta', 'promocion') NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_lectura DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- TABLA: logs_actividad
-- Registro de actividades importantes en el sistema
CREATE TABLE logs_actividad (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    gimnasio_id INT NOT NULL,
    accion VARCHAR(255) NOT NULL,
    entidad VARCHAR(100), -- nombre de la tabla afectada
    entidad_id INT, -- ID del registro afectado
    descripcion TEXT,
    ip_address VARCHAR(45),
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (gimnasio_id) REFERENCES gimnasios(id) ON DELETE CASCADE
);

-- ============================================
-- ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS
-- ============================================

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_gimnasio ON usuarios(gimnasio_id);
CREATE INDEX idx_usuarios_rol ON usuarios(rol_id);
CREATE INDEX idx_membresias_usuario ON membresias(usuario_id);
CREATE INDEX idx_membresias_estado ON membresias(estado);
CREATE INDEX idx_accesos_usuario ON accesos(usuario_id);
CREATE INDEX idx_accesos_fecha ON accesos(fecha_hora_entrada);
CREATE INDEX idx_entrenadores_clientes_entrenador ON entrenadores_clientes(entrenador_id);
CREATE INDEX idx_entrenadores_clientes_cliente ON entrenadores_clientes(cliente_id);
CREATE INDEX idx_reservas_usuario ON reservas(usuario_id);
CREATE INDEX idx_reservas_fecha ON reservas(fecha_reserva);
CREATE INDEX idx_facturas_usuario ON facturas(usuario_id);
CREATE INDEX idx_facturas_gimnasio ON facturas(gimnasio_id);
CREATE INDEX idx_facturas_estado ON facturas(estado);
CREATE INDEX idx_productos_gimnasio ON productos(gimnasio_id);
CREATE INDEX idx_inventario_gimnasio ON inventario(gimnasio_id);
CREATE INDEX idx_rutinas_cliente ON rutinas(cliente_id);
CREATE INDEX idx_progreso_usuario ON progreso_fisico(usuario_id);
CREATE INDEX idx_progreso_fecha ON progreso_fisico(fecha_registro);
CREATE INDEX idx_dietas_cliente ON dietas(cliente_id);
CREATE INDEX idx_notificaciones_usuario ON notificaciones(usuario_id);
CREATE INDEX idx_logs_gimnasio ON logs_actividad(gimnasio_id);

-- ============================================
-- DATOS INICIALES - ROLES DEL SISTEMA
-- ============================================

INSERT INTO roles (nombre, descripcion, permisos) VALUES
('super_admin', 'Super Administrador del Gimnasio', '{"all": true}'),
('admin', 'Administrador', '{"usuarios": ["read", "create", "update"], "membresias": ["all"], "productos": ["all"], "inventario": ["all"], "reportes": ["read"]}'),
('entrenador', 'Entrenador Personal', '{"clientes": ["read", "update"], "rutinas": ["all"], "dietas": ["all"], "clases": ["all"], "progreso": ["read"]}'),
('cliente', 'Cliente del Gimnasio', '{"perfil": ["read", "update"], "reservas": ["all"], "progreso": ["all"], "rutinas": ["read"]}');

-- ============================================
-- FIN DEL SCRIPT
-- ============================================