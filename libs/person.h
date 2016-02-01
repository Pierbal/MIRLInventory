#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <ctime>

/*
PEOPLE
These are to keep track of people permissions, basic contact info,
and allow yus to bug them if they have yet to return things
*/

struct checkoutHistoryInfo_person{
	std::string number;
	std::string name;
	time_t startDate;
	time_t endDate;
	time_t returnDate;
};
struct LockedAccountInfo{
	bool administratorLock;
	bool overdueLock;
	bool unpaidMissingLock;
};

class Person{
	std::string number;
	std::string name;
	std::string email;
	std::string phoneNumber;
	std::string faxNumber; //jk - just here 'cause
	std::vector<struct checkoutHistoryInfo_person> checkoutHistory;
	int doorcode;
	std::string major;
	typedef enum{STUDENT,MEMBER,FACULTY,OFFICER,ADVISER}membership;
	membership membershipStatus;
	double unpaidBalance;

	Person(std::string number); //loads basic info from the file Tools/number.info
}
