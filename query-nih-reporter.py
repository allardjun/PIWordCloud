#!/usr/bin/env python3

import requests
import argparse
import re
from collections import defaultdict

'''
Query the v2 NIH Reporter API

Example:

./query-nih-reporter.py -s gonadotropin -v --terms

See the documentation at https://api.reporter.nih.gov/
'''

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true', help="Verbose")
parser.add_argument('--projects', '-p', dest='projects', help="Project numbers, comma-delimited")
parser.add_argument('--searchtext', '-s', dest='search', help="Search string using API")
parser.add_argument('--fields', dest='fields', default='projecttitle,abstracttext', help="Fields to search using API")
parser.add_argument('--fuzzy', help="Do a fuzzy text search on 'terms'")
parser.add_argument('--terms', action='store_true', help="Print out numbers of 'terms'")
parser.add_argument('--filter', help="Do a case-insensitive string filter on records, comma-delimited")
args = parser.parse_args()

def main():
    rq = ReporterQuery(args.verbose)
    # Find grants using one or more project numbers
    if args.projects:
       rq.queryByProject(args.projects)
    # Find grants by string search (default fields: title, abstract)
    if args.search:
        rq.queryByText(args.search,args.fields)
    # Filter grants
    if args.filter:
        rq.doStringFilter(args.filter)
    if args.fuzzy:
        rq.doFuzzyTermFilter(args.fuzzy)
    # Count all the terms and print()
    if args.terms:
        rq.analyzeTerms()


class ReporterQuery:

    def __init__(self, verbose):
        self.verbose = verbose
        self.url = 'https://api.reporter.nih.gov/v2/projects/search'
        self.grants = []

    def queryByText(self, searchstr, fields):
        '''
        { "criteria": { advanced_text_search: { operator: "and", search_field: "projecttitle,terms", "search_text": "brain disorder" } } }
        '''
        params = { 'criteria': { 'advanced_text_search': { 'search_field': fields, 'search_text': searchstr } } }
        resp = requests.post(self.url, json=params)
        json = resp.json()
        if json['meta']['total'] == 0:
            if self.verbose:
                print("No records for search string '{}'".format(str))
            return
        if self.verbose:
            print("Found {0} records for search string '{1}'".format(json['meta']['total'], searchstr))
        self.grants = [g for g in json['results']]

    def queryByProject(self, projects):
        '''
        { "criteria": { project_nums:["5UG1HD078437-07","5R01DK102815-05"] } }
        '''
        params = { 'criteria': { 'project_nums': projects.split(',') } }
        resp = requests.post(self.url, json=params)
        json = resp.json()
        if json['meta']['total'] == 0:
            if self.verbose:
                print("No records for search string '{}'".format(projects))
            return
        if self.verbose:
            print("Found {0} records for projects '{1}'".format(json['meta']['total'], projects))
        self.grants = [g for g in json['results']]
        

    def doStringFilter(self, filters):
        projects = set()
        for filter in filters.split(','):
            # regex = filter str with word boundaries
            regex = r'\b' + re.escape(filter) + r'\b'
            for grant in self.grants:
                if re.search(regex, grant['abstract'], re.IGNORECASE):
                    projects.add(grant['projectNumber'])
        if projects:
            print("Filter:{0}\tProjects:{1}".format(
                filters, projects))

    def doFuzzyTermFilter(self, searchstr):
        from fuzzywuzzy import fuzz
        for grant in self.grants:
            for term in grant['terms'].split(';'):
                if fuzz.ratio(term, searchstr) > 80:
                    print("Term:{0}\tProject:{1}".format(
                        term, grant['projectNumber']))

    def analyzeTerms(self):
        terms = defaultdict(int)
        for grant in self.grants:
            for term in re.split(r"<|>", grant['terms']):
                terms[term] += 1
        for term in terms:
            print("{0}\t{1}".format(terms[term], term))


if __name__ == "__main__":
    main()

'''

{'appl_id': '10409743',
'subproject_id': '7754',
'fiscal_year': 2022,
'project_num': '5P30AG066515-03',
'project_serial_num': 'AG066515',
'organization': {'org_name': 'STANFORD UNIVERSITY',
'city': None,
'country': None,
'org_city': 'STANFORD',
'org_country': 'UNITED STATES',
'org_state': 'CA',
'org_state_name': None,
'dept_type': None,
'fips_country_code': None,
'org_duns': ['009214214'],
'org_ueis': ['HJD6G4D6TJY5'],
'primary_duns': '009214214',
'primary_uei': 'HJD6G4D6TJY5',
'org_fips': 'US',
'org_ipf_code': '8046501',
'org_zipcode': '943052004',
'external_org_id': 8046501},
'award_type': '5',
'activity_code': 'P30',
'award_amount': 588208,
'is_active': True,
'project_num_split': {'appl_type_code': '5',
'activity_code': 'P30',
'ic_code': 'AG',
'serial_num': '066515',
'support_year': '03',
'full_support_year': '03',
'suffix_code': ''},
'principal_investigators': [{'profile_id': 1889223,
'first_name': 'Victor',
'middle_name': '',
'last_name': 'Henderson',
'is_contact_pi': True,
'full_name': 'Victor  Henderson',
'title': 'PROFESSOR'}],
'contact_pi_name': 'HENDERSON, VICTOR ',
'program_officers': [],
'agency_ic_admin': {'code': 'AG',
'abbreviation': 'NIA',
'name': 'National Institute on Aging'},
'agency_ic_fundings': [{'fy': 2022,
'code': 'AG',
'name': 'National Institute on Aging',
'abbreviation': 'NIA',
'total_cost': 588208.0}],
'cong_dist': 'CA-18',
'spending_categories': None,
'project_start_date': '2020-06-01T12:06:00Z',
'project_end_date': '2025-03-31T12:03:00Z',
'organization_type': {'name': None,
'code': '10',
'is_other': True},
'full_foa': 'RFA-AG-20-004',
'full_study_section': {'srg_code': 'ZAG1',
'srg_flex': '',
'sra_designator_code': 'ZIJ',
'sra_flex_code': 'G',
'group_code': '',
'name': 'ZAG1-ZIJ-G'},
'award_notice_date': '2022-06-16T12:06:00Z',
'is_new': True,
'mechanism_code_dc': 'RC',
'core_project_num': 'P30AG066515',
'terms': "<Adult><21+ years old><Adult Human><adulthood><Age><ages><Elderly><advanced age><elders><geriatric><late life><later life><older adult><older person><senior citizen><Aging><Alzheimer's Disease><AD dementia><Alzheimer><Alzheimer Type Dementia><Alzheimer disease><Alzheimer sclerosis><Alzheimer syndrome><Alzheimer's><Alzheimer's disease dementia><Alzheimers Dementia><Alzheimers disease><Primary Senile Degenerative Dementia><dementia of the Alzheimer type><primary degenerative dementia><senile dementia of the Alzheimer type><Amyloid><Amyloid Substance><Brain><Brain Nervous System><Encephalon><Clinical Trials><Diagnosis><Disease><Disorder><Environment><Ethnic group><Ethnic People><Ethnic Population><Ethnicity People><Ethnicity Population><ethnicity group><Faculty><Goals><Grant><Immune System Diseases><Immune Diseases><Immune Disorders><Immune Dysfunction><Immune System Disorder><Immune System Dysfunction><Immune System and Related Disorders><Immunodeficiency and Immunosuppression Disorders><Immunologic Diseases><Immunological Diseases><Immunological Dysfunction><Immunological System Dysfunction><Magnetic Resonance Imaging><MR Imaging><MR Tomography><MRI><Medical Imaging, Magnetic Resonance / Nuclear Magnetic Resonance><NMR Imaging><NMR Tomography><Nuclear Magnetic Resonance Imaging><Zeugmatography><Nerve Degeneration><Neuron Degeneration><neural degeneration><neurodegeneration><neurodegenerative><neurological degeneration><neuronal degeneration><Parkinson Disease><Paralysis Agitans><Parkinson><Parkinson's disease><Parkinsons disease><Primary Parkinsonism><Patients><Phenotype><Population Control><Positron-Emission Tomography><PET><PET Scan><PET imaging><PETSCAN><PETT><Positron Emission Tomography Medical Imaging><Positron Emission Tomography Scan><Rad.-PET><positron emission tomographic (PET) imaging><positron emission tomographic imaging><positron emitting tomography><Research><Research Personnel><Investigators><Researchers><Research Support><Resources><Research Resources><Risk><medical school students><Medical Students><Time><Work><P-30 Protein><P30><P30 Protein><ranpirnase><Alzheimer beta-Protein><Alzheimer's Amyloid beta-Protein><Alzheimer's amyloid><Amyloid Alzheimer's Dementia Amyloid Protein><Amyloid Beta-Peptide><Amyloid Protein A4><Amyloid β><Amyloid β-Peptide><Amyloid β-Protein><Aβ><a beta peptide><abeta><amyloid beta><amyloid-b protein><beta amyloid fibril><soluble amyloid precursor protein><Amyloid beta-Protein><Measures><Medical Research><Lewy Bodies><neurofibrillary degeneration><neurofibrillary lesion><neurofibrillary pathology><tangle><Neurofibrillary Tangles><MT-bound tau><microtubule bound tau><microtubule-bound tau><tau><tau factor><τ Proteins><tau Proteins><Hispanic Populations><Spanish Origin><hispanic community><Hispanics><Latino><Clinical><Neurological><Neurologic><Training><insight><Individual><Family history of><Family Medical History><Family Medical History Epidemiology><Populations at Risk><Funding><alpha synuclein><NAC precursor><PARK1 protein><PARK4 protein><SNCA><SNCA protein><a-syn><a-synuclein><alphaSP22><asyn><non A-beta component of AD amyloid><non A4 component of amyloid precursor><α-syn><α-synuclein><Therapeutic><Senile Plaques><Amyloid Plaques><Neuritic Plaques><amyloid beta plaque><amyloid-b plaque><aβ plaques><cored plaque><diffuse plaque><Impaired cognition><Cognitive Disturbance><Cognitive Impairment><Cognitive decline><Cognitive function abnormal><Disturbance in cognition><cognitive dysfunction><cognitive loss><Consensus><Adopted><Protocols documentation><Protocol><Dementia><Amentia><Neurodegenerative Disorders><Degenerative Neurologic Diseases><Degenerative Neurologic Disorders><Nervous System Degenerative Diseases><Neural Degenerative Diseases><Neural degenerative Disorders><Neurodegenerative Diseases><Neurologic Degenerative Conditions><degenerative diseases of motor and sensory neurons><degenerative neurological diseases><neurodegenerative illness><cohort><Participant><graduate student><Categories><outreach><Pathogenesis><neuropathology><behavioral assessment><Behavior assessment><Adherence><Consent><Data><Catchment Area><Cognitive><enroll><Enrollment><1st degree relative><First Degree Relative><Active Follow-up><active followup><follow up><followed up><followup><follow-up><developmental><Development><Behavioral><imaging><Image><preclinical><pre-clinical><aberrant protein folding><abnormal protein folding><pathologic protein folding><protein mis-folding><protein misfolding><Clinical assessments><PD with dementia><Parkinson Dementia><Parkinson Disease dementia><Parkinson Disease with dementia><Parkinson's Disease dementia><Parkinson's disease with dementia><dementia in PD><dementia in Parkinson disease><Parkinson's Dementia><resilience><Population><Cognitive aging><resistant><Resistance><amyloid imaging><movement impairment><movement limitation><motor impairment><bio-markers><biologic marker><biomarker><Biological Markers><mild cognitive disorder><mild cognitive impairment><cognitive assessment><cognitive testing><Alzheimer's disease pathology><AD pathology><Alzheimer's pathology><Minority Enrollment><education research><recruit><participant retention><AD related dementia><ADRD><Alzheimer related dementia><Alzheimer's disease related dementia><patient enrollment><participant enrollment><Dementia with Lewy Bodies>",
'pref_terms': 'Adherence;Adopted;Adult;Age;Aging;Alzheimer&apos;s Disease;Alzheimer&apos;s disease pathology;Alzheimer&apos;s disease related dementia;Amyloid;Amyloid beta-Protein;Behavior assessment;Behavioral;Biological Markers;Brain;Catchment Area;Categories;Clinical;Clinical Trials;Clinical assessments;Cognitive;Cognitive aging;Consensus;Consent;Data;Dementia;Dementia with Lewy Bodies;Development;Diagnosis;Disease;Elderly;Enrollment;Environment;Ethnic group;Faculty;Family history of;First Degree Relative;Funding;Goals;Grant;Hispanics;Image;Immune System Diseases;Impaired cognition;Individual;Latino;Lewy Bodies;Magnetic Resonance Imaging;Measures;Medical Research;Medical Students;Minority Enrollment;Nerve Degeneration;Neurodegenerative Disorders;Neurofibrillary Tangles;Neurologic;Parkinson Disease;Parkinson&apos;s Dementia;Participant;Pathogenesis;Patients;Phenotype;Population;Population Control;Populations at Risk;Positron-Emission Tomography;Protocols documentation;Research;Research Personnel;Research Support;Resistance;Resources;Risk;Senile Plaques;Therapeutic;Time;Training;Work;alpha synuclein;amyloid imaging;cognitive testing;cohort;education research;follow-up;graduate student;insight;mild cognitive impairment;motor impairment;neuropathology;outreach;participant enrollment;participant retention;pre-clinical;protein misfolding;ranpirnase;recruit;resilience;tau Proteins',
'abstract_text': "1. SUMMARY (Clinical Core)\nIn support of the goals of the National Alzheimer's Project Act, the Stanford ADRC will focus on the\nAlzheimer's disease (AD) spectrum and the Lewy body (LB) spectrum of neurodegenerative cognitive\nimpairment. Recognizing that critical answers will emerge more readily when investigators can delve deeply\nwithin and across multiple levels of participant data, we have adopted a strategy of deep phenotyping. Stanford\nADRC participants are characterized intensively and followed over time. The AD spectrum includes cognitively\nimpaired patients with AD dementia and mild cognitive impairment due to AD, as well as preclinical AD inferred\nfrom biomarker data. The LB spectrum encompasses dementia with Lewy bodies and Parkinson's disease\ndementia and Parkinson's disease patients with mild cognitive impairment. Healthy adults without cognitive or\nmotor impairment can serve as an age-equivalent comparison population, as an asymptomatic at-risk\npopulation, and as a potential preclinical population in which mechanisms of cognitive aging and preclinical\ntransition can be studied. Within the LB spectrum, Parkinson's disease patients without cognitive impairment\nserve as age-equivalent comparators and as an at-risk transitional population for the development of LB-\nspectrum cognitive impairment. Stanford ADRC resources will enable the parallel study of these AD and LB\nspectrum disorders. Opportunities for investigators to compare and contrast can provide unique insights into\npathogenesis, resistance and resilience, and therapeutic approaches. The Clinical Core will be responsible for\nparticipant enrollment and for clinical, cognitive, and behavioral assessments. In support of a strategy that\nemphasizes the deep phenotyping of individual participants, the Clinical Core is also responsible for\nbiospecimen procurement, imaging referral, and brain donation consent. It is responsible for participant\nretention and for longitudinal follow-up. Most new participants in the Stanford ADRC will be asked to provide\ndisease-defining biomarkers measured in CSF, imaged by amyloid-PET/MRI, or both; to consent to\nlongitudinal follow-up; and to agree to brain donation through the Neuropathology Core. The Clinical Core will\nwork with other ADRC Cores to accomplish four aims focused on the AD spectrum and the LB spectrum of\nneurodegenerative cognitive impairment: (1) Enroll participants into longitudinal research protocols of the\nStanford ADRC; characterize their neurological, cognitive, and behavioral status; provide consensus\ndiagnoses; follow participants longitudinally; and promote adherence; (2) support the efforts of other ADRC\nCores; (3) support ADRC development project grants and research needs of qualified externally funded\ninvestigators who could benefit from Core resources; and (4) support the Research Education Component by\nproviding a rich training environment for medical and graduate students, residents, fellows, and junior faculty.",
'project_title': 'Clinical Core',
'phr_text': None,
'spending_categories_desc': None,
'agency_code': 'NIH',
'covid_response': None,
'arra_funded': 'N',
'budget_start': '2022-04-01T12:04:00Z',
'budget_end': '2023-03-31T12:03:00Z',
'cfda_code': None,
'funding_mechanism': 'Research Centers',
'direct_cost_amt': 384246,
'indirect_cost_amt': 203962,
'project_detail_url': 'https://reporter.nih.gov/project-details/10409743',
'date_added': '2022-06-18T04:06:17Z'}

'''