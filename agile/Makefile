HEADERS = \
	AddEmployeeTransaction.h \
	AddSalariedEmployee.h \
	AddHourlyEmployee.h \
	AddCommissionedEmployee.h \
	DeleteEmployeeTransaction.h \
	BiweeklySchedule.h \
	ChangeClassificationTransaction.h \
	ChangeEmployeeTransaction.h \
	CommissionedClassification.h \
	Employee.h \
	HoldMethod.h \
	HourlyClassification.h \
	HourlySchedule.h \
	PaymentClassification.h \
	PaymentMethod.h \
	PaymentSchedule.h \
	PayrollDatabase.h \
	SalariedClassification.h \
	WeeklySchedule.h \
	MonthlySchedule.h \
	Transaction.h

CPP_FILES = \
	AddEmployeeTransaction.cpp \
	AddSalariedEmployee.cpp \
	AddHourlyEmployee.cpp \
	AddCommissionedEmployee.cpp \
	DeleteEmployeeTransaction.cpp \
	BiweeklySchedule.cpp \
	Employee.cpp \
	HoldMethod.cpp \
	HourlySchedule.cpp \
	MonthlySchedule.cpp \
	PaymentMethod.cpp \
	PayrollDatabase.cpp \
	PayrollTest.cpp \
	SalariedClassification.cpp \
	HourlyClassification.cpp \
	WeeklySchedule.cpp

agile: ${HEADERS} ${CPP_FILES}
	g++ ${HEADERS} ${CPP_FILES} gtest_main.a -I../gtest/include -o agile



