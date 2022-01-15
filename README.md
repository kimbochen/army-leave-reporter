# Leave Reporter

This is a software service for soldiers to report their status during leave.

## Goals

Streamline the report process for both the reporters and the recievers, including:
- Give reporters an accessible UI to fill the information
- Give recievers quick access to automatically aggregated report

## System

The system contains 3 parts:
- Reporter End: Provides an interface for reporters
- Server End: Aggregates the reports into a specific format
- Reciever End: Outputs the aggregated report

### Reporter End

The reporter end is implemented using Google Forms.  
Google Forms provides an intuitive and flexible UI accessible to both desktop and mobile devices.

Users need to fill in 2 blanks:
1. Identity: Users pick their army ID and name in a drop down menu
1. Report content: Users fill in their report here.

There are 2 caveats when using Google Forms:
1. Google Forms is designed for anonymous submissions, which is orthogonal to this use case. 
1. A user needs to save a link to edit his reponse unless he logs in to his Google account.

### Server End

Google Forms stores all submissions into a Google spreadsheet.  
Hence, the server end leverages the Google Sheets API to aggregate all the records into a report.


### Reciever End

Conforming to the current report process, the reciever end needs to output the report to a LINE chat room.  
Thus, the reciever end is a LINE chat bot that interacts with reporters and recievers.

Tasks include:
- Sends a Google Form to the chat room at scheduled time.
- Sends the report message to the chat room for the recievers.
