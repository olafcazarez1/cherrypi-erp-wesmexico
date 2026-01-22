from .base import Model


class Employee(Model):
    """Database table name"""

    _TABLE = "employees"

    """Database primary keys
    """
    _IDS = ["employee_id"]

    """Database binary fields
    """
    _BINARY = []

    """Database binary fields
    """
    _UNIQUE = []

    """Required files for INSERT statement
    """
    _REQUIRED = [
        "company_id",
        "branch_id",
        "employee_id",
        "code",
        "internal_code",
        "names",
        "first_last_name",
        "second_last_name",
        "birthday",
        "gender",
        "taxpayer_id",
        "federal_id",
        "department_id",
        "work_position_id",
        "work_area_id",
        "email",
        "phone",
        "cell_phone",
        "address_street",
        "address_external_number",
        "address_internal_number",
        "neighborhood",
        "state_id",
        "municipality_id",
        "locality_id",
        "zip",
        "blood_type",
        "education_level",
        "marital_status",
        "has_license",
        "has_medical_insurance",
        "has_infonavit_credit",
        "has_fonacot_credit",
        "has_alergies",
        "has_medical_conditions",
        "status",
    ]

    _ALIAS = {"full_name": 'CONCAT(`names`, " ", `first_last_name`, " ", `second_last_name`)'}

    """Fields should not been overrided for set_attrs method
    """
    _RESTRICTED = ["created_at", "updated_at"]

    """While the global search index is available on this fields the global
    search is going to work for q parameter in filter method
    """
    _SEARCH_INDEX = []

    """Filter limit default (Used in filters())
    """
    _FILTER_LIMIT_DEFAULT = 50

    """Maximum limit value allowed (Used in filters())
    """
    _FILTER_LIMIT_MAX = 500

    """SQL funtion to generate a virtual project id
    """
    _SQL_GENERATE_ID = "SELECT UUID() as `id`;"

    @property
    def company_id(self):
        """Getter company_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> company_id = self.company_id
        """
        try:
            return self.__company_id
        except AttributeError:
            return None

    @company_id.setter
    def company_id(self, company_id):
        """Setter company_id

        Args:
            company_id(string): id.

        Returns:

        Usage:
            >>> self.company_id = company_id
        """
        self.__company_id = company_id

    @property
    def branch_id(self):
        """Getter branch_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> branch_id = self.branch_id
        """
        try:
            return self.__branch_id
        except AttributeError:
            return None

    @branch_id.setter
    def branch_id(self, branch_id):
        """Setter branch_id

        Args:
            branch_id(string): id.

        Returns:

        Usage:
            >>> self.branch_id = branch_id
        """
        self.__branch_id = branch_id

    @property
    def employee_id(self):
        """Getter employee_id

        Args:

        Returns:
            string: id value

        Usage:
            >>> employee_id = self.employee_id
        """
        try:
            return self.__employee_id
        except AttributeError:
            return None

    @employee_id.setter
    def employee_id(self, employee_id):
        """Setter employee_id

        Args:
            employee_id(string): id.

        Returns:

        Usage:
            >>> self.employee_id = employee_id
        """
        self.__employee_id = employee_id

    @property
    def code(self):
        """Getter code

        Args:

        Returns:
            string: code value

        Usage:
            >>> code = self.code
        """
        try:
            return self.__code
        except AttributeError:
            return None

    @code.setter
    def code(self, code):
        """Setter code

        Args:
            code(string): code.

        Returns:

        Usage:
            >>> self.code = code
        """
        self.__code = code

    @property
    def internal_code(self):
        """Getter internal_code

        Args:

        Returns:
            string: internal_code value

        Usage:
            >>> internal_code = self.internal_code
        """
        try:
            return self.__internal_code
        except AttributeError:
            return None

    @internal_code.setter
    def internal_code(self, internal_code):
        """Setter internal_code

        Args:
            internal_code(string): internal_code.

        Returns:

        Usage:
            >>> self.internal_code = internal_code
        """
        self.__internal_code = internal_code

    @property
    def names(self):
        """Getter names

        Args:

        Returns:
            string: names value

        Usage:
            >>> names = self.names
        """
        try:
            return self.__names
        except AttributeError:
            return None

    @names.setter
    def names(self, names):
        """Setter names

        Args:
            names(string): names.

        Returns:

        Usage:
            >>> self.names = names
        """
        self.__names = names

    @property
    def first_last_name(self):
        """Getter first_last_name

        Args:

        Returns:
            string: first_last_name value

        Usage:
            >>> first_last_name = self.first_last_name
        """
        try:
            return self.__first_last_name
        except AttributeError:
            return None

    @first_last_name.setter
    def first_last_name(self, first_last_name):
        """Setter first_last_name

        Args:
            first_last_name(string): first_last_name.

        Returns:

        Usage:
            >>> self.first_last_name = first_last_name
        """
        self.__first_last_name = first_last_name

    @property
    def second_last_name(self):
        """Getter second_last_name

        Args:

        Returns:
            string: second_last_name value

        Usage:
            >>> second_last_name = self.second_last_name
        """
        try:
            return self.__second_last_name
        except AttributeError:
            return None

    @second_last_name.setter
    def second_last_name(self, second_last_name):
        """Setter second_last_name

        Args:
            second_last_name(string): second_last_name.

        Returns:

        Usage:
            >>> self.second_last_name = second_last_name
        """
        self.__second_last_name = second_last_name

    @property
    def full_name(self):
        """Getter full_name

        Args:

        Returns:
            string: full_name value

        Usage:
            >>> full_name = self.full_name
        """
        try:
            return self.__full_name
        except AttributeError:
            return None

    @full_name.setter
    def full_name(self, full_name):
        """Setter full_name

        Args:
            full_name(string): full_name.

        Returns:

        Usage:
            >>> self.full_name = full_name
        """
        self.__full_name = full_name

    @property
    def birthday(self):
        """Getter birthday

        Args:

        Returns:
            string: birthday value

        Usage:
            >>> birthday = self.birthday
        """
        try:
            return self.__birthday
        except AttributeError:
            return None

    @birthday.setter
    def birthday(self, birthday):
        """Setter birthday

        Args:
            birthday(string): birthday.

        Returns:

        Usage:
            >>> self.birthday = birthday
        """
        self.__birthday = birthday

    @property
    def gender(self):
        """Getter gender

        Args:

        Returns:
            string: gender value

        Usage:
            >>> gender = self.gender
        """
        try:
            return self.__gender
        except AttributeError:
            return None

    @gender.setter
    def gender(self, gender):
        """Setter gender

        Args:
            gender(string): gender.

        Returns:

        Usage:
            >>> self.gender = gender
        """
        self.__gender = gender

    @property
    def taxpayer_id(self):
        """Getter taxpayer_id

        Args:

        Returns:
            string: taxpayer_id value

        Usage:
            >>> taxpayer_id = self.taxpayer_id
        """
        try:
            return self.__taxpayer_id
        except AttributeError:
            return ""

    @taxpayer_id.setter
    def taxpayer_id(self, taxpayer_id):
        """Setter taxpayer_id

        Args:
            taxpayer_id(string): taxpayer_id.

        Returns:

        Usage:
            >>> self.taxpayer_id = taxpayer_id
        """
        self.__taxpayer_id = taxpayer_id

    @property
    def federal_id(self):
        """Getter federal_id

        Args:

        Returns:
            string: federal_id value

        Usage:
            >>> federal_id = self.federal_id
        """
        try:
            return self.__federal_id
        except AttributeError:
            return ""

    @federal_id.setter
    def federal_id(self, federal_id):
        """Setter federal_id

        Args:
            federal_id(string): federal_id.

        Returns:

        Usage:
            >>> self.federal_id = federal_id
        """
        self.__federal_id = federal_id

    @property
    def department_id(self):
        """Getter department_id

        Args:

        Returns:
            string: department_id value

        Usage:
            >>> department_id = self.department_id
        """
        try:
            return self.__department_id
        except AttributeError:
            return None

    @department_id.setter
    def department_id(self, department_id):
        """Setter department_id

        Args:
            department_id(string): department_id.

        Returns:

        Usage:
            >>> self.department_id = department_id
        """
        self.__department_id = department_id

    @property
    def work_position_id(self):
        """Getter work_position_id

        Args:

        Returns:
            string: work_position_id value

        Usage:
            >>> work_position_id = self.work_position_id
        """
        try:
            return self.__work_position_id
        except AttributeError:
            return None

    @work_position_id.setter
    def work_position_id(self, work_position_id):
        """Setter work_position_id

        Args:
            work_position_id(string): work_position_id.

        Returns:

        Usage:
            >>> self.work_position_id = work_position_id
        """
        self.__work_position_id = work_position_id

    @property
    def work_area_id(self):
        """Getter work_area_id

        Args:

        Returns:
            string: work_area_id value

        Usage:
            >>> work_area_id = self.work_area_id
        """
        try:
            return self.__work_area_id
        except AttributeError:
            return None

    @work_area_id.setter
    def work_area_id(self, work_area_id):
        """Setter work_area_id

        Args:
            work_area_id(string): work_area_id.

        Returns:

        Usage:
            >>> self.work_area_id = work_area_id
        """
        self.__work_area_id = work_area_id

    @property
    def email(self):
        """Getter email

        Args:

        Returns:
            string: email value

        Usage:
            >>> email = self.email
        """
        try:
            return self.__email
        except AttributeError:
            return ""

    @email.setter
    def email(self, email):
        """Setter email

        Args:
            email(string): email.

        Returns:

        Usage:
            >>> self.email = email
        """
        self.__email = email

    @property
    def phone(self):
        """Getter phone

        Args:

        Returns:
            string: phone value

        Usage:
            >>> phone = self.phone
        """
        try:
            return self.__phone
        except AttributeError:
            return ""

    @phone.setter
    def phone(self, phone):
        """Setter phone

        Args:
            phone(string): phone.

        Returns:

        Usage:
            >>> self.phone = phone
        """
        self.__phone = phone

    @property
    def cell_phone(self):
        """Getter cell_phone

        Args:

        Returns:
            string: cell_phone value

        Usage:
            >>> cell_phone = self.cell_phone
        """
        try:
            return self.__cell_phone
        except AttributeError:
            return ""

    @cell_phone.setter
    def cell_phone(self, cell_phone):
        """Setter cell_phone

        Args:
            cell_phone(string): cell_phone.

        Returns:

        Usage:
            >>> self.cell_phone = cell_phone
        """
        self.__cell_phone = cell_phone

    @property
    def address_street(self):
        """Getter address_street

        Args:

        Returns:
            string: address_street value

        Usage:
            >>> address_street = self.address_street
        """
        try:
            return self.__address_street
        except AttributeError:
            return None

    @address_street.setter
    def address_street(self, address_street):
        """Setter address_street

        Args:
            address_street(string): address_street.

        Returns:

        Usage:
            >>> self.address_street = address_street
        """
        self.__address_street = address_street

    @property
    def address_external_number(self):
        """Getter address_external_number

        Args:

        Returns:
            string: address_external_number value

        Usage:
            >>> address_external_number = self.address_external_number
        """
        try:
            return self.__address_external_number
        except AttributeError:
            return ""

    @address_external_number.setter
    def address_external_number(self, address_external_number):
        """Setter address_external_number

        Args:
            address_external_number(string): address_external_number.

        Returns:

        Usage:
            >>> self.address_external_number = address_external_number
        """
        self.__address_external_number = address_external_number

    @property
    def address_internal_number(self):
        """Getter address_internal_number

        Args:

        Returns:
            string: address_internal_number value

        Usage:
            >>> address_internal_number = self.address_internal_number
        """
        try:
            return self.__address_internal_number
        except AttributeError:
            return ""

    @address_internal_number.setter
    def address_internal_number(self, address_internal_number):
        """Setter address_internal_number

        Args:
            address_internal_number(string): address_internal_number.

        Returns:

        Usage:
            >>> self.address_internal_number = address_internal_number
        """
        self.__address_internal_number = address_internal_number

    @property
    def neighborhood(self):
        """Getter neighborhood

        Args:

        Returns:
            string: neighborhood value

        Usage:
            >>> neighborhood = self.neighborhood
        """
        try:
            return self.__neighborhood
        except AttributeError:
            return ""

    @neighborhood.setter
    def neighborhood(self, neighborhood):
        """Setter neighborhood

        Args:
            neighborhood(string): neighborhood.

        Returns:

        Usage:
            >>> self.neighborhood = neighborhood
        """
        self.__neighborhood = neighborhood

    @property
    def state_id(self):
        """Getter state_id

        Args:

        Returns:
            string: state id value

        Usage:
            >>> state_id = self.state_id
        """
        try:
            return self.__state_id
        except AttributeError:
            return None

    @state_id.setter
    def state_id(self, state_id):
        """Setter state_id

        Args:
            state_id(string): state id.

        Returns:

        Usage:
            >>> self.state_id = state_id
        """
        self.__state_id = state_id

    @property
    def municipality_id(self):
        """Getter municipality_id

        Args:

        Returns:
            string: municipality id value

        Usage:
            >>> municipality_id = self.municipality_id
        """
        try:
            return self.__municipality_id
        except AttributeError:
            return None

    @municipality_id.setter
    def municipality_id(self, municipality_id):
        """Setter municipality_id

        Args:
            municipality_id(string): municipality id.

        Returns:

        Usage:
            >>> self.municipality_id = municipality_id
        """
        self.__municipality_id = municipality_id

    @property
    def locality_id(self):
        """Getter locality_id

        Args:

        Returns:
            string: locality id value

        Usage:
            >>> locality_id = self.locality_id
        """
        try:
            return self.__locality_id
        except AttributeError:
            return None

    @locality_id.setter
    def locality_id(self, locality_id):
        """Setter locality_id

        Args:
            locality_id(string): locality id.

        Returns:

        Usage:
            >>> self.locality_id = locality_id
        """
        self.__locality_id = locality_id

    @property
    def zip(self):
        """Getter zip

        Args:

        Returns:
            string: zip value

        Usage:
            >>> zip = self.zip
        """
        try:
            return self.__zip
        except AttributeError:
            return 0

    @zip.setter
    def zip(self, zip):
        """Setter zip

        Args:
            zip(string): zip.

        Returns:

        Usage:
            >>> self.zip = zip
        """
        self.__zip = zip

    @property
    def blood_type(self):
        """Getter Social Security Number

        Args:

        Returns:
            string: Social Security Number value

        Usage:
            >>> blood_type = self.blood_type
        """
        try:
            return self.__blood_type
        except AttributeError:
            return ""

    @blood_type.setter
    def blood_type(self, blood_type):
        """Setter Social Security Number

        Args:
            blood_type(string): Social Security Number.

        Returns:

        Usage:
            >>> self.blood_type = blood_type
        """
        self.__blood_type = blood_type

    @property
    def education_level(self):
        """Getter Social Security Number

        Args:

        Returns:
            string: Social Security Number value

        Usage:
            >>> education_level = self.education_level
        """
        try:
            return self.__education_level
        except AttributeError:
            return ""

    @education_level.setter
    def education_level(self, education_level):
        """Setter Social Security Number

        Args:
            education_level(string): Social Security Number.

        Returns:

        Usage:
            >>> self.education_level = education_level
        """
        self.__education_level = education_level

    @property
    def marital_status(self):
        """Getter Social Security Number

        Args:

        Returns:
            string: Social Security Number value

        Usage:
            >>> marital_status = self.marital_status
        """
        try:
            return self.__marital_status
        except AttributeError:
            return ""

    @marital_status.setter
    def marital_status(self, marital_status):
        """Setter Social Security Number

        Args:
            marital_status(string): Social Security Number.

        Returns:

        Usage:
            >>> self.marital_status = marital_status
        """
        self.__marital_status = marital_status

    @property
    def has_license(self):
        """Getter has_license

        Args:

        Returns:
            bool: has_license value

        Usage:
            >>> has_license = self.has_license
        """
        try:
            return self.__has_license
        except AttributeError:
            return 0

    @has_license.setter
    def has_license(self, has_license):
        """Setter has_license

        Args:
            has_license(bool): has_license.

        Returns:

        Usage:
            >>> self.has_license = has_license
        """
        self.__has_license = has_license

    @property
    def has_medical_insurance(self):
        """Getter has_medical_insurance

        Args:

        Returns:
            bool: has_medical_insurance value

        Usage:
            >>> has_medical_insurance = self.has_medical_insurance
        """
        try:
            return self.__has_medical_insurance
        except AttributeError:
            return 0

    @has_medical_insurance.setter
    def has_medical_insurance(self, has_medical_insurance):
        """Setter has_medical_insurance

        Args:
            has_medical_insurance(bool): has_medical_insurance.

        Returns:

        Usage:
            >>> self.has_medical_insurance = has_medical_insurance
        """
        self.__has_medical_insurance = has_medical_insurance

    @property
    def has_infonavit_credit(self):
        """Getter has_infonavit_credit

        Args:

        Returns:
            bool: has_infonavit_credit value

        Usage:
            >>> has_infonavit_credit = self.has_infonavit_credit
        """
        try:
            return self.__has_infonavit_credit
        except AttributeError:
            return 0

    @has_infonavit_credit.setter
    def has_infonavit_credit(self, has_infonavit_credit):
        """Setter has_infonavit_credit

        Args:
            has_infonavit_credit(bool): has_infonavit_credit.

        Returns:

        Usage:
            >>> self.has_infonavit_credit = has_infonavit_credit
        """
        self.__has_infonavit_credit = has_infonavit_credit

    @property
    def has_fonacot_credit(self):
        """Getter has_fonacot_credit

        Args:

        Returns:
            bool: has_fonacot_credit value

        Usage:
            >>> has_fonacot_credit = self.has_fonacot_credit
        """
        try:
            return self.__has_fonacot_credit
        except AttributeError:
            return 0

    @has_fonacot_credit.setter
    def has_fonacot_credit(self, has_fonacot_credit):
        """Setter has_fonacot_credit

        Args:
            has_fonacot_credit(bool): has_fonacot_credit.

        Returns:

        Usage:
            >>> self.has_fonacot_credit = has_fonacot_credit
        """
        self.__has_fonacot_credit = has_fonacot_credit

    @property
    def has_alergies(self):
        """Getter has_alergies

        Args:

        Returns:
            bool: has_alergies value

        Usage:
            >>> has_alergies = self.has_alergies
        """
        try:
            return self.__has_alergies
        except AttributeError:
            return 0

    @has_alergies.setter
    def has_alergies(self, has_alergies):
        """Setter has_alergies

        Args:
            has_alergies(bool): has_alergies.

        Returns:

        Usage:
            >>> self.has_alergies = has_alergies
        """
        self.__has_alergies = has_alergies

    @property
    def alergies(self):
        """Getter alergies

        Args:

        Returns:
            bool: alergies value

        Usage:
            >>> alergies = self.alergies
        """
        try:
            return self.__alergies
        except AttributeError:
            return ""

    @alergies.setter
    def alergies(self, alergies):
        """Setter alergies

        Args:
            alergies(bool): alergies.

        Returns:

        Usage:
            >>> self.alergies = alergies
        """
        self.__alergies = alergies

    @property
    def has_medical_conditions(self):
        """Getter has_medical_conditions

        Args:

        Returns:
            bool: has_medical_conditions value

        Usage:
            >>> has_medical_conditions = self.has_medical_conditions
        """
        try:
            return self.__has_medical_conditions
        except AttributeError:
            return 0

    @has_medical_conditions.setter
    def has_medical_conditions(self, has_medical_conditions):
        """Setter has_medical_conditions

        Args:
            has_medical_conditions(bool): has_medical_conditions.

        Returns:

        Usage:
            >>> self.has_medical_conditions = has_medical_conditions
        """
        self.__has_medical_conditions = has_medical_conditions

    @property
    def medical_conditions(self):
        """Getter medical_conditions

        Args:

        Returns:
            bool: medical_conditions value

        Usage:
            >>> medical_conditions = self.medical_conditions
        """
        try:
            return self.__medical_conditions
        except AttributeError:
            return ""

    @medical_conditions.setter
    def medical_conditions(self, medical_conditions):
        """Setter medical_conditions

        Args:
            medical_conditions(bool): medical_conditions.

        Returns:

        Usage:
            >>> self.medical_conditions = medical_conditions
        """
        self.__medical_conditions = medical_conditions

    @property
    def status(self):
        """Getter status

        Args:

        Returns:
            string: status value

        Usage:
            >>> status = self.status
        """
        try:
            return self.__status
        except AttributeError:
            return "active"

    @status.setter
    def status(self, status):
        """Setter status

        Args:
            status(string): status.

        Returns:

        Usage:
            >>> self.status = status
        """
        self.__status = status

    @property
    def created_at(self):
        """Getter created_at

        Args:

        Returns:
            string: created_at value

        Usage:
            >>> created_at = self.created_at
        """
        try:
            return self.__created_at
        except AttributeError:
            return None

    @created_at.setter
    def created_at(self, created_at):
        """Setter created_at

        Args:
            created_at(string): created_at.

        Returns:

        Usage:
            >>> self.created_at = created_at
        """
        self.__created_at = created_at

    @property
    def updated_at(self):
        """Getter updated_at

        Args:

        Returns:
            string: updated_at value

        Usage:
            >>> updated_at = self.updated_at
        """
        try:
            return self.__updated_at
        except AttributeError:
            return None

    @updated_at.setter
    def updated_at(self, updated_at):
        """Setter updated_at

        Args:
            updated_at(string): updated_at.

        Returns:

        Usage:
            >>> self.updated_at = updated_at
        """
        self.__updated_at = updated_at

    def get_attrs(self):
        """Get the list of properties that belongs to this class

        Returns:
            list: List of attributes in the Model
        """
        return super().get_attrs(Employee)

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __repr__(self):
        """Built-in function used to return the object representation

        Args:
            None

        Returns:
            str: A string with the object representation
        """
        return f"Employee('{self.employee_id}')"
