HEADERS = \
	PayrollDatabase.h \
	Employee.h \
	AddEmployeeTransaction.h \
	AddSalariedEmployee.h \
	Transaction.h

CPP_FILES = \
	PayrollDatabase.cpp \
	PayrollTest.cpp \
	Employee.cpp \
	AddEmployeeTransaction.cpp

agile: ${HEADERS} ${CPP_FILES}
	g++ ${HEADERS} ${CPP_FILES} -I../gtest/include -o agile

