from .database import DatabaseConnection

class Tarea:
    def __init__(self, tarea_id=None, tarea_nombre=None, fecha_creacion=None, fecha_limite=None, completado=None, categoria_id=None):
        self.tarea_id=tarea_id
        self.tarea_nombre=tarea_nombre
        self.fecha_creacion=fecha_creacion
        self.fecha_limite=fecha_limite
        self.completado=completado
        self.categoria_id=categoria_id

    @classmethod
    def get_tarea(cls, tarea_id):
        query="SELECT t.nombre, t.fecha_creacion, t.fecha_limite, i.item_completado, c.categoria_nombre\
                FROM  to_do_app.tareas t\
                INNER JOIN to_do_app.categorias c on t.categoria_id = c.categoria_id\
                LEFT JOIN to_do_app.items i on t.tarea_id = i.tarea_id\
                WHERE tarea_id = %s"
        params=(tarea_id,)
        result=DatabaseConnection.fetch_one(query, params)
        if result is not None:
            return Tarea(
                tarea_id=tarea_id,
                tarea_nombre=result[0],
                fecha_creacion=result[1],
                fecha_limite=result[2],
                completado=result[3],
                categoria_id=result[4]
            )
        else:
            return None

    @classmethod
    def get_tareas(cls):
        query = "SELECT t.tarea_id, t.tarea_nombre, t.fecha_creacion, t.fecha_limite, t.completado, c.categoria_nombre\
            FROM to_do_app.tareas t\
            LEFT JOIN to_do_app.categorias c ON t.categoria_id = c.categoria_id"
        results = DatabaseConnection.fetch_all(query)

        tareas = []
        for result in results:
            tarea = Tarea(
                tarea_id=result[0],
                tarea_nombre=result[1],
                fecha_creacion=result[2],
                fecha_limite=result[3],
                completado=result[4],
                categoria_id=result[5]
            )
            tareas.append(tarea)

        return tareas


    @classmethod
    def create_tarea(cls,tarea):
        query="INSERT INTO to_do_app.tareas (tarea_nombre, fecha_creacion, fecha_limite, completado, categoria_id) VALUES (%s, NOW(), %s, %s, %s)"
        
        if tarea.tarea_nombre!='' and tarea.fecha_creacion!='' and tarea.fecha_limite!='' and tarea.completado!='' and tarea.categoria_id!='':
            params=(tarea.tarea_nombre, tarea.fecha_limite, tarea.completado, tarea.categoria_id)
            DatabaseConnection.execute_query(query, params)
            message='Tarea creada con exito'
        else:
            message=None
        return message

    @classmethod
    def update_tarea(cls, tarea_id, tarea):
        if cls.check_tarea(tarea_id):
            query = "UPDATE to_do_app.tareas SET"
            params = []

            if tarea.tarea_nombre:
                query += ' tarea_nombre=%s,'
                params.append(tarea.tarea_nombre)
            if tarea.fecha_limite:
                query += ' fecha_limite=%s,'
                params.append(tarea.fecha_limite)
            if tarea.completado is not None:
                query += ' completado=%s,'
                params.append(tarea.completado)
            if tarea.categoria_id:
                query += ' categoria_id=%s,'
                params.append(tarea.categoria_id)

            query = query.rstrip(',')
            query += ' WHERE tarea_id = %s'
            params.append(tarea_id)
            DatabaseConnection.execute_query(query, params)
            message='Tarea actualizada con exito'
        else:
            message=None
        return message

    @classmethod
    def check_tarea(cls, tarea_id):
        query = "SELECT COUNT(*) FROM to_do_app.tareas WHERE tarea_id = %s"
        params = (tarea_id,)
        result = DatabaseConnection.fetch_one(query, params)[0]
        return result > 0


    @classmethod
    def delete_tarea(cls, tarea_id):
        if cls.check_tarea(tarea_id):
            query = "DELETE FROM to_do_app.tareas WHERE tarea_id = %s"
            params = (tarea_id,)
            DatabaseConnection.execute_query(query, params)
            message='Tarea eliminada con exito'
        else:
            message=None
        return message