#include <iostream>
#include <string>
using namespace std;

enum Instruction {
	forward_ins, // direction no change
	back_ins, // right_ins right_ins 
	left_ins, // right_ins right_ins right_ins:w
	right_ins, // right_ins [base] 
	up_ins, // up_ins [base case]
	down_ins // up_ins right_ins right_ins 
};

// face direction of [facedirection][righthanddirection]
int faceAfterRight[6][6] = {
	{-1, 1, 2, -1, 4, 5},
	{0, -1, 2, 3, -1, 5},
	{0, 1, -1, 3, 4, -1},
	{-1, 1, 2, -1, 4, 5},
	{0, -1, 2, 3, -1, 5},
	{0, 1, -1, 3, 4, -1}
};

// righthand direction of [facedirection][righthanddirection]
int rightHandAfterRight[6][6] = {
	{-1, 3, 3, -1, 3, 3},
	{4, -1, 4, 4, -1, 4},
	{5, 5, -1, 5, 5, -1},
	{-1, 0, 0, -1, 0, 0},
	{1, -1, 1, 1, -1, 1},
	{2, 2, -1, 2, 2, -1}
};

int faceAfterUp[6][6] = {
	{-1, 2, 4, -1, 5, 1},
	{5, -1, 0, 2, -1, 3},
	{1, 3, -1, 4, 0, -1},
	{-1, 5, 1, -1, 2, 4},
	{2, -1, 3, 5, -1, 0},
	{4, 0, -1, 1, 3, -1}
};

int rightHandAfterUp[6][6] = {
	{-1, 1, 2, -1, 4, 5},
	{0, -1, 2, 3, -1, 5},
	{0, 1, -1, 3, 4, -1},
	{-1, 1, 2, -1, 4, 5},
	{0, -1, 2, 3, -1, 5},
	{0, 1, -1, 3, 4, -1}
};

int curFace = 0;
int curRightHand = 1;
int curX = 0;
int curY = 0;
int curZ = 0;

Instruction getInstructionFromString(string insString);

void getNewPosition(int oldFace, int oldRightHand, int oldX, int oldY, int oldZ, 
		Instruction ins, int offset, 
		int *newFace, int *newRightHand,
		int *newX, int *newY, int *newZ);

int main(int argc, char **argv) {
	int setNum;
	int insNum;
	cin>>setNum;
	string insString;
	int offset;
	for (int i = 0; i < setNum; ++i) {
		cin>>insNum;
		curX = curY = curZ = 0;
		curFace = 0;
		curRightHand = 1;
		for (int j = 0; j < insNum; ++j) {
			cin>>insString;
			cin>>offset;
			Instruction ins = getInstructionFromString(insString);
			getNewPosition(curFace, curRightHand, curX, curY, curZ, 
					ins, offset, &curFace, &curRightHand, &curX, &curY, &curZ);
		}
		cout<<curX<<' '<<curY<<' '<<curZ<<' '<<curFace<<endl;
	}
	return 0;
}

Instruction getInstructionFromString(string insString) {
	if (insString == "left") {
		return left_ins;
	} else if (insString == "right") {
		return right_ins;
	} else if (insString == "up") {
		return up_ins;
	} else if (insString == "down") {
		return down_ins;
	} else if (insString == "forward") {
		return forward_ins;
	} else { 
		return back_ins;
	}
}

void forwardOnDirection(int direction, int offset, int oldX, int oldY, int oldZ,
		int *newX, int *newY, int *newZ) {
	switch (direction) {
		case 0:
			*newX = oldX + offset;
			break;
		case 1:
			*newY = oldY + offset;
			break;
		case 2:
			*newZ = oldZ + offset;
			break;
		case 3:
			*newX = oldX - offset;
			break;
		case 4:
			*newY = oldY - offset;
			break;
		case 5:
			*newZ = oldZ - offset;
			break;
	}
}

void getNewDirection(int oldFace, int oldRightHand, int ins, 
		int *newFace, int *newRightHand) {
	switch (ins) {
		case forward_ins: // no change
			break;
		case back_ins: // right_ins, right_ins
			getNewDirection(oldFace, oldRightHand, right_ins, newFace, newRightHand);
			getNewDirection(*newFace, *newRightHand, right_ins, newFace, newRightHand);
			break;
		case left_ins: // right_ins, right_ins, right_ins
			getNewDirection(oldFace, oldRightHand, right_ins, newFace, newRightHand);
			getNewDirection(*newFace, *newRightHand, right_ins, newFace, newRightHand);
			getNewDirection(*newFace, *newRightHand, right_ins, newFace, newRightHand);
			break;
		case right_ins:
			*newFace = faceAfterRight[oldFace][oldRightHand];
			*newRightHand = rightHandAfterRight[oldFace][oldRightHand];
			break;
		case up_ins:
			*newFace = faceAfterUp[oldFace][oldRightHand];
			*newRightHand = rightHandAfterUp[oldFace][oldRightHand];
			break;
		case down_ins:
			getNewDirection(oldFace, oldRightHand, up_ins, newFace, newRightHand);
			getNewDirection(*newFace, *newRightHand, up_ins, newFace, newRightHand);
			getNewDirection(*newFace, *newRightHand, up_ins, newFace, newRightHand);
			break;
	}
}

void getNewPosition(int oldFace, int oldRightHand, int oldX, int oldY, int oldZ, 
		Instruction ins, int offset, 
		int *newFace, int *newRightHand,
		int *newX, int *newY, int *newZ) {
	getNewDirection(oldFace, oldRightHand, ins, newFace, newRightHand);
	forwardOnDirection(*newFace, offset, oldX, oldY, oldZ, newX, newY, newZ);
}

