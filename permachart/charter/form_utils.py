from google.appengine.ext import db

class BaseFormSet(object):
    def __init__(self, data=None, instances=None, extra_forms=2):
        """
        Testing Concerns:
         - deleting an item
         - adding an item
         - altering the key
         - altering the value
        """
        self.forms = []
        instances = instances or []
        for i, obj in enumerate(instances):
            if isinstance(obj, db.Key):
                # fetch keys for validation
                # FIXME: Can probably do a bulk get
                obj = db.get(obj)
            form_kwargs = {'instance': obj,
                           'prefix': '%i' % i}
            if data:
                form_kwargs.update(dict(data=data))
            base_form = self.base_form(**form_kwargs)
            self.forms.append(base_form)

        offset = len(instances)
        for i in range(extra_forms):
            form_kwargs = dict(prefix="%i" % (offset+i))
            if data:
                form_kwargs.update({'data':data})
            base_form = self.base_form(**form_kwargs)
            base_form.empty_ok = True
            self.forms.append(base_form)
    
    def is_valid(self):
        """
        App engine doesn't support the empty_permitted flag to model
        forms, so we're going to dupe a bit of the validation logic
        here.
        
        This is coupled with checking for a 'cleaned_data' attribute
        on the form. If its not there, we'll assume its an empty form
        that we can skip (otherwise, it wouldn't have passed
        validation).
        """
        for i, sub_form in enumerate(self.forms):
            if not sub_form.is_valid():
                if not sub_form.has_changed() and \
                        hasattr(sub_form, 'empty_ok') and\
                        sub_form.empty_ok == True:
                    continue
                return False
        return True

