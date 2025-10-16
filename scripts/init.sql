-- Script de inicialización de base de datos
CREATE DATABASE IF NOT EXISTS employees_db;

USE employees_db;


-- Insertar algunos empleados de ejemplo
INSERT INTO employees (first_name, last_name, email, phone, position, department, salary, hire_date)
VALUES
 ('Juan', 'Pérez', 'juan.perez@company.com', '+51999999999', 'Developer', 'IT', 5000.00, '2024-01-15'),
 ('María', 'González', 'maria.gonzalez@company.com', '+51988888888', 'Designer', 'Marketing', 4500.00, '2024-02-20');