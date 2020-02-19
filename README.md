# interview-calendar

#### Task

Write a Python application which provides an API for an interview calendar.
There are interviewers and candidates. Each interview may consist of exactly one candidate
and one or more interviewers.
If there are more interviewers available than candidates, the spare interviewers are
distributed evenly across candidates.
An interview can only start on the hour.

1. Interviewers can add slots when they have time independently from each other
2. Candidates can add slots when they have time independently from each other
3. Anyone can retrieve a collection of slots when interviews can take place. The API
allows the caller to optionally define the candidate and optionally to define one or
more interviewer. The API requires either the candidate or the interviewer(s) to be
set

What we are looking for
* a RESTful API
* readable and tested code
* coding not just the "happy path" but also handling erroneous requests, ...
* usage of a VCS and an informative commit history
* to run the project via docker
* API docs, Quick start readme

#### Running the application
* Clone from github
* Go to the application root folder and run
``` docker-compose up ```

#### Endpoints

You can import Postman collection or follow the online documentation.

* Collection: 
* Documentation: 

#### Usage

* You must add some data in order to get this working. Please add Interviewers, Candidates, Interviewers Slots and Candidates Slots
* "Call endpoint": You can start a "Call" from the call endpoint, the system will look for available Candidates and Interviewers and generate the interviews.
* "Call with candidate": You can start a "Call" with an specific candidate (you must provide the id, it can be obtained in Candidates list endpoint), in that case the system will look for available interviewers.
* "Call with interviewers": You can start a "Call" with specific interviewers (you must provide the id separated by comma, it can be obtained in Interviewers list endpoint), in that case the system will look for available candidates.
* You can see available slots from "List Interviewers slots" and "List Candidates slots" endpoints.

#### Testing