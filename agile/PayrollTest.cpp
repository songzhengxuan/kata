TEST(PayRollTest, TestAddSalariedEmployee) {
	int empId = 1;
	AddSalariedEmployee t(empId, "Bob", "Home", 1000.00);
	t.execute();
	
	Employee* e = GpayrollDatabase.GetEmployee(empId);

}
