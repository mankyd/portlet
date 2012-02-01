import uuid

class BasePortlet(object):
    def __init__(self, template):
        self.tpl_vars = {}
        self.template = template

    def execute(self):
        return True
  
    def __call__(self, render_func):
        if not self.execute():
            return ''

        return self._execution_complete(render_func)

    def _execution_complete(self, render_func):
        return render_func(self.template, self.tpl_vars)

class Portlet(BasePortlet):
    PREFIX_CSS_CLASS = 'portlet'
    """Base Class for generating chunks of HTML content"""
    def __init__(self, template, css_class=None, get_args=None, post_args=None):
        css_class = css_class or []
        if isinstance(css_class, basestring):
            css_class = [css_class.split(' ')]

        self.get_args = get_args or {}
        self.post_args = post_args or {}
        self.css_class = set(css_class)
        self._id = self.html_id()

        BasePortlet.__init__(self, template)

    def _execution_complete(self, render_func):
        content = BasePortlet._execution_complete(self, render_func)

        css_class = self.PREFIX_CSS_CLASS
        if self.css_class:
            css_class = '{} {}' % (css_class, ' '.join(self.css_class))

        return '<div class="{}" id="{}">{}</div>'.format(css_class, self._id, content)
  
    def forms(self):
        for form in self._forms():
            result = form.process_strings(self.get_args, self.post_args)
            if result != None:
                return result

        return False

    def _forms(self):
        """
        Override this. Return a list of forms that should be run.
        """
        return []

    @classmethod
    def html_id(cls, prefix='portlet_'):
        return '{}{}'.format(prefix, uuid.uuid4().hex)

class AsyncPortlet(Portlet):
    def __call__(self, render_func, callback):
        def execute_cb(result):
            if result:
                callback(self._execution_complete(render_func))
            else:
                callback('')

        self.execute(execute_cb)

    def forms(self, callback):
        forms = self.forms()
        if len(forms) == 0:
            callback(None)
            return

        for form in forms:
            if isinstance(form, AsyncForm):
                form.process_strings(self.get_args, self.post_args, callback)
            else:
                callback(form.process_strings(self.get_args, self.post_args))

class AsyncForm(object): pass
