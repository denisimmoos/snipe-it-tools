class SnipeItTools:

    def __init__(self, base_url, api_key):

        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"
        }
    #
    # COMPANY
    #
    def get_company(self, name):

        import requests
        import json

        url = self.base_url + "/api/v1/companies"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']

        return(id)

    def set_company(self, name):

        import requests
        import json

        url = self.base_url + "/api/v1/companies"
        payload = {"name": name}

        response = requests.request(
            "POST",
            url,
            json=payload,
            headers=self.headers
        )

        response = json.loads(response.text)

        if response['status'] == 'success':
            id = response['payload']['id']
        else:
            id = self.get_company(name)

        return(id)
    #
    # MANUFACTURER
    #
    def get_manufacturer(self, name):

        import requests
        import json

        url = self.base_url + "/api/v1/manufacturers"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def set_manufacturer(self, name):

        import requests
        import json

        url = self.base_url + "/api/v1/manufacturers"
        payload = {"name": name}

        response = requests.request(
            "POST",
            url,
            json=payload,
            headers=self.headers
        )

        response = json.loads(response.text)

        if response['status'] == 'success':
            id = response['payload']['id']
        else:
            id = self.get_manufacturer(name)

        return(id)

    #
    # DEPARTMENT
    #
    def get_department(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/departments"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def set_department(self, name):

        import requests
        import json

        url = self.base_url + "/api/v1/departments"

        id = self.get_department(name)

        if not id:
            payload = {"name": name}

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    #
    # CATEGORIES
    #
    def get_category(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/categories"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def set_category(
        self,
        name,
        category_type,
        use_default_eula=None,
        require_acceptance=None,
        checkin_email=None
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/categories"

        id = self.get_category(name)

        if not id:
            payload = {
                "name": name,
                "category_type": category_type
            }

            if use_default_eula:
                payload['use_default_eula'] = use_default_eula
            if require_acceptance:
                payload['require_acceptance'] = require_acceptance
            if checkin_email:
                payload['checkin_email'] = checkin_email

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    #
    # LOCATIONS
    #
    def get_location(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/locations"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def set_location(
        self,
        name,
        address=None,
        address2=None,
        state=None,
        country=None,
        zip=None,
        ldap_ou=None,
        parent_id=None,
        currency=None,
        manager_id=None
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/locations"

        id = self.get_location(name)

        if not id:
            payload = {"name": name}

            if address:
                payload['address'] = address
            if address2:
                payload['address2'] = address2
            if state:
                payload['state'] = state
            if country:
                payload['country'] = country
            if zip:
                payload['zip'] = zip
            if parent_id:
                payload['parent_id'] = parent_id
            if currency:
                payload['currency'] = currency
            if manager_id:
                payload['manager_id'] = manager_id

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    #
    # STATUSLABELS
    #
    def get_statuslabel(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/statuslabels"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def set_statuslabel(
        self,
        name,
        type,
        notes=None,
        color=None,
        show_in_nav=None,
        default_label=None,
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/statuslabels"

        id = self.get_statuslabel(name)

        if not id:
            payload = {
                "name": name,
                "type": type
            }

            if notes:
                payload['notes'] = notes
            if color:
                payload['color'] = color
            if show_in_nav:
                payload['show_in_nav'] = show_in_nav
            if default_label:
                payload['default_label'] = default_label

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    #
    # MODELS
    #
    def get_model(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/models"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def get_model_by_model_nummer(self, model_number):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/models"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['model_number'] == model_number:
                id = row['id']
        return(id)

    def set_model(
        self,
        name,
        category_id,
        manufacturer_id,
        model_number,
        eol=None,
        fieldset_id=None,
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/models"

        id = self.get_model(name)

        if not id:
            payload = {
                "name": name,
                "category_id": category_id,
                "manufacturer_id": manufacturer_id,
                "model_number": model_number,
            }

            if eol:
                payload['eol'] = eol
            if fieldset_id:
                payload['fieldset_id'] = fieldset_id

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    def update_model(
        self,
        model_id,
        name,
        category_id,
        manufacturer_id,
        model_number=None,
        eol=None,
        fieldset_id=None,
        depreciation_id=None,
        notes=None,
        requestable=None
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/models/" + str(model_id)

        payload = {
            "name": name,
            "category_id": category_id,
            "manufacturer_id": manufacturer_id,
        }

        if model_number:
            payload['model_number'] = model_number
        if eol:
            payload['eol'] = eol
        if fieldset_id:
            payload['fieldset_id'] = fieldset_id
        if depreciation_id:
            payload['depreciation_id'] = depreciation_id
        if notes:
            payload['notes'] = notes
        if requestable:
            payload['requestable'] = requestable

        response = requests.request(
            "PUT",
            url,
            json=payload,
            headers=self.headers
        )

        response = json.loads(response.text)
        id = response['payload']['id']

        return(id)


#
# ASSETS
#
    def get_hardware_by_serial(self, serial):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/hardware/byserial/" + serial

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['serial'] == serial:
                id = row['id']

        return(id)

    def set_hardware(
        self,
        name,
        company_id,
        manufacturer_id,
        serial,
        model_id,
        status_id,
        asset_tags=None,
        checkout_to_type=None,
        assigned_user=None,
        assigned_asset=None,
        assigned_location=None,
        purchase_date=None,
        purchase_cost=None,
        supplier_id=None,
        order_number=None,
        warranty_months=None,
        notes=None,
        rtd_location_id=None,
        image=None
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/hardware"

        id = self.get_hardware_by_serial(serial)

        if not id:
            payload = {
                "name": name,
                "company_id": company_id,
                "manufacturer_id": manufacturer_id,
                'serial': serial,
                "model_id": model_id,
                "status_id": status_id,
            }

            if checkout_to_type:
                payload['checkout_to_type'] = checkout_to_type
            if assigned_user:
                payload['assigned_user'] = assigned_user
            if assigned_asset:
                payload['assigned_asset'] = assigned_asset
            if assigned_location:
                payload['assigned_location'] = assigned_location
            if purchase_date:
                payload['purchase_date'] = purchase_date
            if purchase_cost:
                payload['purchase_cost'] = purchase_cost
            if supplier_id:
                payload['supplier_id'] = supplier_id
            if order_number:
                payload['order_number'] = order_number
            if warranty_months:
                payload['warranty_months'] = warranty_months
            if notes:
                payload['notes'] = notes
            if rtd_location_id:
                payload['rtd_location_id'] = rtd_location_id
            if image:
                payload['image']

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)


# XXXXXXXXX

    def update_hardware_fields(
        self,
        hardware_id,
        fields_dict
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/hardware/" + str(hardware_id)

        payload = fields_dict

        response = requests.request(
            "PUT",
            url,
            json=payload,
            headers=self.headers
        )

        response = json.loads(response.text)
        id = response['payload']['id']

        return(id)

    #
    # FIELDSETS
    #
    def get_fieldset(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/fieldsets"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']
        return(id)

    def get_fieldset_dict(self, fieldset_id):

        import requests
        import json

        dict_fieldset = {}
        url = self.base_url + "/api/v1/fieldsets/" + str(fieldset_id) + "fields"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['fields']['rows']:
            dict_fieldset[row['name']] = row['db_column_name']

        return(dict_fieldset)

    def set_fieldset(
        self,
        name,
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/fieldsets"

        id = self.get_fieldset(name)

        if not id:
            payload = {
                "name": name,
            }

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)

    #
    # FIELDS
    #
    def get_field(self, name):

        import requests
        import json

        id = False
        url = self.base_url + "/api/v1/fields"

        response = requests.request("GET", url, headers=self.headers)
        response = json.loads(response.text)

        for row in response['rows']:
            if row['name'] == name:
                id = row['id']

        return(id)

    def associate_field(self, field_id, fieldset_id):

        import requests
        import json

        url = self.base_url + "/api/v1/fields/" + str(field_id) + "/associate"

        payload = {
            "field_id": field_id,
            "fieldset_id": fieldset_id
        }

        response = requests.request(
            "POST",
            url,
            json=payload,
            headers=self.headers
        )
        response = json.loads(response.text)
        id = response['payload']['id']

        return(id)

    def set_field(
        self,
        name,
        element,
        field_values=None,
        show_in_email=None,
        format="ANY",
        field_encrypted=None,
        help_text=None
    ):

        import requests
        import json

        url = self.base_url + "/api/v1/fields"

        id = self.get_field(name)

        if not id:

            payload = {
                "name": name,
                "element": element,
            }

            if field_values:
                payload['field_values'] = field_values
            if show_in_email:
                payload['show_in_email'] = show_in_email
            if format:
                payload['format'] = format
            if field_encrypted:
                payload['field_encrypted'] = field_encrypted
            if help_text:
                payload['help_text'] = help_text

            response = requests.request(
                "POST",
                url,
                json=payload,
                headers=self.headers
            )

            response = json.loads(response.text)
            id = response['payload']['id']

        return(id)
