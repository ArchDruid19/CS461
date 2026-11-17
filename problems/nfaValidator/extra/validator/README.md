## Execution Instructions
- machine_parser.py, nfa_validator.py, nfa.py, and main.py all need to be in the same folder.
- To run the program, use: `python main.py "<description>"`
- Run the program using python version <= 3.14.9 

## Examples
### Strings Ending in 01
Input: ({A,B,C}, {0,1}, {(A,0,A), (A,1,A), (A,0,B), (B,1,C)}, A, {C})
Output: VALID

Input: ({A,B,C}, {0,1}, {(A,0,F), (A,1,A), (A,0,B), (B,1,C)}, A, {C})
Output: State F not in Q, but found in transition from A on 0
Output: INVALID

### Strings of The Form 0*1
Input: ({S,P,F}, {0,1}, {(S,eps,P), (P,0,P), (P,1,F)}, S, {F})
Output: VALID

### Exactly 01 or 02
Input: ({A,B,C,D}, {0,1,2}, {(A,0,B), (A,0,C), (B,1,D), (C,2,D)}, A, {D})
Output: VALID

### (0U1)*
Input: ({A,B,C,D,E}, {0,1}, {(A,eps,B), (B,eps,C), (B,eps,D), (C,0,E), (D,1,E), (E,eps,A)}, A, {B,E})
Output: VALID

Input: ({A,B,C,D,E}, {0,1,eps}, {(A,eps,B), (B,eps,C), (B,eps,D), (C,0,E), (D,1,E), (E,eps,A)}, A, {B,E})
Output: The empty string is not allowed as an input symbol
Output: INVALID

### Accepts Nothing (Language is the empty set)
Input: ({A}, {0}, {}, A, {})
Output: VALID

Input: "({A}, {0}, {}, A, {}))"
Output: ERROR: Extra ) closure at 21
Output: INVALID

## AI Acknowledgment
Claude Sonnet 5.5 Medium was used to help write the processor, along with the script for the video.
