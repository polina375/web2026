from dataclasses import dataclass


@dataclass
class Student:
    isuId: int
    fullName: str
    group: str
    dormNumber: int
    room: int
    moveInDate: str
    isForeigner: bool
    notes: str = ""

    def to_dict(self):
        return {
            "isuId": self.isuId,
            "fullName": self.fullName,
            "group": self.group,
            "dormNumber": self.dormNumber,
            "room": self.room,
            "moveInDate": self.moveInDate,
            "isForeigner": self.isForeigner,
            "notes": self.notes
        }