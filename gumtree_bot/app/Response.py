import json


class JSONResponse:

    SUCCESS_STATUS = 200
    ERROR_STATUS = 400

    status = 400
    message = ''
    form_errors = ''
    data = ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)

    def exception_response(self, exception):
        self.status = self.ERROR_STATUS
        self.data = None
        self.message = exception
        self.form_errors = ''
        return self

    def form_error_response(self, form):
        self.status = self.ERROR_STATUS
        self.data = None
        self.message = 'form validation failed'
        self.form_errors = form.errors.as_json()
        return self

    def form_invalid_response(self, message):
        self.status = self.ERROR_STATUS
        self.data = None
        self.message = message
        self.form_errors = None
        return self
