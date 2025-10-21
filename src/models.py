from src.modules.auth.infrastructure.models import Permission, Role, RolePermission
from src.modules.competition.infrastructure.models import (
    Match,
    MatchParticipant,
    MatchResult,
    Sanction,
    SanctionType,
    StatDefinition,
    StudentMatchStat,
)
from src.modules.documents.infrastructure.models import Document
from src.modules.institutions.infrastructure.models import (
    EducationalInstitution,
    Representative,
)
from src.modules.locations.infrastructure.models import City
from src.modules.sports.infrastructure.models import (
    AgeCategory,
    Rule,
    Sport,
)
from src.modules.students.infrastructure.models import (
    Gender,
    Student,
    StudentDocument,
)
from src.modules.tournaments.infrastructure.models import (
    AcademicYear,
    Event,
    EventRule,
    Phase,
    Registration,
    Tournament,
    TournamentInstitution,
    Venue,
)
from src.modules.users.infrastructure.models import Person, User
