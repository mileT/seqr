"""
APIs used by the case review page
"""


import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from seqr.views.auth_api import API_LOGIN_REDIRECT_URL
from seqr.views.utils import get_user_info, render_with_initial_json, create_json_response
from seqr.models import Project, Family, Individual


logger = logging.getLogger(__name__)


@staff_member_required
def case_review_page(request, project_guid):
    """Generates the case review page, with initial case_review_page_data json embedded.

    Args:
        project_guid (string): GUID of the Project under case review.
    """

    initial_json = json.loads(
        case_review_page_data(request, project_guid).content
    )

    return render_with_initial_json('case_review.html', initial_json)


@staff_member_required(login_url=API_LOGIN_REDIRECT_URL)
def case_review_page_data(request, project_guid):
    """Returns a JSON object containing information used by the case review page:
    ::

      json_response = {
         'user': {..},
         'familiesByGuid': {..},
         'individualsByGuid': {..},
         'familyGuidToIndivGuids': {..},
       }
    Args:
        project_guid (string): GUID of the Project under case review.
    """

    # get all families in this project
    project = Project.objects.filter(guid=project_guid)
    if not project:
        raise ValueError("Invalid project id: %s" % project_guid)

    json_response = {
        'user': get_user_info(request.user),
        'familiesByGuid': {},
        'individualsByGuid': {},
        'familyGuidToIndivGuids': {},
    }

    project = project[0]
    project_json = {
        'project': {
            'projectGuid': '%s' % project.guid,
            'displayName': project.name,
            'deprecatedProjectId': project.deprecated_project_id,
        }
    }

    json_response.update(project_json)

    for i in Individual.objects.filter(family__project=project).select_related(
            'family'):

        # filter out individuals that were never in case review (or where case review status is set to -- )
        if not i.case_review_status:
            continue

        # process family record if it hasn't been added already
        family = i.family
        if str(family.guid) not in json_response['familiesByGuid']:
            json_response['familyGuidToIndivGuids']['%s' % family.guid] = []

            json_response['familiesByGuid']['%s' % family.guid] = _compute_json_for_family(family)

        json_response['familyGuidToIndivGuids']['%s' % family.guid].append('%s' % i.guid)

        json_response['individualsByGuid']['%s' % i.guid] = _compute_json_for_individual(i)

    return create_json_response(json_response)


@staff_member_required(login_url=API_LOGIN_REDIRECT_URL)
@csrf_exempt
def save_case_review_status(request, project_guid):
    """Updates the `case_review_status`, with initial case_review_page_data json embedded.

    Args:
        project_guid (string): GUID of the Project under case review.
    """

    project = Project.objects.get(guid=project_guid)

    requestJSON = json.loads(request.body)
    responseJSON = {}
    for individual_guid, new_case_review_status in requestJSON['form'].items():
        i = Individual.objects.get(family__project=project, guid=individual_guid)
        if i.case_review_status == new_case_review_status:
            continue
        i.case_review_status = new_case_review_status
        i.case_review_status_last_modified_by = request.user
        i.case_review_status_last_modified_date = timezone.now()
        i.save()

        responseJSON[i.guid] = _compute_json_for_individual(i)

    return create_json_response(responseJSON)


@staff_member_required(login_url=API_LOGIN_REDIRECT_URL)
@csrf_exempt
def save_internal_case_review_notes(request, project_guid, family_guid):
    """Updates the `case_review_notes` field for the given family.

    Args:
        project_guid (string): GUID of the project.
        family_guid  (string): GUID of the family.
    """

    family = Family.objects.get(guid=family_guid)
    requestJSON = json.loads(request.body)

    family.internal_case_review_notes = requestJSON['form']
    family.save()

    return create_json_response({family.guid: _compute_json_for_family(family)})


@staff_member_required(login_url=API_LOGIN_REDIRECT_URL)
@csrf_exempt
def save_internal_case_review_summary(request, project_guid, family_guid):
    """Updates the `internal_case_review_summary` field for the given family.

    Args:
        project_guid (string): GUID of the project.
        family_guid  (string): GUID of the family.
    """

    family = Family.objects.get(guid=family_guid)
    requestJSON = json.loads(request.body)

    family.internal_case_review_brief_summary = requestJSON['form']
    family.save()

    return create_json_response({family.guid: _compute_json_for_family(family)})


def _compute_json_for_family(family):
    """Returns a json object for the given individual, with all fields that are relevant to the case
    review page.

    Args:
        family (model): django model representing the individual.
    Returns:
        dict: json object
    """

    return {
        'familyGuid':      '%s' % family.guid,
        'familyId':        family.family_id,
        'displayName':     family.name,
        'description':     family.description,
        'analysisNotes':   family.analysis_notes,
        'analysisSummary': family.analysis_summary,
        'pedigreeImage':   family.pedigree_image.url if family.pedigree_image else None,
        'analysisStatus':  family.analysis_status,
        'causalInheritanceMode': family.causal_inheritance_mode,
        'internalCaseReviewNotes': family.internal_case_review_notes,
        'internalCaseReviewSummary': family.internal_case_review_brief_summary,
    }


def _compute_json_for_individual(individual):
    """Returns a json object for the given individual, with all fields that are relevant to the case
    review page.

    Args:
        individual (model): django model representing the individual.
    Returns:
        dict: json object
    """

    case_review_status_last_modified_by = None
    if individual.case_review_status_last_modified_by:
        u = individual.case_review_status_last_modified_by
        case_review_status_last_modified_by = u.email or u.username

    return {
        'individualGuid': '%s' % individual.guid,
        'individualId': individual.individual_id,
        'displayName': individual.display_name,
        'paternalId': individual.paternal_id,
        'maternalId': individual.maternal_id,
        'sex': individual.sex,
        'affected': individual.affected,
        'caseReviewStatus': individual.case_review_status,
        'caseReviewStatusLastModifiedBy': case_review_status_last_modified_by,
        'caseReviewStatusLastModifiedDate': individual.case_review_status_last_modified_date,
        'phenotipsPatientId': individual.phenotips_patient_id,
        'phenotipsData': json.loads(individual.phenotips_data) if individual.phenotips_data else None,
        'createdDate': individual.created_date,
        'lastModifiedDate': individual.last_modified_date,
    }