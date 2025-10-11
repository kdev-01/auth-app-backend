from src.core.database.models import AcademicYear, City, Document, Person, Role
from src.modules.auth.infrastructure.models import Permission, RolePermission
from src.modules.institutions.infrastructure.models import (
    EducationalInstitution,
    Representative,
)
from src.modules.sports.infrastructure.models import (
    AgeCategory,
    Discipline,
    Modality,
    Rule,
    Sport,
    SportCategory,
)
from src.modules.students.infrastructure.models import (
    Student,
    StudentDocument,
    StudentEnrolment,
)
from src.modules.tournaments.infrastructure.models import (
    Tournament,
    TournamentEvent,
    Venue,
)
from src.modules.users.infrastructure.models.user import User
