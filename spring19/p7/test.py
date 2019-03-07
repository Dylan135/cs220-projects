# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math, ast

PASS = "PASS"
TEXT_FORMAT = "text"
Question = collections.namedtuple("Question", ["number", "weight", "format"])

# group_weights = {
#     "test_get_value": 5,
#     "test_get_value": 2,
#     "test_get_highest_paid": 5,
#     "test_get_highest_worth": 5,
#     "test_get_column": 5,
#     "test_get_sorted": 3,
#     "test_avg_networth": 3,
#     "test_least_avg_age": 6,
#     "test_player_count": 4,
#     "test_max_players": 8,
#     "test_age_limit": 5,
#     "test_compare_clubs": 6,
#     "test_compare_clubs": 3,
#     "test_get_dictionary": 5,
#     "test_get_unique_element_list": 6,
#     "test_high_paying_clubs": 6,
#     "test_output_nat_club": 5,
#     "test_club_List": 5,
#     "test_best_scores_players": 8,
#     "test_find_savings": 5
# }



questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),    
]
question_nums = set([q.number for q in questions])


# JSON and plaintext values
expected_json = {
    "1": 'Argentina',
    "2": 'Cristiano Ronaldo',
    "3": 'Neymar',
    "4": 'Paris Saint-Germain',
    "5": ['Portugal', 'Argentina', 'Brazil', 'Uruguay', 'Germany'],
    "6": ['A. Abbas', 'A. Abbas', 'A. Abdallah', 'A. Abdennour', 'A. Abdi'],
    "7": 2407282.6149178543,
    "8": 25.133264640219817,
    "9": 355,
    "10": 800,
    "11": "England",
    "12": {'Id': '20801',
            'name': 'Cristiano Ronaldo',
            'Age': 32.0,
            'nationality': 'Portugal',
            'club': 'Real Madrid CF',
            'league': 'Spanish Primera División',
            'euro_wage': 565000.0,
            'networth': 95500000.0,
            'score_of_100': 94.0},
    "13": {'Id': '190871',
            'name': 'Neymar',
            'Age': 25.0,
            'nationality': 'Brazil',
            'club': 'Paris Saint-Germain',
            'league': 'French Ligue 1',
            'euro_wage': 280000.0,
            'networth': 123000000.0,
            'score_of_100': 92.0},
    "14": {'Id': '158023',
            'name': 'L. Messi',
            'Age': 30.0,
            'nationality': 'Argentina',
            'club': 'FC Barcelona',
            'league': 'Spanish Primera División',
            'euro_wage': 565000.0,
            'networth': 105000000.0,
            'score_of_100': 93.0},
    "15": {'Id': '192985',
            'name': 'K. De Bruyne',
            'Age': 26.0,
            'nationality': 'Belgium',
            'club': 'Manchester City',
            'league': 'English Premier League',
            'euro_wage': 285000.0,
            'networth': 83000000.0,
            'score_of_100': 89.0},
    "17": {'nationalities': 163, 'clubs': 647},
    "18": ['FC Bayern Munich',
 'Borussia Dortmund',
 'Bayer 04 Leverkusen',
 'FC Köln',
 'FC Schalke 04',
 'RB Leipzig',
 'Borussia Mönchengladbach',
 'TSG 1899 Hoffenheim',
 'SV Werder Bremen',
 'VfL Wolfsburg',
 'Hertha BSC Berlin',
 'Eintracht Frankfurt',
 'Hannover 96',
 'FC Augsburg',
 'VfB Stuttgart',
 'Hamburger SV',
 'FSV Mainz 05',
 'SC Freiburg'],
    "19": ['E. Hazard'],
    "20": "4941040.0"}
           
# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-301-test.ipynb'

    # re-execute it from the beginning
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines)
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        extra = set(actual) - set(expected)
        missing = set(expected) - set(actual)
        if extra:
            return "found unexpected entry in list: %s" % repr(list(extra)[0])
        elif missing:
            return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
        elif len(actual) != len(expected):
            return "expected %d entries in the list but found %d" % (len(expected), len(actual))
    else:
        if expected != actual:
            expected_mismatch = True
            
    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    nb = rerun_notebook(orig_notebook)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()