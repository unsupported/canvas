# pullexams_bycourse.py
#
# Usage: python3 pullexams_bycourse.py <environment> <semester_code>
#
# Outputs: CSV of exam info with course info to cross-reference
#
# Args: Requires a target (test or prod) and any amount of terms
#       Note that terms must match the SIS ID for term in Canvas
#       See: https://canvas.instructure.com/doc/api/enrollment_terms.html
#
# Outline: 1. Request and document all courses matching criteria specified
#          2. Request and document all quiz info for courses from 1
#          3. Check quiz due dates against current date to filter further
#          4. Write remaining available quizzes to file
#
# General advice: * Most replacement should happen between <>
#                 * When you see {} do not remove w/o removing matching .format
#                 * Careful changing things, infinite loops are possible
#
# Author: Brandon Poulliot
#
# Works as of 9/20/19
