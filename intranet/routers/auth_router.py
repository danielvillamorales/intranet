class AuthRouter:
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'logistica_db':
            return 'logistica_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'logistica_db':
            return 'logistica_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return app_label == 'logistica_db'
    
#    def allow_relation(self, obj1, obj2, **hints):
#        if obj1._meta.app_label == 'logistica_db' or obj2._meta.app_label == 'logistica_db':
#            return True
#        return None
#    
#    def allow_migrate(self, db, app_label, model_name=None, **hints):
#        if app_label == 'logistica_db':
#            return db == 'logistica_db'
#        return None