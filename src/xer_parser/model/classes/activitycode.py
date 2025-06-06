import locale
from typing import ClassVar

from xer_parser.model.acttypes import ActTypes


class ActivityCode:
    obj_list: ClassVar[list] = []

    def __init__(self, params):
        # Unique ID generated by the system.
        self.actv_code_id = (
            int(params.get("actv_code_id").strip())
            if params.get("actv_code_id")
            else None
        )
        # The parent Activity Code value in the user code value hierarchy.
        self.parent_actv_code_id = (
            int(params.get("parent_actv_code_id"))
            if params.get("parent_actv_code_id")
            else None
        )
        # The Activity Code type id acts as foreign key to activity code types table
        self.actv_code_type_id = (
            int(params.get("actv_code_type_id").strip())
            if params.get("actv_code_type_id")
            else None
        )
        # The description of an Activity Code value.
        self.actv_code_name = (
            params.get("actv_code_name").strip()
            if params.get("actv_code_name")
            else None
        )
        # The value of the activity code.
        self.short_name = (
            params.get("short_name").strip() if params.get("short_name") else None
        )
        # Sequence number for sorting.
        self.seq_num = (
            int(params.get("seq_num").strip()) if params.get("seq_num") else None
        )
        self.color = params.get("color").strip() if params.get("color") else None
        self.total_assignments = (
            int(locale.atof(params.get("total_assignments").strip()))
            if params.get("total_assignments")
            else None
        )
        ActivityCode.obj_list.append(self)

    def get_id(self):
        return self.actv_code_id

    def get_tsv(self):
        return [
            "%R",
            self.actv_code_id,
            self.parent_actv_code_id,
            self.actv_code_type_id,
            self.actv_code_name,
            self.short_name,
            self.seq_num,
            self.color,
            self.total_assignments,
        ]

    # @staticmethod
    # def find_by_id(id):
    #     obj = list(filter(lambda x: x.actv_code_id == id, ActivityCode.obj_list))
    #     if obj:
    #         return obj[0]
    #     return obj

    # @classmethod
    # def find_by_code(cls, code):
    #     """ This Function searches for activity code using ID code
    #
    #     Args:
    #         code: ID code as defined in Primavera and not the database
    #         obj_list: list of activity codes that need to be searched
    #
    #     Returns: an ActivityCode object that matches the supplied code
    #
    #     """
    #     actv_code = list(filter(lambda x: x.short_name == code, ActivityCode.obj_list))[0]
    #     return actv_code
    #
    # @classmethod
    # def get_parent(cls, id):
    #     obj = None
    #     c_actv_code = list(filter(lambda x: x.actv_code_id == id, ActivityCode.obj_list))[0]
    #     if c_actv_code:
    #         obj = cls.find_by_id(c_actv_code.actv_code_id, ActivityCode.obj_list)
    #     return obj
    #
    # @classmethod
    # def get_children(cls, id, obj_list):
    #     childs = list(filter(lambda x: x.parent_actv_code_id == id, obj_list))
    #     return childs

    @property
    def type(self):
        return ActTypes.find_by_id(self.actv_code_type_id)

    def __repr__(self):
        return (
            str(self.actv_code_id) + " - " + self.short_name
            if self.short_name
            else "" + " - " + self.actv_code_name
            if self.actv_code_name
            else ""
        )
