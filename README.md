# Insight-Data-Engineering-Assessment
Language: Python v3.6
Major Libraries used: datetime, re
# Test Instructions
1) The folder 'insight_testsuite' contains a 'mytest.bat' which runs donation-analytics.py on itcont.txt in 'my_tests'. Run this first to generate 'repeat_donors.txt' for this test file.
2) Navigate to insight_testsuite -> tests -> my_tests -> output. Run 'compare_files.bat' to check if 'repeat_donors.txt' matches the expected output i.e. 'expected_output.txt'.

# Summary
My approach first identifies the repeat donors for each recipient, taking care of the input considerations. It then maps each recipient to his repeat donors, by zipcode and calendar year. Computations for running percentile, total donations and count of repeat donors are made for each recipient according to calendar year.
