•	Funcionalidades de administración: Usuario principal – Administrador
o	Gestión de estudiantes:
	RF-01 Registro de estudiantes: El sistema permitirá a los administradores registrar estudiantes en la plataforma. Esto generará un usuario con el que se pueda acceder a las funcionalidades de estudiante.
	RF-02 Registro masivo de estudiantes: El sistema permitirá a los administradores registrar múltiples estudiantes de forma simultánea subiendo al servidor un archivo de tipo CSV con los datos correspondientes. El sistema deberá comprobar que el archivo subido es válido antes de realizar las operaciones de registro.
	RF-03 Visualización general de estudiantes: El sistema permitirá a los administradores visualizar un listado de los estudiantes del centro. Este listado debe incluir filtros de búsqueda y ordenamiento para facilitar la localización de estudiantes concretos.
	RF-04 Visualización de detalles de un estudiante: El sistema permitirá a los administradores visualizar los detalles de un estudiante concreto. Esto debe incluir un listado de las asignaturas a las que está apuntado y una ficha con su información personal.
	RF-05 Desapuntar a estudiante de asignaturas: El sistema permitirá a los administradores desapuntar al estudiante de las asignaturas a las que está apuntado.
	RF-06 Apuntar a estudiante en asignaturas: El sistema permitirá a los administradores apuntar a un estudiante en una o más asignaturas en las que no estuviera apuntado.
	RF-07 Eliminación de estudiantes de la plataforma: El sistema permitirá a los administradores eliminar un estudiante de la plataforma. Esta acción deberá eliminar el usuario de acceso y toda la información del estudiante.
	RF-08 Modificación de datos personales del estudiante: El sistema permitirá a los administradores la actualización de los datos personales del estudiante.



o	Gestión de profesores:
	RF-09 Registro de profesores: El sistema permitirá a los administradores registrar profesores en la plataforma. Esto generará un usuario con el que se pueda acceder a las funcionalidades de profesor.
	RF-10 Visualización general de profesores: El sistema permitirá a los administradores visualizar un listado de los profesores del centro. Este listado debe incluir filtros de búsqueda y ordenamiento para facilitar la localización de profesores concretos.
	RF-11 Visualización de detalles de un profesor: El sistema permitirá a los administradores visualizar los detalles de un profesor concreto. Esto debe incluir un listado de las asignaturas que imparte y una ficha con su información personal.
	RF-12 Desapuntar a profesor de asignaturas: El sistema permitirá a los administradores desapuntar al profesor de las asignaturas a las que está apuntado. 
	RF-13 Apuntar a profesor en asignaturas: El sistema permitirá a los administradores apuntar a un profesor en una o más asignaturas en las que no estuviera apuntado.
	RF-14 Eliminación de profesores de la plataforma: El sistema permitirá a los administradores eliminar un profesor de la plataforma. Esta acción deberá eliminar el usuario de acceso y toda la información del profesor.
	RF-15 Modificación de datos personales del profesor: El sistema permitirá a los administradores la actualización de los datos personales del profesor.

o	Gestión de asignaturas:
	RF-16 Creación de asignaturas: El sistema permitirá a los administradores crear asignaturas. Las asignaturas podrán crearse sin ningún profesor o estudiante asignados.
	RF-17 Visualización general de asignaturas: El sistema permitirá a los administradores visualizar un listado de las asignaturas existentes en la plataforma. Este listado debe incluir filtros de búsqueda y ordenamiento para facilitar la localización de asignaturas concretas.
	RF-18 Visualización de detalles de una asignatura: El sistema permitirá a los administradores visualizar para una asignatura concreta aquellos profesores y estudiantes que están apuntados.
	RF-19 Añadir/eliminar profesores y estudiantes a una asignatura : El sistema permitirá añadir en una asignatura uno o varios profesores. También permitirá añadir uno o varios estudiantes. Solo dará la opción de apuntar a estudiantes/profesores que no estuvieran apuntados.
	RF-20 Editar información asignatura: El sistema permitirá a los administradores cambiar el nombre de una asignatura existente.
	RF-21 Eliminar asignatura de la plataforma: El sistema permitirá a los administradores eliminar una asignatura de la plataforma. Esta acción deberá eliminar todo el contenido de la asignatura y los estudiantes o profesores que estuvieran apuntados ya no podrán acceder a ella.

•	Funcionalidades del profesorado: Usuario principal – Profesor
o	Gestión de asignaturas:
	RF-22 Visualización de asignaturas: El sistema mostrará a los profesores un listado de las asignaturas que imparten.
o	Gestión de tareas:
	RF-23 Creación de tareas: El sistema permitirá a los profesores crear tareas para las asignaturas que imparten.
	RF-24 Edición de tareas: Los profesores podrán editar aquellas tareas que pertenezcan a las asignaturas que imparten.
	RF-25 Eliminación de tareas: Los profesores podrán eliminar de la plataforma las tareas de las asignaturas que imparten. Eliminar una tarea también eliminará las entregas que los estudiantes hicieron para esa tarea concreta.
o	Gestión de entregas:
	RF-26 Visualización de entregas: Los profesores podrán visualizar las entregas que los alumnos hacen de las tareas.
	RF-27 Corrección de entregas: Los profesores podrán corregir las tareas que los alumnos hacen. La corrección consiste en añadir una calificación y un comentario a la entrega. Las tareas que se entreguen tarde se podrán corregir pero se indicará que se entregó fuera del plazo.

•	Funcionalidades de los estudiantes: Usuario principal – estudiante
o	Gestión de asignaturas:
	RF-28 Visualización de asignaturas: El sistema mostrará a los estudiantes un listado de las asignaturas que cursan.
o	Gestión de entregas:
	RF-29 Envío de entregas: El sistema permitirá a los estudiantes entregar las tareas que tengan asignadas en sus asignaturas. Si las tareas se entregan después de la fecha límite el sistema lo detectará y quedará registrado.

•	Funcionalidades del aula: Usuario principal – Profesores y estudiantes
o	Foro de la asignatura
	RF-30 Visualización de mensajes del foro: Cada asignatura tendrá un foro público que podrán visualizar los profesores y estudiantes que estén asignados a ella.
	RF-31 Envío de mensajes al foro: Los estudiantes y profesores podrán publicar mensajes en el foro y responder los mensajes de otras personas.

o	Gestión de tareas:
	RF-32 Visualización de tareas: Los profesores y estudiantes podrán visualizar las tareas de la asignatura. Podrán filtrar las tareas para ver cuáles no han cumplido la fecha límite de entrega.	

•	Funcionalidades de autenticación y autorización: Usuario principal – Profesores, Estudiantes, Administradores, Usuario sin autenticar
o	Funcionalidades de autenticación:
	RF-33 Inicio de sesión: El sistema redirigirá a todos los usuarios sin autenticar a un formulario de inicio de sesión. Deberán introducir un nombre de usuario y una contraseña. El sistema comprobará estas credenciales y dará acceso o lo negará en función de su coincidencia con las credenciales de un usuario registrado en la plataforma.
	RF-34 Cierre de sesión: Los usuarios autenticados podrán cerrar sesión. Cuando vuelvan a acceder a la plataforma ya no estarán autenticados y tendrán que introducir de nuevo sus credenciales para acceder.

o	Funcionalidades de autorización:
	RF-35 Autorización basada en roles: Todos los usuarios de la plataforma tendrán un rol asignado. El sistema deberá restringir el acceso a las funcionalidades y sólo permitirlo a aquellos usuarios con el rol adecuado. Para preservar la seguridad del sistema, si por error hubiera usuarios sin rol asignado no podrán acceder a ninguna funcionalidad.
