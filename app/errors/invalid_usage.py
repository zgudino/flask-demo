class InvalidUsage(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    @staticmethod
    def to_dict(self):
        ret = dict(self.payload or ())
        ret['message'] = self.message

        return ret
