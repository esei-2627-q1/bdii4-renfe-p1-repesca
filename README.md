# BDII4 · RENFE · Repesca del Entregable 1 (EER y DDL)

Bases de Datos II · ESEI · Universidade de Vigo · Curso 2026/2027

**Entrega:** domingo **15/11/2026, 23:59** en Moovi (2 intentos).
**Estado:** versión definitiva. Script ejecutado en Oracle 26ai el 06/11/2026: **50 pruebas correctas, 0 fallidas**.

## Qué hay en el repositorio

| Carpeta | Contenido |
|---|---|
| `entrega/` | **Lo que se sube a Moovi**: `E1_REP_BDII4_RENFE.zip` y sus tres ficheros sueltos |
| `sql/` | Script final y salida real de su ejecución en Oracle |
| `memoria/` | Fuente LaTeX de la memoria (`main.tex`, diccionario, esquema relacional y figuras) |
| `cambios/` | Fuente LaTeX del documento de cambios (`cambios.tex`) |
| `diagrama/` | Diagrama EER (PDF vectorial y PNG) y su fuente (`eer.dot`, `generar_eer.py`) |
| `docs/` | Enunciado de la práctica |
| `scripts/` | `empaquetar_entrega.sh`: recompila los PDF y vuelve a montar el ZIP |

## ZIP de entrega

`E1_REP_BDII4_RENFE.zip`, con estos tres ficheros en la raíz, sin carpetas:

- `E1_REP_BDII4_RENFE_MEM.pdf`: memoria corregida
- `E1_REP_BDII4_RENFE_SQL.sql`: script corregido
- `E1_REP_BDII4_RENFE_CAM.pdf`: documento de cambios

Ojo: `BDII4` va sin guion bajo entre BDII y 4.

## Cómo modificar algo

1. **Regla obligatoria:** cualquier cambio del modelo se aplica **a la vez** en la memoria (reglas, justificación, relacional y diccionario), el diagrama, el SQL y el documento de cambios.
2. **SQL:** si se toca el script, hay que volver a ejecutarlo completo en Oracle 26ai y sustituir la salida en `sql/salida_oracle_*.txt` y en el Apéndice A de la memoria.
3. **Memoria y cambios:** se pueden compilar en Overleaf (New Project → Upload Project, con el contenido de `memoria/` o de `cambios/`; compilador pdfLaTeX) o en local con `latexmk -pdf`.
4. **Diagrama:** `cd diagrama && python3 generar_eer.py && neato -n2 -Tpdf eer.dot -o EER_BDII4_RENFE.pdf`. Después, copiadlo a `memoria/figuras/eer.pdf`.
5. **Regenerar la entrega:** `./scripts/empaquetar_entrega.sh`.

## Antes de entregar

- [ ] Los cuatro hemos leído la memoria entera
- [ ] PDF de `entrega/` actualizados con la última versión (misma fecha en memoria y cambios)
- [ ] ZIP abierto y comprobado: tres ficheros con los nombres exactos y los PDF se abren bien
- [ ] Confirmado con Rubén si sube el ZIP uno o todos (si no, lo subimos todos)
- [ ] Subido a Moovi

## Repaso para la defensa

- Por qué Billete es una especialización (d, total) y no una categorización
- Tren_Mixto como subclase compartida y la generalización solapada y total de Tren
- Agregación Viaje: qué relaciones salen de ella y por qué la fecha de salida forma parte de la clave
- INSTALA (ternaria): por qué no se descompone y por qué la fecha de instalación es multivaluada
- Reflexivas: ACOPLA (precede/sigue, 1:1) y SUPERVISA (supervisor/supervisado, 1:N)
- DIRIGE (1:1) y por qué los jefes de estación no tienen rol operativo
- ORIGEN y DESTINO de Ruta, y cómo la FK compuesta obliga a llegar a un andén de la estación destino
- REVISA con Viaje (0,N): los viajes de mercancías no tienen revisor
- Discriminante de Empleado y de Billete (disyunción) y UNIQUE del vagón siguiente
- Qué restricciones no garantiza el DDL y cómo se comprueban
- Vista no actualizable (GROUP BY) frente a vista actualizable (una tabla + ROLLBACK)

## Integrantes

Alejandro Francisco Pérez Rodríguez · Mario Pérez González · Jacobo Montero Naranjo · Pablo Regueira Castaño
