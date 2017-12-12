''' simple test '''
import SimpleBackTracking
from queen import QueenCSP

def main():
    ''' main '''
    problem = QueenCSP(8)
    r, assgiment = SimpleBackTracking.backtracking_search(problem)
    print(r)
    print(assgiment)

if __name__ == '__main__':
    main()
