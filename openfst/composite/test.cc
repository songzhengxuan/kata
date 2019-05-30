#include <iostream>
#include <fst/fst.h>
#include <fst/vector-fst.h>
using namespace std;
using namespace fst;

void createA(VectorFst<StdArc> &fst);
void createB(VectorFst<StdArc> &fst);

int main(int argc, char **argv)
{
    cout << "Hello world\n";
    VectorFst<StdArc> fst;

    fst.Write("T.fst");

    return 0;
}

void createA(VectorFst<StdArc> &fst) {

    fst.AddState();  // 1st state will be state 0 (returned by AddState)
    fst.SetStart(0); // arg is state ID

    // Add two arcs exiting state 0
    // Arc constructor args: ilabel, olabel, weight, dest state ID
    fst.AddArc(0, StdArc(1, 1, 0.5, 1));
    fst.AddArc(0, StdArc(2, 2, 1.5, 1));

    // Add state 1 and its arc
    fst.AddState();
    fst.AddArc(1, StdArc(3, 3, 2.5, 2));

    // Add state2 and set its final weight
    fst.AddState();
    fst.SetFinal(2, 3.5); // 1st arg is state ID, 2nd arg weight

    return;
}

void createB(VectorFst<StdArc> &fst) {

    fst.AddState();  // 1st state will be state 0 (returned by AddState)
    fst.SetStart(0); // arg is state ID

    // Add two arcs exiting state 0
    // Arc constructor args: ilabel, olabel, weight, dest state ID
    fst.AddArc(0, StdArc(1, 1, 0.5, 1));
    fst.AddArc(0, StdArc(2, 2, 1.5, 1));

    // Add state 1 and its arc
    fst.AddState();
    fst.AddArc(1, StdArc(3, 3, 2.5, 2));

    // Add state2 and set its final weight
    fst.AddState();
    fst.SetFinal(2, 3.5); // 1st arg is state ID, 2nd arg weight

    return;
}