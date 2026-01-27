36. Overview of Module endorsement
This section is completely optional. It is for students who have enjoyed the project so far and would like to do some more. It is not necessary to complete this part of the project to finish the course, and it will not be checked on submission. You can even work on this part of the project after the course is over, provided you copy these instructions.
The module endorsement is designed to search for a second class of violations, other than weather violations. Technically, endorsements have a technical meaning in aviation such as what planes a pilot is cleared to fly in. You saw some of this in the pilots module. However, this module includes all violations in which a pilot attempts a flight for which they are not qualified. This includes a solo flight before a solo certification, or an instrument flight without an instructor before a instrument rating. Finally, since it keeps track of instrument flight violations, it also identifies those cases in which a pilot attempts an instrument flight with a plane that is not certified for instrument flight.
This module will make use of two additional files in the dataset: instructors.csv and fleet.csv. The first is the list of all flight instructors and their qualifications (e.g. whether they can instruct instrument flying or only visual). The second is the list of all planes in the school and what qualifications are required to fly them.
NOTE: Remember to circle back to step 15. Implement ratings/endorsements and code the has_instrument_rating, has_advanced_endorsement, and has_multiengine_endorsement functions if you did not code them already.

codio@mike-panther:~/workspace/auditor$ python
...
>>> import tests
>>> tests.test_endorsements()
Testing module endorsements

Instructors File

ID, LAST, FIRST, CFI, CFII, MEI

CFI allows the instructor to teach single-engine non-instrument flying
CFII allows the instructor to teach instrument flying
MEI allows the instructor to teach multiengine-engine flying
